from __future__ import annotations

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def client(monkeypatch: pytest.MonkeyPatch) -> Generator[TestClient, None, None]:
    monkeypatch.setenv("SECRET_KEY", "gateway-test-secret")
    monkeypatch.setenv("TOKEN_ISSUER", "gateway-test")
    monkeypatch.setenv("IDENTITY_SERVICE_URL", "http://identity.test/api/v1")
    monkeypatch.setenv("WORKSPACE_SERVICE_URL", "http://workspace.test/api/v1")
    monkeypatch.setenv("NOTIFICATION_SERVICE_URL", "http://notification.test/api/v1")
    monkeypatch.setenv("REDIS_URL", "")
    from app.core.config import get_settings
    from app.main import create_app

    get_settings.cache_clear()
    with TestClient(create_app()) as test_client:
        yield test_client
    get_settings.cache_clear()
