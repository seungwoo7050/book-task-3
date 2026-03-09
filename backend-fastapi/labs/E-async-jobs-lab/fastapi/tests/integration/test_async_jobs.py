from __future__ import annotations


def test_idempotent_enqueue_and_outbox_drain(client) -> None:
    first = client.post(
        "/api/v1/jobs/notifications",
        json={"recipient": "team@example.com", "subject": "Deploy finished"},
        headers={"Idempotency-Key": "job-1"},
    )
    second = client.post(
        "/api/v1/jobs/notifications",
        json={"recipient": "team@example.com", "subject": "Deploy finished"},
        headers={"Idempotency-Key": "job-1"},
    )
    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json()["id"] == second.json()["id"]

    drain = client.post("/api/v1/jobs/outbox/drain")
    assert drain.status_code == 200
    assert drain.json()["processed"] == 1

    job = client.get(f"/api/v1/jobs/notifications/{first.json()['id']}")
    assert job.status_code == 200
    assert job.json()["status"] == "sent"


def test_retrying_job_requires_second_drain(client) -> None:
    job = client.post(
        "/api/v1/jobs/notifications",
        json={"recipient": "retry@example.com", "subject": "Retry me"},
        headers={"Idempotency-Key": "job-2"},
    )
    assert job.status_code == 200

    first_drain = client.post("/api/v1/jobs/outbox/drain")
    assert first_drain.status_code == 200
    first_job = client.get(f"/api/v1/jobs/notifications/{job.json()['id']}")
    assert first_job.json()["status"] == "retrying"

    second_drain = client.post("/api/v1/jobs/outbox/drain")
    assert second_drain.status_code == 200
    second_job = client.get(f"/api/v1/jobs/notifications/{job.json()['id']}")
    assert second_job.json()["status"] == "sent"
    assert second_job.json()["attempt_count"] == 2
