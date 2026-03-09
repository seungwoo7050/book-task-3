from __future__ import annotations


def test_filter_sort_pagination_and_soft_delete(client) -> None:
    client.post("/api/v1/data/projects", json={"title": "Alpha", "status": "active"})
    client.post("/api/v1/data/projects", json={"title": "Gamma", "status": "archived"})
    beta = client.post("/api/v1/data/projects", json={"title": "Beta", "status": "active"}).json()

    filtered = client.get(
        "/api/v1/data/projects",
        params={"status": "active", "sort": "title", "page": 1, "page_size": 1},
    )
    assert filtered.status_code == 200
    payload = filtered.json()
    assert payload["total"] == 2
    assert len(payload["items"]) == 1
    assert payload["items"][0]["title"] == "Alpha"

    deleted = client.delete(f"/api/v1/data/projects/{beta['id']}")
    assert deleted.status_code == 200

    after_delete = client.get("/api/v1/data/projects", params={"status": "active"})
    titles = [item["title"] for item in after_delete.json()["items"]]
    assert titles == ["Alpha"]

    with_deleted = client.get(
        "/api/v1/data/projects",
        params={"include_deleted": "true", "sort": "-title"},
    )
    assert with_deleted.status_code == 200
    assert {item["title"] for item in with_deleted.json()["items"]} >= {"Alpha", "Beta", "Gamma"}


def test_optimistic_locking_and_task_comment_creation(client) -> None:
    project = client.post(
        "/api/v1/data/projects",
        json={"title": "Roadmap", "status": "active"},
    ).json()

    update = client.patch(
        f"/api/v1/data/projects/{project['id']}",
        json={"version": project["version"], "title": "Roadmap v2"},
    )
    assert update.status_code == 200
    assert update.json()["version"] == 2

    stale = client.patch(
        f"/api/v1/data/projects/{project['id']}",
        json={"version": 1, "status": "archived"},
    )
    assert stale.status_code == 409

    task = client.post(
        f"/api/v1/data/projects/{project['id']}/tasks",
        json={"title": "Ship API", "status": "todo", "priority": 1},
    )
    assert task.status_code == 200

    comment = client.post(
        f"/api/v1/data/tasks/{task.json()['id']}/comments",
        json={"body": "Need pagination semantics in the README."},
    )
    assert comment.status_code == 200
