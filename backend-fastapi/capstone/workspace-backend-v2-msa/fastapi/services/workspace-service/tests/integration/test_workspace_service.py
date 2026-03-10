from __future__ import annotations

from app.core.config import Settings
from app.core.security import build_access_token


def _token(user_id: str, handle: str, email: str, settings: Settings) -> str:
    return build_access_token(user_id, handle, email, handle, settings)


def test_workspace_project_comment_outbox_flow(client) -> None:
    settings = Settings(secret_key="workspace-service-test-secret", token_issuer="workspace-service-test")
    owner_token = _token("00000000-0000-4000-8000-000000000001", "owner", "owner@example.com", settings)
    collaborator_token = _token("00000000-0000-4000-8000-000000000002", "collab", "collab@example.com", settings)

    workspace = client.post(
        "/api/v1/internal/workspaces",
        json={"name": "Alpha"},
        headers={"Authorization": f"Bearer {owner_token}"},
    ).json()
    invite = client.post(
        f"/api/v1/internal/workspaces/{workspace['id']}/invites",
        json={"email": "collab@example.com", "role": "member"},
        headers={"Authorization": f"Bearer {owner_token}"},
    ).json()
    accept = client.post(
        f"/api/v1/internal/invites/{invite['token']}/accept",
        headers={"Authorization": f"Bearer {collaborator_token}"},
    )
    assert accept.status_code == 200

    project = client.post(
        f"/api/v1/internal/workspaces/{workspace['id']}/projects",
        json={"title": "Platform API"},
        headers={"Authorization": f"Bearer {owner_token}"},
    ).json()
    task = client.post(
        f"/api/v1/internal/projects/{project['id']}/tasks",
        json={"title": "Ship comments"},
        headers={"Authorization": f"Bearer {owner_token}"},
    ).json()
    comment = client.post(
        f"/api/v1/internal/tasks/{task['id']}/comments",
        json={"body": "Please review the API contract."},
        headers={"Authorization": f"Bearer {owner_token}"},
    )
    assert comment.status_code == 200
    pending = client.get("/api/v1/internal/debug/outbox/pending")
    assert pending.json()["pending"] == 1
