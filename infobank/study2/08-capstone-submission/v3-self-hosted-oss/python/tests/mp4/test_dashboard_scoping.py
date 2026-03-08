from __future__ import annotations

import io
import zipfile
from pathlib import Path

from fastapi.testclient import TestClient
from services.jobs import run_job


def _bundle_payload() -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        archive.writestr("docs/policies/refund.md", "# Refund\n환불은 본인확인 후 확인해야 합니다.\n")
        archive.writestr("docs/policies/escalation.md", "# Escalation\n분쟁 이슈는 전문 부서 이관이 필요합니다.\n")
    return buffer.getvalue()


def _seed_run(auth_client: TestClient, temp_jsonl: Path, run_label: str) -> dict[str, object]:
    with temp_jsonl.open("rb") as handle:
        dataset_response = auth_client.post(
            "/api/datasets/import",
            files={"file": ("support.jsonl", handle, "application/x-ndjson")},
            data={"name": f"dataset-{run_label}"},
        )
    bundle_response = auth_client.post(
        "/api/kb-bundles/import",
        files={"file": ("kb.zip", io.BytesIO(_bundle_payload()), "application/zip")},
        data={"name": f"kb-{run_label}"},
    )
    job_response = auth_client.post(
        "/api/jobs",
        json={
            "dataset_id": dataset_response.json()["dataset_id"],
            "kb_bundle_id": bundle_response.json()["kb_bundle_id"],
            "run_label": run_label,
            "retrieval_version": "retrieval-v2",
        },
    )
    job = job_response.json()["job"]
    run_job(job["id"])
    return job


def test_dashboard_and_session_review_are_scoped_by_job(auth_client: TestClient, temp_jsonl: Path) -> None:
    job = _seed_run(auth_client, temp_jsonl, "scoped-run")

    overview = auth_client.get(f"/api/dashboard/overview?job_id={job['id']}")
    failures = auth_client.get(f"/api/dashboard/failures?job_id={job['id']}")
    conversations = auth_client.get(f"/api/conversations?job_id={job['id']}")

    assert overview.status_code == 200
    assert failures.status_code == 200
    assert conversations.status_code == 200

    overview_payload = overview.json()
    assert overview_payload["selected_job_id"] == job["id"]
    assert overview_payload["selected_run_id"] == job["run_id"]
    assert overview_payload["evaluation_count"] == 2

    conversation_items = conversations.json()["items"]
    assert len(conversation_items) == 2

    detail = auth_client.get(
        f"/api/conversations/{conversation_items[0]['id']}?job_id={job['id']}"
    )
    assert detail.status_code == 200
    turns = detail.json()["turns"]
    assert turns[0]["evaluation"] is not None
    assert turns[0]["evaluation"]["lineage"]["run_id"] == job["run_id"]
