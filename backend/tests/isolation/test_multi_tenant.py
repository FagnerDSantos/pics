"""Isolamento entre estúdios (RLS) e funções de resolução pré-contexto.

Tudo conecta como `app_runtime` (sem SUPERUSER/BYPASSRLS, não dono). Dados
sintéticos, só no banco descartável pics_test.
"""
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from uuid import UUID, uuid4

import pytest
from alembic.config import Config
from app.core.tenancy import (
    clear_studio_context,
    create_studio,
    resolve_user_studios,
    set_studio_context,
)
from app.db.session import get_engine
from sqlalchemy import Engine, create_engine, text
from sqlalchemy.exc import DataError, DBAPIError, IntegrityError
from sqlalchemy.orm import Session as ORMSession

from tests.db_helpers import ensure_roles, get_test_url, reset_database, role_url

BACKEND_DIR = Path(__file__).resolve().parents[2]


@dataclass
class World:
    app_engine: Engine
    admin_engine: Engine
    studio_a: UUID
    studio_b: UUID
    user_a: UUID
    user_b: UUID
    user_loner: UUID


def sqlstate(error: DBAPIError) -> str | None:
    return getattr(error.orig, "sqlstate", None)


def new_slug() -> str:
    return f"s-{uuid4().hex[:12]}"


def insert_user(admin: Engine) -> UUID:
    user_id = uuid4()
    with admin.begin() as conn:
        conn.execute(
            text(
                "INSERT INTO users (id, email, role, full_name) "
                "VALUES (:id, :email, 'client', 'Sintético')"
            ),
            {"id": user_id, "email": f"{user_id.hex}@example.test"},
        )
    return user_id


@pytest.fixture(scope="module")
def world() -> Iterator[World]:
    url = get_test_url()
    ensure_roles(url)
    config = Config(str(BACKEND_DIR / "alembic.ini"))
    reset_database(config, url)

    admin = create_engine(url)
    app_engine = create_engine(
        role_url(url, "app_runtime"), pool_size=1, max_overflow=0
    )
    with admin.begin() as conn:
        # Só nos testes: emula a escrita em studio_members que a tarefa 007 concederá,
        # para provar que a RLS bloqueia escrita cruzada mesmo com o grant.
        conn.execute(
            text("GRANT INSERT, UPDATE, DELETE ON studio_members TO app_runtime")
        )
    user_a, user_b, loner = insert_user(admin), insert_user(admin), insert_user(admin)
    with ORMSession(app_engine) as db:
        studio_a = create_studio(db, "Estúdio A", new_slug(), user_a)
        studio_b = create_studio(db, "Estúdio B", new_slug(), user_b)
        db.commit()
    try:
        yield World(app_engine, admin, studio_a, studio_b, user_a, user_b, loner)
    finally:
        app_engine.dispose()
        admin.dispose()
        get_engine.cache_clear()


def scoped(world: World, studio_id: UUID | None) -> ORMSession:
    db = ORMSession(world.app_engine)
    if studio_id is not None:
        set_studio_context(db, studio_id)
    return db


def count(db: ORMSession, table: str) -> int:
    return int(db.execute(text(f"SELECT count(*) FROM {table}")).scalar_one())


def test_runtime_role_is_not_privileged(world: World) -> None:
    with scoped(world, None) as db:
        flags = db.execute(
            text(
                "SELECT rolsuper, rolbypassrls FROM pg_roles "
                "WHERE rolname = current_user"
            )
        ).one()
        assert tuple(flags) == (False, False)
        assert db.execute(text("SELECT current_user")).scalar_one() == "app_runtime"
        owned = db.execute(
            text("SELECT count(*) FROM pg_tables WHERE tableowner = current_user")
        ).scalar_one()
        assert owned == 0


def test_reads_are_isolated_between_studios(world: World) -> None:
    for mine, other in (
        (world.studio_a, world.studio_b),
        (world.studio_b, world.studio_a),
    ):
        with scoped(world, mine) as db:
            ids = set(db.execute(text("SELECT id FROM studios")).scalars())
            assert ids == {mine}
            members = set(
                db.execute(text("SELECT studio_id FROM studio_members")).scalars()
            )
            assert members == {mine}
            assert (
                db.execute(
                    text("SELECT count(*) FROM studios WHERE id = :o"), {"o": other}
                ).scalar_one()
                == 0
            )


def test_missing_or_empty_context_returns_nothing(world: World) -> None:
    with scoped(world, None) as db:
        assert count(db, "studios") == 0
        assert count(db, "studio_members") == 0
        assert count(db, "audit_log") == 0
    with scoped(world, None) as db:
        db.execute(text("SELECT set_config('app.studio_id', '', true)"))
        assert count(db, "studios") == 0
        assert count(db, "studio_members") == 0


