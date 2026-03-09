from __future__ import annotations

from urllib.parse import parse_qs, urlparse

from fastapi.testclient import TestClient

from app.domain.services.google_oidc import GoogleOIDCService


def test_google_callback_creates_user_and_session(client: TestClient, monkeypatch) -> None:
    def fake_exchange(self: GoogleOIDCService, code: str, code_verifier: str) -> dict[str, object]:
        assert code == "sample-code"
        assert code_verifier
        return {"access_token": "google-access", "id_token": "google-id"}

    def fake_validate(self: GoogleOIDCService, id_token: str, nonce: str) -> dict[str, object]:
        assert id_token == "google-id"
        assert nonce
        return {
            "sub": "google-subject-1",
            "email": "pong@example.com",
            "email_verified": True,
            "name": "Pong User",
        }

    def fake_userinfo(self: GoogleOIDCService, access_token: str) -> dict[str, object]:
        assert access_token == "google-access"
        return {"picture": "https://example.com/avatar.png"}

    monkeypatch.setattr(GoogleOIDCService, "exchange_code_for_tokens", fake_exchange)
    monkeypatch.setattr(GoogleOIDCService, "validate_id_token", fake_validate)
    monkeypatch.setattr(GoogleOIDCService, "fetch_userinfo", fake_userinfo)

    login_response = client.get("/api/v1/auth/google/login")
    assert login_response.status_code == 200

    authorization_url = login_response.json()["authorization_url"]
    state = parse_qs(urlparse(authorization_url).query)["state"][0]

    callback_response = client.get(
        "/api/v1/auth/google/callback",
        params={"code": "sample-code", "state": state},
    )

    assert callback_response.status_code == 200
    payload = callback_response.json()
    assert payload["status"] == "authenticated"
    assert payload["user"]["email"] == "pong@example.com"
    assert client.cookies.get("access_token")
    assert client.cookies.get("refresh_token")
    assert client.cookies.get("csrf_token")

    me_response = client.get("/api/v1/auth/me")
    assert me_response.status_code == 200
    assert me_response.json()["user"]["handle"] == "pong"
