import os
from collections.abc import Generator
from functools import lru_cache

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session as ORMSession
from sqlalchemy.orm import sessionmaker


@lru_cache(maxsize=1)
def get_engine() -> Engine:
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL must be set in the process environment.")

    return create_engine(database_url, pool_pre_ping=True)


def get_db_session() -> Generator[ORMSession, None, None]:
    with sessionmaker(bind=get_engine(), expire_on_commit=False)() as session:
        yield session