def test_invalid_context_fails_closed(world: World) -> None:
    with scoped(world, None) as db:
        db.execute(text("SELECT set_config('app.studio_id', 'nao-e-uuid', true)"))
        with pytest.raises(DBAPIError) as error:
            db.execute(text("SELECT count(*) FROM studios"))
        assert sqlstate(error.value) == "22P02"
    with pytest.raises(TypeError):
        set_studio_context(ORMSession(world.app_engine), "x")  # type: ignore[arg-type]


def test_cross_studio_writes_are_rejected(world: World) -> None:
    # INSERT com studio_id de B sob contexto A.
    with scoped(world, world.studio_a) as db:
        with pytest.raises(DBAPIError) as error:
            db.execute(
                text(
                    "INSERT INTO studio_members (studio_id, user_id, role) "
                    "VALUES (:s, :u, 'studio_member')"
                ),
                {"s": world.studio_b, "u": world.user_loner},
            )
        assert sqlstate(error.value) == "42501"
    # INSERT sem contexto.
    with scoped(world, None) as db:
        with pytest.raises(DBAPIError) as error:
            db.execute(
                text(
                    "INSERT INTO studio_members (studio_id, user_id, role) "
                    "VALUES (:s, :u, 'studio_member')"
                ),
                {"s": world.studio_a, "u": world.user_loner},
            )
        assert sqlstate(error.value) == "42501"
    # UPDATE que move a linha de A para B (WITH CHECK).
    with scoped(world, world.studio_a) as db:
        with pytest.raises(DBAPIError) as error:
            db.execute(
                text("UPDATE studio_members SET studio_id = :b"),
                {"b": world.studio_b},
            )
        assert sqlstate(error.value) == "42501"
    # UPDATE e DELETE contra linhas de B: zero linhas afetadas.
    with scoped(world, world.studio_a) as db:
        updated = db.execute(
            text("UPDATE studios SET name = 'x' WHERE id = :b"), {"b": world.studio_b}
        )
        assert updated.rowcount == 0
        deleted = db.execute(
            text("DELETE FROM studio_members WHERE studio_id = :b"),
            {"b": world.studio_b},
        )
        assert deleted.rowcount == 0
    with scoped(world, world.studio_b) as db:
        assert count(db, "studio_members") == 1
    # Estúdio só nasce pela função definer.
    with scoped(world, world.studio_a) as db:
        with pytest.raises(DBAPIError) as error:
            db.execute(
                text("INSERT INTO studios (name, slug) VALUES ('x', :s)"),
                {"s": new_slug()},
            )
        assert sqlstate(error.value) == "42501"


def test_resolve_user_studios(world: World) -> None:
    with scoped(world, None) as db:
        assert resolve_user_studios(db, world.user_a) == [
            (world.studio_a, "studio_owner")
        ]
        assert resolve_user_studios(db, world.user_b) == [
            (world.studio_b, "studio_owner")
        ]
        assert resolve_user_studios(db, world.user_loner) == []
        assert resolve_user_studios(db, uuid4()) == []
        # app_runtime sem contexto não lê studio_members direto.
        assert count(db, "studio_members") == 0

    owner = insert_user(world.admin_engine)
    with ORMSession(world.app_engine) as db:
        suspended = create_studio(db, "Suspenso", new_slug(), owner)
        db.commit()
    with world.admin_engine.begin() as conn:
        conn.execute(
            text("UPDATE studios SET status = 'suspended' WHERE id = :i"),
            {"i": suspended},
        )
    with scoped(world, None) as db:
        assert resolve_user_studios(db, owner) == []


def test_create_studio_validation(world: World) -> None:
    owner = insert_user(world.admin_engine)
    slug = new_slug()
    with ORMSession(world.app_engine) as db:
        create_studio(db, "Ok", slug, owner)
        db.commit()
    with ORMSession(world.app_engine) as db:
        with pytest.raises(IntegrityError):
            create_studio(db, "Duplicado", slug, owner)
    for bad in ("Admin", "admin", "a", "-abc", "has space", "x" * 50):
        with ORMSession(world.app_engine) as db:
            with pytest.raises((IntegrityError, DataError)):
                create_studio(db, "Inválido", bad, owner)
    with ORMSession(world.app_engine) as db:
        with pytest.raises(IntegrityError):
            create_studio(db, "Sem dono", new_slug(), uuid4())


