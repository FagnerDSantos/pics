import os
from collections.abc import Iterator
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

import pytest
from alembic import command
from alembic.config import Config
from app.db.session import get_engine
from app.models import AuditLog, Session, User
from sqlalchemy import Engine, delete, inspect, select, update
from sqlalchemy.engine import make_url
from sqlalchemy.exc import DBAPIError, IntegrityError
from sqlalchemy.orm import Session as ORMSession

BACKEND_DIR = Path(__file__).resolve().parents[1]
ALLOWED_TEST_HOSTS = {"localhost", "127.0.0.1", "postgres"}


@pytest.fixture
def test_database() -> Iterator[tuple[Config, Engine]]:
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

    config = Config(str(BACKEND_DIR / "alembic.ini"))
    command.downgrade(config, "base")
    command.upgrade(config, "head")
    engine = get_engine()
    try:
        yield config, engine
    finally:
        engine.dispose()
        get_engine.cache_clear()
        command.downgrade(config, "base")
        command.upgrade(config, "head")


def test_migrations_persistence_and_database_constraints(
    test_database: tuple[Config, Engine],
) -> None:
    config, engine = test_database
    expected_tables = {"users", "sessions", "audit_log", "alembic_version"}
    assert expected_tables.issubset(set(inspect(engine).get_table_names()))

    user_id = uuid4()
    email = f"integration-{user_id.hex}@example.test"
    session_id = uuid4()
    audit_id = uuid4()
    token_hash = f"sha256:{uuid4().hex}"

    try:
        with ORMSession(engine) as db:
            user = User(
                id=user_id,
                email=email,
                role="client",
                full_name="Usuário Sintético",
            )
            db.add(user)
            db.flush()
            db.add(
                Session(
                    id=session_id,
                    user_id=user_id,
                    token_hash=token_hash,
                    expires_at=datetime.now(UTC),
                )
            )
            db.add(
                AuditLog(
                    id=audit_id,
                    actor_id=user_id,
                    action="integration_test",
                    entity="user",
                    entity_id=user_id,
                    meta={"source": "synthetic-test"},
                )
            )
            db.commit()

            saved_user = db.scalar(select(User).where(User.id == user_id))
            saved_session = db.scalar(
                select(Session).where(Session.id == session_id)
            )
            saved_audit = db.scalar(select(AuditLog).where(AuditLog.id == audit_id))
            assert saved_user is not None and saved_user.email == email
            assert saved_user.created_at.tzinfo is not None
            assert saved_session is not None
            assert saved_session.token_hash.startswith("sha256:")
            assert saved_audit is not None
            assert saved_audit.meta == {"source": "synthetic-test"}

            with pytest.raises(DBAPIError) as update_error:
                db.execute(
                    update(AuditLog)
                    .where(AuditLog.id == audit_id)
                    .values(action="tampered")
                )
            assert getattr(update_error.value.orig, "sqlstate", None) == "55000"
            db.rollback()

            with pytest.raises(DBAPIError) as delete_error:
                db.execute(delete(AuditLog).where(AuditLog.id == audit_id))
            assert getattr(delete_error.value.orig, "sqlstate", None) == "55000"
            db.rollback()

            saved_audit = db.scalar(select(AuditLog).where(AuditLog.id == audit_id))
            assert saved_audit is not None
            assert saved_audit.action == "integration_test"

            with pytest.raises(IntegrityError):
                db.add(
                    User(
                        email=email.upper(),
                        role="client",
                        full_name="Duplicado Sintético",
                    )
                )
                db.commit()
            db.rollback()

            with pytest.raises(IntegrityError):
                db.add(
                    User(
                        email=f"invalid-role-{uuid4().hex}@example.test",
                        role="superuser",
                        full_name="Papel Inválido Sintético",
                    )
                )
                db.commit()
            db.rollback()

            with pytest.raises(IntegrityError):
                db.add(
                    Session(
                        user_id=user_id,
                        token_hash=token_hash,
                        expires_at=datetime.now(UTC),
                    )
                )
                db.commit()
            db.rollback()

            db.execute(delete(Session).where(Session.id == session_id))
            db.commit()
    finally:
        engine.dispose()
        get_engine.cache_clear()

    command.downgrade(config, "base")
    check_engine = get_engine()
    try:
        assert not (expected_tables - {"alembic_version"}).intersection(
            set(inspect(check_engine).get_table_names())
        )
    finally:
        check_engine.dispose()
        get_engine.cache_clear()
    command.upgrade(config, "head")
