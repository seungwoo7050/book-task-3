from __future__ import annotations

import io
import zipfile
from pathlib import Path

import pytest
from core.errors import DependencyUnavailableError
from fastapi.testclient import TestClient
from services.jobs import run_job


def _create_bundle_payload() -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        archive.writestr("docs/policies/refund.md", "# Refund\n환불은 본인확인 후 확인해야 합니다.\n")
        archive.writestr("docs/policies/escalation.md", "# Escalation\n분쟁 이슈는 전문 부서 이관이 필요합니다.\n")
    return buffer.getvalue()


def _import_dataset(auth_client: TestClient, temp_jsonl: Path) -> str:
    with temp_jsonl.open("rb") as handle:
        response = auth_client.post(
            "/api/datasets/import",
            files={"file": ("support.jsonl", handle, "application/x-ndjson")},
            data={"name": "uploaded-dataset"},
        )
    assert response.status_code == 200
    return response.json()["dataset_id"]


def _import_bundle(auth_client: TestClient) -> str:
    response = auth_client.post(
        "/api/kb-bundles/import",
        files={"file": ("kb.zip", io.BytesIO(_create_bundle_payload()), "application/zip")},
        data={"name": "uploaded-kb"},
    )
    assert response.status_code == 200
    return response.json()["kb_bundle_id"]


def test_job_lifecycle_completes_and_writes_run_scoped_results(auth_client: TestClient, temp_jsonl: Path) -> None:
    dataset_id = _import_dataset(auth_client, temp_jsonl)
    bundle_id = _import_bundle(auth_client)

    create_response = auth_client.post(
        "/api/jobs",
        json={
            "dataset_id": dataset_id,
            "kb_bundle_id": bundle_id,
            "run_label": "candidate-run",
            "retrieval_version": "retrieval-v2",
        },
    )
    assert create_response.status_code == 200
    job = create_response.json()["job"]

    run_job(job["id"])

    status_response = auth_client.get(f"/api/jobs/{job['id']}")
    assert status_response.status_code == 200
    payload = status_response.json()["job"]
    assert payload["status"] == "completed"
    assert payload["progress_completed"] == payload["progress_total"] == 2
    assert payload["run_label"] == "candidate-run"
    assert payload["evaluation_count"] == 2


def test_job_failure_path_marks_status_failed(
    auth_client: TestClient,
    temp_jsonl: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    dataset_id = _import_dataset(auth_client, temp_jsonl)
    bundle_id = _import_bundle(auth_client)

    create_response = auth_client.post(
        "/api/jobs",
        json={"dataset_id": dataset_id, "kb_bundle_id": bundle_id, "run_label": "failing-run"},
    )
    assert create_response.status_code == 200
    job = create_response.json()["job"]

    def _boom(*args: object, **kwargs: object) -> object:
        raise DependencyUnavailableError("provider", "synthetic provider outage")

    monkeypatch.setattr("services.jobs.EvaluationPipeline.evaluate_turn", _boom)

    run_job(job["id"])

    status_response = auth_client.get(f"/api/jobs/{job['id']}")
    assert status_response.status_code == 200
    payload = status_response.json()["job"]
    assert payload["status"] == "failed"
    assert "synthetic provider outage" in payload["error_summary"]
