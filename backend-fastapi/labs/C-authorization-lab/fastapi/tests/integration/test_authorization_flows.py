from __future__ import annotations


def test_invite_accept_promote_and_document_permissions(client) -> None:
    owner = client.post(
        "/api/v1/authorization/users",
        json={"email": "owner@example.com", "name": "Owner"},
    ).json()
    viewer = client.post(
        "/api/v1/authorization/users",
        json={"email": "viewer@example.com", "name": "Viewer"},
    ).json()

    workspace = client.post(
        "/api/v1/authorization/workspaces",
        json={"name": "Platform"},
        headers={"X-User-Id": owner["id"]},
    ).json()

    invite = client.post(
        f"/api/v1/authorization/workspaces/{workspace['id']}/invites",
        json={"email": viewer["email"], "role": "viewer"},
        headers={"X-User-Id": owner["id"]},
    ).json()

    accept = client.post(
        f"/api/v1/authorization/invites/{invite['token']}/accept",
        headers={"X-User-Id": viewer["id"]},
    )
    assert accept.status_code == 200

    forbidden = client.post(
        f"/api/v1/authorization/workspaces/{workspace['id']}/documents",
        json={"title": "Spec"},
        headers={"X-User-Id": viewer["id"]},
    )
    assert forbidden.status_code == 403

    promote = client.patch(
        f"/api/v1/authorization/workspaces/{workspace['id']}/members/{viewer['id']}",
        json={"role": "member"},
        headers={"X-User-Id": owner["id"]},
    )
    assert promote.status_code == 200

    document = client.post(
        f"/api/v1/authorization/workspaces/{workspace['id']}/documents",
        json={"title": "Spec"},
        headers={"X-User-Id": viewer["id"]},
    )
    assert document.status_code == 200


def test_invite_decline_and_outsider_read_forbidden(client) -> None:
    owner = client.post(
        "/api/v1/authorization/users",
        json={"email": "owner2@example.com", "name": "Owner 2"},
    ).json()
    invitee = client.post(
        "/api/v1/authorization/users",
        json={"email": "invitee@example.com", "name": "Invitee"},
    ).json()
    outsider = client.post(
        "/api/v1/authorization/users",
        json={"email": "outsider@example.com", "name": "Outsider"},
    ).json()

    workspace = client.post(
        "/api/v1/authorization/workspaces",
        json={"name": "Infra"},
        headers={"X-User-Id": owner["id"]},
    ).json()
    document = client.post(
        f"/api/v1/authorization/workspaces/{workspace['id']}/documents",
        json={"title": "Runbook"},
        headers={"X-User-Id": owner["id"]},
    ).json()

    invite = client.post(
        f"/api/v1/authorization/workspaces/{workspace['id']}/invites",
        json={"email": invitee["email"], "role": "viewer"},
        headers={"X-User-Id": owner["id"]},
    ).json()
    decline = client.post(
        f"/api/v1/authorization/invites/{invite['token']}/decline",
        headers={"X-User-Id": invitee["id"]},
    )
    assert decline.status_code == 200
    assert decline.json()["status"] == "declined"

    outsider_read = client.get(
        f"/api/v1/authorization/documents/{document['id']}",
        headers={"X-User-Id": outsider["id"]},
    )
    assert outsider_read.status_code == 403
