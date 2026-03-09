from __future__ import annotations

from urllib.parse import parse_qs, urlparse

import pyotp
from fastapi.testclient import TestClient

from app.domain.services.google_oidc import GoogleOIDCService


def _mock_google(monkeypatch, *, subject: str, email: str, name: str) -> None:
    def fake_exchange(self: GoogleOIDCService, code: str, code_verifier: str) -> dict[str, object]:
        return {"access_token": f"token-for-{code}", "id_token": f"id-for-{code}"}

    def fake_validate(self: GoogleOIDCService, id_token: str, nonce: str) -> dict[str, object]:
        return {"sub": subject, "email": email, "email_verified": True, "name": name}

    def fake_userinfo(self: GoogleOIDCService, access_token: str) -> dict[str, object]:
        return {"picture": "https://example.com/avatar.png"}

    monkeypatch.setattr(GoogleOIDCService, "exchange_code_for_tokens", fake_exchange)
    monkeypatch.setattr(GoogleOIDCService, "validate_id_token", fake_validate)
    monkeypatch.setattr(GoogleOIDCService, "fetch_userinfo", fake_userinfo)


def _complete_google_login(client: TestClient) -> None:
    login_response = client.get("/api/v1/auth/google/login")
    state = parse_qs(urlparse(login_response.json()["authorization_url"]).query)["state"][0]
    callback_response = client.get(
        "/api/v1/auth/google/callback",
        params={"code": "oidc-code", "state": state},
    )
    assert callback_response.status_code == 200


def test_two_factor_setup_and_recovery_code_login(client: TestClient, monkeypatch) -> None:
    _mock_google(
        monkeypatch, subject="google-subject-2", email="twofa@example.com", name="Two Factor"
    )
    _complete_google_login(client)

    csrf_token = client.cookies["csrf_token"]
    setup_response = client.post("/api/v1/auth/2fa/setup", headers={"X-CSRF-Token": csrf_token})
    assert setup_response.status_code == 200
    secret = setup_response.json()["secret"]

    confirm_response = client.post(
        "/api/v1/auth/2fa/confirm",
        json={"code": pyotp.TOTP(secret).now()},
        headers={"X-CSRF-Token": csrf_token},
    )
    assert confirm_response.status_code == 200
    recovery_codes = confirm_response.json()["recovery_codes"]
    assert len(recovery_codes) == 8

    _complete_google_login(client)
    assert client.get("/api/v1/auth/me").status_code == 401

    challenge_csrf = client.cookies["csrf_token"]
    verify_response = client.post(
        "/api/v1/auth/2fa/verify",
        json={"recovery_code": recovery_codes[0]},
        headers={"X-CSRF-Token": challenge_csrf},
    )
    assert verify_response.status_code == 200
    assert verify_response.json()["status"] == "authenticated"
    assert client.get("/api/v1/auth/me").status_code == 200
