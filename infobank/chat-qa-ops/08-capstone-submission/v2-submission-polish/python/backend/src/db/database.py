from __future__ import annotations

import os
from collections.abc import Iterator
from contextlib import contextmanager

from core.config import load_settings
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from db.models import Base

_ENGINES: dict[str, Engine] = {}



def _create_engine(db_url: str) -> Engine:
    connect_args = {"check_same_thread": False} if db_url.startswith("sqlite") else {}
    return create_engine(db_url, connect_args=connect_args, future=True, pool_pre_ping=True)



def get_database_url() -> str:
    return os.getenv("QUALBOT_DB_URL", load_settings().db_url)



def get_engine() -> Engine:
    db_url = get_database_url()
    if db_url not in _ENGINES:
        _ENGINES[db_url] = _create_engine(db_url)
    return _ENGINES[db_url]



def reset_engines() -> None:
    for engine in _ENGINES.values():
        engine.dispose()
    _ENGINES.clear()



def init_db() -> None:
    Base.metadata.create_all(bind=get_engine())



def get_session_factory() -> sessionmaker[Session]:
    return sessionmaker(
        bind=get_engine(),
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
        future=True,
    )


@contextmanager
def session_scope() -> Iterator[Session]:
    session = get_session_factory()()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()



def get_db() -> Iterator[Session]:
    session = get_session_factory()()
    try:
        yield session
    finally:
        session.close()
