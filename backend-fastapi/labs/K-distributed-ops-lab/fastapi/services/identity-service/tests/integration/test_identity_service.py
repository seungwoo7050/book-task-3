from __future__ import annotations


def test_register_verify_login_and_refresh(client) -> None:
    register = client.post(
        "/api/v1/internal/auth/register",
        json={"handle": "owner", "email": "owner@example.com", "password": "super-secret-1"},
    )
    assert register.status_code == 200

    token = client.get(
        "/api/v1/internal/auth/debug/mailbox/latest",
        params={"email": "owner@example.com"},
    ).json()["token"]
    verify = client.post("/api/v1/internal/auth/verify-email", json={"token": token})
    assert verify.status_code == 200

    login = client.post(
        "/api/v1/internal/auth/login",
        json={"email": "owner@example.com", "password": "super-secret-1"},
    )
    assert login.status_code == 200
    refresh = client.post(
        "/api/v1/internal/auth/refresh",
        json={"refresh_token": login.json()["refresh_token"]},
    )
    assert refresh.status_code == 200
