-- Papéis do Pics (ADR-007). Idempotente. Rode como superusuário, FORA das migrações.
-- Sem senhas aqui: defina com `ALTER ROLE <papel> PASSWORD '...'` fora do repositório.
--   pics_migration : dono dos objetos; roda o Alembic; nunca usado pela API.
--   app_runtime    : papel da API; sem SUPERUSER/BYPASSRLS; não é dono; grants mínimos.
--   pics_resolver  : NOLOGIN; dono das funções SECURITY DEFINER de resolução pré-contexto.
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'pics_resolver') THEN
        CREATE ROLE pics_resolver NOLOGIN NOSUPERUSER NOBYPASSRLS NOCREATEDB NOCREATEROLE;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'app_runtime') THEN
        CREATE ROLE app_runtime LOGIN NOSUPERUSER NOBYPASSRLS NOCREATEDB NOCREATEROLE;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'pics_migration') THEN
        CREATE ROLE pics_migration LOGIN NOSUPERUSER NOBYPASSRLS NOCREATEDB NOCREATEROLE;
    END IF;
END
$$;

-- A migração precisa trocar o dono das funções definer para pics_resolver.
GRANT pics_resolver TO pics_migration;

-- pics_migration cria os objetos (dono) e concede CREATE ao pics_resolver durante a
-- migração 0003 (PG15+ não dá CREATE no schema public a PUBLIC).
DO $$
BEGIN
    EXECUTE format('GRANT CREATE ON DATABASE %I TO pics_migration', current_database());
END
$$;
GRANT USAGE, CREATE ON SCHEMA public TO pics_migration WITH GRANT OPTION;