def test_definer_functions_are_hardened(world: World) -> None:
    names = ("resolve_user_studios", "create_studio", "audit_platform_event")
    with world.admin_engine.connect() as conn:
        rows = conn.execute(
            text(
                "SELECT p.proname, p.prosecdef, p.proconfig, r.rolname, r.rolsuper, "
                "r.rolbypassrls, r.rolcanlogin FROM pg_proc p "
                "JOIN pg_roles r ON r.oid = p.proowner "
                "WHERE p.pronamespace = 'public'::regnamespace "
                "AND p.proname = ANY(:names)"
            ),
            {"names": list(names)},
        ).all()
        assert {row[0] for row in rows} == set(names)
        for _, secdef, config, owner, is_super, bypass, can_login in rows:
            assert secdef is True
            assert config == ["search_path=pg_catalog, pg_temp"]
            assert owner == "pics_resolver"
            assert (is_super, bypass, can_login) == (False, False, False)
        public_exec = conn.execute(
            text(
                "SELECT count(*) FROM pg_proc p, aclexplode(p.proacl) a "
                "WHERE a.grantee = 0 AND p.proname = ANY(:names)"
            ),
            {"names": list(names)},
        ).scalar_one()
        assert public_exec == 0


def test_hostile_search_path_does_not_change_resolution(world: World) -> None:
    with scoped(world, None) as db:
        db.execute(
            text("CREATE TEMP TABLE studio_members (LIKE public.studio_members)")
        )
        db.execute(text("CREATE TEMP TABLE studios (LIKE public.studios)"))
        db.execute(text("SET LOCAL search_path = pg_temp, public"))
        assert resolve_user_studios(db, world.user_a) == [
            (world.studio_a, "studio_owner")
        ]


def test_audit_log_isolation_and_append_only(world: World) -> None:
    with scoped(world, world.studio_a) as db:
        db.execute(
            text(
                "INSERT INTO audit_log (studio_id, action, entity, entity_id) "
                "VALUES (:s, 'a', 'studio', :s)"
            ),
            {"s": world.studio_a},
        )
        db.commit()
    with scoped(world, world.studio_b) as db:
        db.execute(
            text(
                "INSERT INTO audit_log (studio_id, action, entity, entity_id) "
                "VALUES (:s, 'b', 'studio', :s)"
            ),
            {"s": world.studio_b},
        )
        db.commit()
    with scoped(world, world.studio_a) as db:
        actions = set(db.execute(text("SELECT action FROM audit_log")).scalars())
        assert actions == {"a"}
        for sql, params in (
            (
                "INSERT INTO audit_log (studio_id, action, entity, entity_id) "
                "VALUES (:s, 'x', 'studio', :s)",
                {"s": world.studio_b},
            ),
            (
                "INSERT INTO audit_log (studio_id, action, entity, entity_id) "
                "VALUES (NULL, 'x', 'studio', :s)",
                {"s": world.studio_a},
            ),
            ("UPDATE audit_log SET action = 'x'", {}),
            ("DELETE FROM audit_log", {}),
            ("TRUNCATE audit_log", {}),
        ):
            with pytest.raises(DBAPIError) as error:
                db.execute(text(sql), params)
            assert sqlstate(error.value) == "42501", sql
            db.rollback()
            set_studio_context(db, world.studio_a)


def test_platform_audit_event_is_invisible_to_tenants(world: World) -> None:
    marker = uuid4()
    with scoped(world, None) as db:
        db.execute(
            text(
                "SELECT public.audit_platform_event("
                ":actor, 'platform.test', 'user', :entity, NULL, NULL)"
            ),
            {"actor": world.user_a, "entity": marker},
        )
        db.commit()
    with scoped(world, world.studio_a) as db:
        assert (
            db.execute(
                text("SELECT count(*) FROM audit_log WHERE entity_id = :e"),
                {"e": marker},
            ).scalar_one()
            == 0
        )
    with world.admin_engine.connect() as conn:
        row = conn.execute(
            text("SELECT studio_id, meta FROM audit_log WHERE entity_id = :e"),
            {"e": marker},
        ).one()
        assert row[0] is None and row[1] == {}


def test_owner_cannot_truncate_or_orphan_audit_log(world: World) -> None:
    with world.admin_engine.connect() as conn:
        with pytest.raises(DBAPIError) as error:
            conn.execute(text("TRUNCATE audit_log"))
        assert sqlstate(error.value) == "55000"
    with world.admin_engine.connect() as conn:
        with pytest.raises(IntegrityError) as fk_error:
            conn.execute(
                text("DELETE FROM studios WHERE id = :s"), {"s": world.studio_a}
            )
        assert sqlstate(fk_error.value) == "23503"


