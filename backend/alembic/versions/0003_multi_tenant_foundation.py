"""Multi-tenant foundation: studios, studio_members, RLS, resolver functions.

Revision ID: 0003_multi_tenant
Revises: 0002_audit_log_append_only
Create Date: 2026-11-03

Os papéis (pics_migration, app_runtime, pics_resolver) são criados fora da
migração, por infra/postgres/roles.sql. Aqui só há GRANT/REVOKE; nunca DROP ROLE.
"""
from collections.abc import Sequence
from typing import Union

from alembic import op

revision: str = "0003_multi_tenant"
down_revision: Union[str, Sequence[str], None] = "0002_audit_log_append_only"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

CTX = "public.current_studio_id()"

SIGNATURES = (
    "public.resolve_user_studios(uuid)",
    "public.create_studio(text, text, uuid)",
    "public.audit_platform_event(uuid, text, text, uuid, text, jsonb)",
)


def upgrade() -> None:
    op.execute(
        """
        DO $$
        BEGIN
            IF (SELECT count(*) FROM pg_roles
                WHERE rolname IN ('app_runtime', 'pics_resolver')) < 2 THEN
                RAISE EXCEPTION
                    'roles ausentes: rode infra/postgres/roles.sql';
            END IF;
        END
        $$
        """
    )

    # Contexto do estúdio (não é definer; tudo qualificado com pg_catalog).
    # Ausente ou vazio -> NULL (nenhuma linha casa).
    # Valor malformado -> erro de cast (fail-closed).
    op.execute(
        """
        CREATE FUNCTION public.current_studio_id()
        RETURNS uuid
        LANGUAGE sql
        STABLE
        AS $$
            SELECT NULLIF(pg_catalog.current_setting('app.studio_id', true), '')::uuid
        $$
        """
    )

    op.execute(
        """
        CREATE TABLE public.studios (
            id uuid NOT NULL DEFAULT gen_random_uuid(),
            name varchar(200) NOT NULL,
            slug varchar(40) NOT NULL,
            status varchar(16) NOT NULL DEFAULT 'active',
            created_at timestamptz NOT NULL DEFAULT now(),
            CONSTRAINT pk_studios PRIMARY KEY (id),
            CONSTRAINT uq_studios_slug UNIQUE (slug),
            CONSTRAINT ck_studios_status
                CHECK (status IN ('active', 'suspended', 'canceled')),
            CONSTRAINT ck_studios_slug
                CHECK (slug ~ '^[a-z0-9][a-z0-9-]{1,38}[a-z0-9]$'
                       AND slug NOT IN
                       ('admin', 'api', 'app', 'www', 'mail', 'static', 'assets'))
        )
        """
    )
    op.execute(
        """
        CREATE TABLE public.studio_members (
            studio_id uuid NOT NULL,
            user_id uuid NOT NULL,
            role varchar(16) NOT NULL,
            CONSTRAINT pk_studio_members PRIMARY KEY (studio_id, user_id),
            CONSTRAINT fk_studio_members_studio_id_studios
                FOREIGN KEY (studio_id) REFERENCES public.studios (id)
                ON DELETE CASCADE,
            CONSTRAINT fk_studio_members_user_id_users
                FOREIGN KEY (user_id) REFERENCES public.users (id)
                ON DELETE CASCADE,
            CONSTRAINT ck_studio_members_role
                CHECK (role IN ('studio_owner', 'studio_member', 'assembler'))
        )
        """
    )
    op.execute(
        "CREATE INDEX ix_studio_members_user_id ON public.studio_members (user_id)"
    )

    # audit_log mista: RESTRICT (SET NULL dispararia UPDATE e o trigger append-only).
    op.execute("ALTER TABLE public.audit_log ADD COLUMN studio_id uuid")
    op.execute(
        """
        ALTER TABLE public.audit_log
            ADD CONSTRAINT fk_audit_log_studio_id_studios
            FOREIGN KEY (studio_id) REFERENCES public.studios (id) ON DELETE RESTRICT
        """
    )
    op.execute(
        "CREATE INDEX ix_audit_log_studio_id_at ON public.audit_log (studio_id, at)"
    )
    op.execute(
        """
        CREATE TRIGGER audit_log_no_truncate
        BEFORE TRUNCATE ON public.audit_log
        FOR EACH STATEMENT
        EXECUTE FUNCTION public.prevent_audit_log_mutation()
        """
    )

    # ---- RLS ----
    for table in ("studios", "studio_members", "audit_log"):
        op.execute(f"ALTER TABLE public.{table} ENABLE ROW LEVEL SECURITY")
        op.execute(f"ALTER TABLE public.{table} FORCE ROW LEVEL SECURITY")

    op.execute(
        f"""
        CREATE POLICY studios_tenant ON public.studios
            FOR ALL TO app_runtime
            USING (id = {CTX}) WITH CHECK (id = {CTX})
        """
    )
    op.execute(
        """
        CREATE POLICY studios_resolver_select ON public.studios
            FOR SELECT TO pics_resolver USING (true)
        """
    )
    op.execute(
        """
        CREATE POLICY studios_resolver_insert ON public.studios
            FOR INSERT TO pics_resolver WITH CHECK (true)
        """
    )
    op.execute(
        f"""
        CREATE POLICY studio_members_tenant ON public.studio_members
            FOR ALL TO app_runtime
            USING (studio_id = {CTX}) WITH CHECK (studio_id = {CTX})
        """
    )
    op.execute(
        """
        CREATE POLICY studio_members_resolver_select ON public.studio_members
            FOR SELECT TO pics_resolver USING (true)
        """
    )
    op.execute(
        """
        CREATE POLICY studio_members_resolver_insert ON public.studio_members
            FOR INSERT TO pics_resolver WITH CHECK (true)
        """
    )
    op.execute(
        f"""
        CREATE POLICY audit_log_tenant_select ON public.audit_log
            FOR SELECT TO app_runtime USING (studio_id = {CTX})
        """
    )
    op.execute(
        f"""
        CREATE POLICY audit_log_tenant_insert ON public.audit_log
            FOR INSERT TO app_runtime WITH CHECK (studio_id = {CTX})
        """
    )
    op.execute(
        """
        CREATE POLICY audit_log_platform_insert ON public.audit_log
            FOR INSERT TO pics_resolver WITH CHECK (studio_id IS NULL)
        """
    )

    # ---- Grants mínimos explícitos (sem ALTER DEFAULT PRIVILEGES) ----
    op.execute("GRANT USAGE ON SCHEMA public TO app_runtime, pics_resolver")
    op.execute(
        "GRANT EXECUTE ON FUNCTION public.current_studio_id() "
        "TO app_runtime, pics_resolver"
    )
    op.execute("GRANT SELECT, INSERT, UPDATE ON public.users TO app_runtime")
    op.execute("GRANT SELECT, INSERT, UPDATE, DELETE ON public.sessions TO app_runtime")
    # Só o nome do estúdio é editável pela API; status/slug/id não (suspensão é da
    # plataforma). studio_members é só leitura: escrita e papéis são da tarefa 007.
    op.execute("GRANT SELECT, UPDATE (name) ON public.studios TO app_runtime")
    op.execute("GRANT SELECT ON public.studio_members TO app_runtime")
    op.execute("GRANT SELECT, INSERT ON public.audit_log TO app_runtime")
    op.execute(
        "GRANT SELECT, INSERT ON public.studios, public.studio_members "
        "TO pics_resolver"
    )
    op.execute("GRANT INSERT ON public.audit_log TO pics_resolver")

    # ---- Funções de resolução pré-contexto (S-40, D-32) ----
    op.execute(
        """
        CREATE FUNCTION public.resolve_user_studios(p_user_id uuid)
        RETURNS TABLE (studio_id uuid, role text)
        LANGUAGE sql
        STABLE
        SECURITY DEFINER
        SET search_path = pg_catalog, pg_temp
        AS $$
            SELECT m.studio_id, m.role::text
            FROM public.studio_members AS m
            JOIN public.studios AS s ON s.id = m.studio_id
            WHERE m.user_id = p_user_id AND s.status = 'active'
        $$
        """
    )
    op.execute(
        """
        CREATE FUNCTION public.create_studio(
            p_name text, p_slug text, p_owner_user_id uuid
        )
        RETURNS uuid
        LANGUAGE sql
        VOLATILE
        SECURITY DEFINER
        SET search_path = pg_catalog, pg_temp
        AS $$
            WITH s AS (
                INSERT INTO public.studios (name, slug) VALUES (p_name, p_slug)
                RETURNING id
            ), m AS (
                INSERT INTO public.studio_members (studio_id, user_id, role)
                SELECT id, p_owner_user_id, 'studio_owner' FROM s
            )
            SELECT id FROM s
        $$
        """
    )
    op.execute(
        """
        CREATE FUNCTION public.audit_platform_event(
            p_actor_id uuid, p_action text, p_entity text, p_entity_id uuid,
            p_ip_hash text, p_meta jsonb
        )
        RETURNS void
        LANGUAGE plpgsql
        VOLATILE
        SECURITY DEFINER
        SET search_path = pg_catalog, pg_temp
        AS $$
        BEGIN
            IF p_action IS NULL OR p_action !~ '^platform[.][a-z0-9_.]{1,80}$' THEN
                RAISE EXCEPTION 'invalid platform audit action'
                    USING ERRCODE = '22023';
            END IF;
            IF p_meta IS NOT NULL AND pg_column_size(p_meta) > 4096 THEN
                RAISE EXCEPTION 'audit meta too large' USING ERRCODE = '22023';
            END IF;
            INSERT INTO public.audit_log
                (actor_id, studio_id, action, entity, entity_id, ip_hash, meta)
            VALUES
                (p_actor_id, NULL, p_action, p_entity, p_entity_id, p_ip_hash,
                 COALESCE(p_meta, '{}'::jsonb));
        END
        $$
        """
    )

    # O novo dono precisa de CREATE no schema para ALTER OWNER; revogado em seguida.
    op.execute("GRANT CREATE ON SCHEMA public TO pics_resolver")
    for signature in SIGNATURES:
        op.execute(f"ALTER FUNCTION {signature} OWNER TO pics_resolver")
        op.execute(f"REVOKE ALL ON FUNCTION {signature} FROM PUBLIC")
        op.execute(f"GRANT EXECUTE ON FUNCTION {signature} TO app_runtime")
    op.execute("REVOKE CREATE ON SCHEMA public FROM pics_resolver")


def downgrade() -> None:
    for signature in SIGNATURES:
        op.execute(f"DROP FUNCTION {signature}")
    op.execute("DROP TRIGGER audit_log_no_truncate ON public.audit_log")
    op.execute("DROP POLICY audit_log_tenant_select ON public.audit_log")
    op.execute("DROP POLICY audit_log_tenant_insert ON public.audit_log")
    op.execute("DROP POLICY audit_log_platform_insert ON public.audit_log")
    op.execute("ALTER TABLE public.audit_log NO FORCE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE public.audit_log DISABLE ROW LEVEL SECURITY")
    op.execute("REVOKE ALL ON public.audit_log FROM app_runtime, pics_resolver")
    op.execute("DROP INDEX public.ix_audit_log_studio_id_at")
    op.execute(
        "ALTER TABLE public.audit_log DROP CONSTRAINT fk_audit_log_studio_id_studios"
    )
    op.execute("ALTER TABLE public.audit_log DROP COLUMN studio_id")
    op.execute("REVOKE ALL ON public.users, public.sessions FROM app_runtime")
    op.execute("DROP TABLE public.studio_members")
    op.execute("DROP TABLE public.studios")
    op.execute("DROP FUNCTION public.current_studio_id()")
