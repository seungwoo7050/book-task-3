from __future__ import annotations

from datetime import UTC, datetime, timedelta

import httpx
import jwt

from tests.compose_harness import compose_stack


def _token(user_id: str, handle: str, email: str) -> str:
    issued_at = datetime.now(UTC)
    payload = {
        "sub": user_id,
        "handle": handle,
        "email": email,
        "display_name": handle,
        "type": "access",
        "iss": "i-event-integration",
        "iat": int(issued_at.timestamp()),
        "exp": int((issued_at + timedelta(minutes=30)).timestamp()),
    }
    return jwt.encode(payload, "i-event-integration-secret-key", algorithm="HS256")


def test_outbox_and_idempotent_consumer_flow() -> None:
    with compose_stack():
        owner_token = _token("00000000-0000-4000-8000-000000000011", "owner", "owner@example.com")
        collaborator_token = _token("00000000-0000-4000-8000-000000000012", "collab", "collab@example.com")
        workspace = httpx.Client(base_url="http://127.0.0.1:8012/api/v1", timeout=10.0)
        notifications = httpx.Client(base_url="http://127.0.0.1:8112/api/v1", timeout=10.0)

        created_workspace = workspace.post(
            "/internal/workspaces",
            json={"name": "Alpha"},
            headers={"Authorization": f"Bearer {owner_token}"},
        ).json()
        invite = workspace.post(
            f"/internal/workspaces/{created_workspace['id']}/invites",
            json={"email": "collab@example.com", "role": "member"},
            headers={"Authorization": f"Bearer {owner_token}"},
        ).json()
        accept = workspace.post(
            f"/internal/invites/{invite['token']}/accept",
            headers={"Authorization": f"Bearer {collaborator_token}"},
        )
        assert accept.status_code == 200

        project = workspace.post(
            f"/internal/workspaces/{created_workspace['id']}/projects",
            json={"title": "Platform API"},
            headers={"Authorization": f"Bearer {owner_token}"},
        ).json()
        task = workspace.post(
            f"/internal/projects/{project['id']}/tasks",
            json={"title": "Ship comments"},
            headers={"Authorization": f"Bearer {owner_token}"},
        ).json()
        comment = workspace.post(
            f"/internal/tasks/{task['id']}/comments",
            json={"body": "Please review the API contract."},
            headers={"Authorization": f"Bearer {owner_token}"},
        )
        assert comment.status_code == 200
        assert workspace.get("/internal/debug/outbox/pending").json()["pending"] == 1

        relay = workspace.post("/internal/events/relay")
        assert relay.status_code == 200
        first_consume = notifications.post("/internal/notifications/consume")
        second_consume = notifications.post("/internal/notifications/consume")
        assert first_consume.json()["processed"] == 1
        assert second_consume.json()["processed"] == 0

        saved = notifications.get("/internal/notifications/users/00000000-0000-4000-8000-000000000012").json()
        assert len(saved) == 1
        assert saved[0]["message"].startswith("New comment on task")
