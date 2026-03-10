from __future__ import annotations

import subprocess

import httpx
from websockets.sync.client import connect

from tests.compose_harness import ROOT, compose_stack, wait_for


def _latest_token(email: str) -> str:
    response = httpx.get(
        "http://127.0.0.1:8115/api/v1/internal/auth/debug/mailbox/latest",
        params={"email": email},
        timeout=5.0,
    )
    response.raise_for_status()
    return response.json()["token"]


def test_v2_system_flow_and_notification_recovery() -> None:
    with compose_stack() as project_name:
        owner = httpx.Client(base_url="http://127.0.0.1:8015", timeout=10.0)
        collaborator = httpx.Client(base_url="http://127.0.0.1:8015", timeout=10.0)

        register = owner.post(
            "/api/v1/auth/register",
            json={"handle": "owner", "email": "owner@example.com", "password": "super-secret-1"},
        )
        assert register.status_code == 200
        verify = owner.post("/api/v1/auth/verify-email", json={"token": _latest_token("owner@example.com")})
        assert verify.status_code == 200
        login = owner.post("/api/v1/auth/login", json={"email": "owner@example.com", "password": "super-secret-1"})
        assert login.status_code == 200

        google_login = collaborator.post(
            "/api/v1/auth/google/login",
            json={"subject": "google-123", "email": "collab@example.com", "display_name": "Collab"},
        )
        assert google_login.status_code == 200
        access_token = collaborator.cookies["access_token"]

        workspace = owner.post("/api/v1/platform/workspaces", json={"name": "Alpha"}).json()
        invite = owner.post(
            f"/api/v1/platform/workspaces/{workspace['id']}/invites",
            json={"email": "collab@example.com", "role": "member"},
        ).json()
        accept = collaborator.post(f"/api/v1/platform/invites/{invite['token']}/accept")
        assert accept.status_code == 200

        with connect(f"ws://127.0.0.1:8015/api/v1/platform/ws/notifications?access_token={access_token}") as websocket:
            project = owner.post(
                f"/api/v1/platform/workspaces/{workspace['id']}/projects",
                json={"title": "Platform API"},
            ).json()
            task = owner.post(
                f"/api/v1/platform/projects/{project['id']}/tasks",
                json={"title": "Ship comments"},
            ).json()

            first_comment = owner.post(
                f"/api/v1/platform/tasks/{task['id']}/comments",
                json={"body": "Please review the API contract."},
            )
            assert first_comment.status_code == 200
            first_drain = owner.post("/api/v1/platform/notifications/drain")
            assert first_drain.status_code == 200
            assert "New comment on task" in websocket.recv(timeout=20)

            subprocess.run(
                ["docker", "compose", "-p", project_name, "-f", "compose.yaml", "stop", "notification-service"],
                cwd=ROOT,
                check=True,
            )

            second_comment = owner.post(
                f"/api/v1/platform/tasks/{task['id']}/comments",
                json={"body": "Second comment after consumer outage."},
            )
            assert second_comment.status_code == 200
            failed_drain = owner.post("/api/v1/platform/notifications/drain")
            assert failed_drain.status_code == 503

            subprocess.run(
                ["docker", "compose", "-p", project_name, "-f", "compose.yaml", "start", "notification-service"],
                cwd=ROOT,
                check=True,
            )
            wait_for("http://127.0.0.1:8117/api/v1/health/ready")

            recovery_drain = owner.post("/api/v1/platform/notifications/drain")
            assert recovery_drain.status_code == 200
            assert "Second comment after consumer outage." in websocket.recv(timeout=20)
