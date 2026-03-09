from __future__ import annotations

from urllib.parse import parse_qs, urlparse

from fastapi.testclient import TestClient

from app.domain.services.google_oidc import GoogleOIDCService


def _mock_google(monkeypatch) -> None:
    monkeypatch.setattr(
        GoogleOIDCService,
        "exchange_code_for_tokens",
        lambda self, code, code_verifier: {"access_token": "access", "id_token": "id-token"},
    )
    monkeypatch.setattr(
        GoogleOIDCService,
        "validate_id_token",
        lambda self, id_token, nonce: {
            "sub": "subject-refresh",
            "email": "refresh@example.com",
            "email_verified": True,
            "name": "Refresh User",
        },
    )
    monkeypatch.setattr(
        GoogleOIDCService,
        "fetch_userinfo",
        lambda self, access_token: {"picture": "https://example.com/avatar.png"},
    )


def _login(client: TestClient) -> None:
    login_response = client.get("/api/v1/auth/google/login")
    state = parse_qs(urlparse(login_response.json()["authorization_url"]).query)["state"][0]
    callback_response = client.get(
        "/api/v1/auth/google/callback",
        params={"code": "refresh-code", "state": state},
    )
    assert callback_response.status_code == 200


def test_refresh_rotation_detects_reuse(client: TestClient, monkeypatch) -> None:
    _mock_google(monkeypatch)
    _login(client)

    original_refresh = client.cookies["refresh_token"]
    csrf_token = client.cookies["csrf_token"]

    refresh_response = client.post(
        "/api/v1/auth/token/refresh", headers={"X-CSRF-Token": csrf_token}
    )
    assert refresh_response.status_code == 200
    rotated_csrf = client.cookies["csrf_token"]

    attacker = TestClient(client.app)
    attacker.cookies.set("refresh_token", original_refresh)
    attacker.cookies.set("csrf_token", "attacker-csrf")
    reuse_response = attacker.post(
        "/api/v1/auth/token/refresh",
        headers={"X-CSRF-Token": "attacker-csrf"},
    )
    assert reuse_response.status_code == 401
    assert reuse_response.json()["error"]["code"] == "REFRESH_TOKEN_REUSED"

    family_revoked_response = client.post(
        "/api/v1/auth/token/refresh",
        headers={"X-CSRF-Token": rotated_csrf},
    )
    assert family_revoked_response.status_code == 401
    assert family_revoked_response.json()["error"]["code"] == "REFRESH_TOKEN_REUSED"
