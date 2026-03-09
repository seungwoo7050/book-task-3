from __future__ import annotations

from fastapi.testclient import TestClient


def _latest_token(client: TestClient) -> str:
    return client.app.state.mailbox[-1]["token"]


def test_local_auth_workspace_flow_and_google_member_notification(app_client: TestClient) -> None:
    owner = app_client
    register = owner.post(
        "/api/v1/auth/register",
        json={"handle": "owner", "email": "owner@example.com", "password": "super-secret-1"},
    )
    assert register.status_code == 200
    verify = owner.post("/api/v1/auth/verify-email", json={"token": _latest_token(owner)})
    assert verify.status_code == 200
    login = owner.post(
        "/api/v1/auth/login",
        json={"email": "owner@example.com", "password": "super-secret-1"},
    )
    assert login.status_code == 200

    collaborator = TestClient(owner.app)
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

    with collaborator.websocket_connect(f"/api/v1/platform/ws/notifications?access_token={access_token}") as websocket:
        project = owner.post(
            f"/api/v1/platform/workspaces/{workspace['id']}/projects",
            json={"title": "Platform API"},
        ).json()
        task = owner.post(
            f"/api/v1/platform/projects/{project['id']}/tasks",
            json={"title": "Ship comments"},
        ).json()
        comment = owner.post(
            f"/api/v1/platform/tasks/{task['id']}/comments",
            json={"body": "Please review the API contract."},
        )
        assert comment.status_code == 200

        drain = owner.post("/api/v1/platform/notifications/drain")
        assert drain.status_code == 200
        assert websocket.receive_json()["message"].startswith("New comment on task")

    me = collaborator.get("/api/v1/auth/me")
    assert me.status_code == 200
    assert me.json()["user"]["email"] == "collab@example.com"
