from __future__ import annotations

import httpx

from tests.compose_harness import compose_stack


def _latest_token(email: str) -> str:
    response = httpx.get(
        "http://127.0.0.1:8111/api/v1/internal/auth/debug/mailbox/latest",
        params={"email": email},
        timeout=5.0,
    )
    response.raise_for_status()
    return response.json()["token"]


def test_identity_token_then_workspace_creation() -> None:
    with compose_stack():
        identity = httpx.Client(base_url="http://127.0.0.1:8111/api/v1", timeout=10.0)
        workspace = httpx.Client(base_url="http://127.0.0.1:8011/api/v1", timeout=10.0)

        register = identity.post(
            "/internal/auth/register",
            json={"handle": "owner", "email": "owner@example.com", "password": "super-secret-1"},
        )
        assert register.status_code == 200
        verify = identity.post("/internal/auth/verify-email", json={"token": _latest_token("owner@example.com")})
        assert verify.status_code == 200
        login = identity.post("/internal/auth/login", json={"email": "owner@example.com", "password": "super-secret-1"})
        assert login.status_code == 200

        access_token = login.json()["access_token"]
        create_workspace = workspace.post(
            "/internal/workspaces",
            json={"name": "Alpha"},
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert create_workspace.status_code == 200
        assert create_workspace.json()["name"] == "Alpha"
