import os
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine
from sqlalchemy.engine import URL, make_url

ROOT_DIR = Path(__file__).resolve().parents[2]
ROLES_SQL = ROOT_DIR / "infra" / "postgres" / "roles.sql"
ALLOWED_TEST_HOSTS = {"localhost", "127.0.0.1", "postgres"}
# Senha sintética, só para o banco descartável pics_test.
TEST_ROLE_PASSWORD = "synthetic-test-only"


def get_test_url() -> URL:
    raw_url = os.environ.get("DATABASE_URL")
    if not raw_url:
        pytest.skip(
            "PostgreSQL integration test requires DATABASE_URL in the environment"
        )
    try:
        parsed_url = make_url(raw_url)
    except (ValueError, TypeError):
        pytest.fail("DATABASE_URL is not a valid SQLAlchemy URL", pytrace=False)
    if (
        parsed_url.drivername != "postgresql+psycopg"
        or parsed_url.database != "pics_test"
        or parsed_url.host not in ALLOWED_TEST_HOSTS
    ):
        pytest.fail(
            "Integration tests require PostgreSQL Psycopg, a local host, and "
            "the pics_test database",
            pytrace=False,
        )
    return parsed_url


def ensure_roles(url: URL) -> None:
    """Cria os papéis (infra/postgres/roles.sql) e define senha sintética.
    Exige superusuário; só roda no banco descartável pics_test."""
    engine = create_engine(url)
    try:
        with engine.begin() as conn:
            raw = conn.connection.driver_connection
            assert raw is not None
            raw.execute(ROLES_SQL.read_text(encoding="utf-8"))  # type: ignore[attr-defined]
            for role in ("app_runtime", "pics_migration"):
                raw.execute(  # type: ignore[attr-defined]
                    f"ALTER ROLE {role} PASSWORD '{TEST_ROLE_PASSWORD}'"
                )
    finally:
        engine.dispose()


def role_url(url: URL, role: str) -> URL:
    return url.set(username=role, password=TEST_ROLE_PASSWORD)


def reset_database(config: Config, url: URL) -> None:
    """Desfaz tudo (superusuário) e migra como pics_migration, o caminho real:
    o dono dos objetos não é superusuário."""
    command.downgrade(config, "base")
    # O downgrade como superusuário deixa o alembic_version com dono superusuário
    # (em banco novo, como no CI); pics_migration não leria. Recria como dono real.
    engine = create_engine(url)
    try:
        with engine.begin() as conn:
            conn.exec_driver_sql("DROP TABLE IF EXISTS alembic_version")
    finally:
        engine.dispose()
    migration_url = role_url(url, "pics_migration")
    os.environ["MIGRATION_DATABASE_URL"] = migration_url.render_as_string(
        hide_password=False
    )
    try:
        command.upgrade(config, "head")
    finally:
        del os.environ["MIGRATION_DATABASE_URL"]