def test_context_does_not_leak_through_pool_commit_or_rollback(
    world: World,
) -> None:
    # pool_size=1: a mesma conexão física é reutilizada em todas as etapas.
    with world.app_engine.connect() as conn:
        conn.execute(
            text("SELECT set_config('app.studio_id', :s, true)"),
            {"s": str(world.studio_a)},
        )
        assert conn.execute(text("SELECT count(*) FROM studios")).scalar_one() == 1
        conn.commit()
    with world.app_engine.connect() as conn:
        assert conn.execute(text("SELECT count(*) FROM studios")).scalar_one() == 0
        conn.execute(
            text("SELECT set_config('app.studio_id', :s, true)"),
            {"s": str(world.studio_a)},
        )
        conn.rollback()
        assert conn.execute(text("SELECT count(*) FROM studios")).scalar_one() == 0

    # Sessão com contexto: reaplicado após commit no meio da requisição.
    with scoped(world, world.studio_a) as db:
        assert count(db, "studios") == 1
        db.commit()
        assert set(db.execute(text("SELECT id FROM studios")).scalars()) == {
            world.studio_a
        }
        db.rollback()
        assert count(db, "studios") == 1
        clear_studio_context(db)
        assert count(db, "studios") == 0
        db.commit()
        assert count(db, "studios") == 0
    with scoped(world, None) as db:
        assert count(db, "studios") == 0


def test_grants_and_platform_audit_validation(world: World) -> None:
    with scoped(world, world.studio_a) as db:
        for sql in (
            "UPDATE studios SET status = 'active'",
            "UPDATE studios SET slug = 'novo-slug-x'",
        ):
            with pytest.raises(DBAPIError) as error:
                db.execute(text(sql))
            assert sqlstate(error.value) == "42501"
            db.rollback()
            set_studio_context(db, world.studio_a)
        assert (
            db.execute(text("UPDATE studios SET name = 'Novo nome'")).rowcount == 1
        )
        db.rollback()
    for action in ("x", "admin.forged", "platform.", None):
        with scoped(world, None) as db:
            with pytest.raises(DBAPIError) as error:
                db.execute(
                    text(
                        "SELECT public.audit_platform_event("
                        ":a, :act, 'user', :e, NULL, NULL)"
                    ),
                    {"a": world.user_a, "act": action, "e": uuid4()},
                )
            assert sqlstate(error.value) == "22023"
    with scoped(world, None) as db:
        with pytest.raises(DBAPIError) as error:
            db.execute(
                text(
                    "SELECT public.audit_platform_event("
                    ":a, 'platform.big', 'user', :e, NULL, CAST(:m AS jsonb))"
                ),
                {"a": world.user_a, "e": uuid4(), "m": '{"k": "' + "x" * 5000 + '"}'},
            )
        assert sqlstate(error.value) == "22023"


def test_catalog_every_tenant_table_has_forced_rls(world: World) -> None:
    global_tables = {"users", "sessions", "alembic_version"}
    with world.admin_engine.connect() as conn:
        rows = conn.execute(
            text(
                "SELECT c.relname, c.relrowsecurity, c.relforcerowsecurity, "
                "(SELECT count(*) FROM pg_policy p WHERE p.polrelid = c.oid) "
                "FROM pg_class c WHERE c.relnamespace = 'public'::regnamespace "
                "AND c.relkind = 'r'"
            )
        ).all()
    assert {row[0] for row in rows} >= {"studios", "studio_members", "audit_log"}
    for name, rls, forced, policies in rows:
        if name in global_tables:
            continue
        assert rls and forced and policies >= 1, name


def test_runtime_privileges_are_minimal(world: World) -> None:
    checks = {
        ("audit_log", "UPDATE"): False,
        ("audit_log", "DELETE"): False,
        ("audit_log", "TRUNCATE"): False,
        ("audit_log", "REFERENCES"): False,
        ("audit_log", "TRIGGER"): False,
        ("audit_log", "SELECT"): True,
        ("audit_log", "INSERT"): True,
        ("studios", "INSERT"): False,
        ("studios", "DELETE"): False,
        ("alembic_version", "SELECT"): False,
    }
    with world.admin_engine.connect() as conn:
        for (table, privilege), expected in checks.items():
            granted = conn.execute(
                text("SELECT has_table_privilege('app_runtime', :t, :p)"),
                {"t": f"public.{table}", "p": privilege},
            ).scalar_one()
            assert granted is expected, (table, privilege)
        for column in ("status", "slug", "id"):
            assert not conn.execute(
                text(
                    "SELECT has_column_privilege("
                    "'app_runtime', 'public.studios', :c, 'UPDATE')"
                ),
                {"c": column},
            ).scalar_one()


def test_table_owner_cannot_mutate_audit_log(world: World) -> None:
    # FORCE RLS: o dono não tem policy em audit_log, então não vê nem altera linhas.
    migration_engine = create_engine(role_url(get_test_url(), "pics_migration"))
    try:
        with migration_engine.connect() as conn:
            for sql in ("UPDATE audit_log SET action = 'x'", "DELETE FROM audit_log"):
                assert conn.execute(text(sql)).rowcount == 0
                conn.rollback()
    finally:
        migration_engine.dispose()
