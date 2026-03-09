from __future__ import annotations

from fastapi.testclient import TestClient


def _latest_mail_token(client: TestClient, kind: str) -> str:
    mailbox = client.app.state.mailbox
    assert mailbox
    messages = [message for message in mailbox if message["kind"] == kind]
    assert messages
    return messages[-1]["token"]


def _register_and_verify(client: TestClient) -> None:
    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "handle": "player-one",
            "email": "player@example.com",
            "password": "super-secret-1",
        },
    )
    assert register_response.status_code == 200

    verify_response = client.post(
        "/api/v1/auth/verify-email",
        json={"token": _latest_mail_token(client, "verify_email")},
    )
    assert verify_response.status_code == 200


def test_local_login_refresh_rotation_and_logout(client: TestClient) -> None:
    _register_and_verify(client)

    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": "player@example.com", "password": "super-secret-1"},
    )
    assert login_response.status_code == 200
    assert client.cookies.get("access_token")
    assert client.cookies.get("refresh_token")
    assert client.cookies.get("csrf_token")

    me_response = client.get("/api/v1/auth/me")
    assert me_response.status_code == 200
    assert me_response.json()["user"]["email_verified"] is True

    original_refresh = client.cookies["refresh_token"]
    csrf_token = client.cookies["csrf_token"]
    refresh_response = client.post(
        "/api/v1/auth/token/refresh",
        headers={"X-CSRF-Token": csrf_token},
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

    family_revoked = client.post(
        "/api/v1/auth/token/refresh",
        headers={"X-CSRF-Token": rotated_csrf},
    )
    assert family_revoked.status_code == 401
    assert family_revoked.json()["error"]["code"] == "REFRESH_TOKEN_REUSED"

    second_login = client.post(
        "/api/v1/auth/login",
        json={"email": "player@example.com", "password": "super-secret-1"},
    )
    assert second_login.status_code == 200
    logout_response = client.post(
        "/api/v1/auth/logout",
        headers={"X-CSRF-Token": client.cookies["csrf_token"]},
    )
    assert logout_response.status_code == 200


def test_password_reset_flow(client: TestClient) -> None:
    _register_and_verify(client)

    request_response = client.post(
        "/api/v1/auth/password-reset/request",
        json={"email": "player@example.com"},
    )
    assert request_response.status_code == 200

    reset_response = client.post(
        "/api/v1/auth/password-reset/confirm",
        json={
            "token": _latest_mail_token(client, "password_reset"),
            "new_password": "even-better-secret-2",
        },
    )
    assert reset_response.status_code == 200

    old_login = client.post(
        "/api/v1/auth/login",
        json={"email": "player@example.com", "password": "super-secret-1"},
    )
    assert old_login.status_code == 401

    new_login = client.post(
        "/api/v1/auth/login",
        json={"email": "player@example.com", "password": "even-better-secret-2"},
    )
    assert new_login.status_code == 200


def test_csrf_rejects_refresh_without_header(client: TestClient) -> None:
    _register_and_verify(client)
    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": "player@example.com", "password": "super-secret-1"},
    )
    assert login_response.status_code == 200

    refresh_response = client.post("/api/v1/auth/token/refresh")
    assert refresh_response.status_code == 403
    assert refresh_response.json()["error"]["code"] == "CSRF_VALIDATION_FAILED"
