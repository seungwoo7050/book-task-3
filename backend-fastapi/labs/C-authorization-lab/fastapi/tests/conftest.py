from __future__ import annotations

import os
from collections.abc import Generator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def app_env(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Generator[None, None, None]:
    database_path = tmp_path / "c_authorization_lab_test.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite+pysqlite:///{database_path}")

    from app.core.config import get_settings
    from app.db.base import Base
    from app.db.models import authorization as authorization_models  # noqa: F401
    from app.db.session import configure_engine, get_engine

    get_settings.cache_clear()
    configure_engine(os.environ["DATABASE_URL"])
    engine = get_engine()
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    get_settings.cache_clear()


@pytest.fixture()
def client(app_env: None) -> Generator[TestClient, None, None]:
    from app.main import create_app

    with TestClient(create_app()) as test_client:
        yield test_client
