from __future__ import annotations

import io
import zipfile
from pathlib import Path

from fastapi.testclient import TestClient
from services.jobs import run_job


def _bundle_payload() -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        archive.writestr("docs/policies/refund.md", "# Refund\n환불은 본인확인 후 접수 상태를 확인해야 합니다.\n")
        archive.writestr("docs/procedures/verification.md", "# Verification\n환불 전에는 본인확인이 필요합니다.\n")
    return buffer.getvalue()


def test_version_compare_supports_imported_run_labels(auth_client: TestClient, temp_jsonl: Path) -> None:
    with temp_jsonl.open("rb") as handle:
        dataset_response = auth_client.post(
            "/api/datasets/import",
            files={"file": ("shared.jsonl", handle, "application/x-ndjson")},
            data={"name": "shared-dataset"},
        )
    bundle_response = auth_client.post(
        "/api/kb-bundles/import",
        files={"file": ("shared-kb.zip", io.BytesIO(_bundle_payload()), "application/zip")},
        data={"name": "shared-kb"},
    )

    dataset_id = dataset_response.json()["dataset_id"]
    bundle_id = bundle_response.json()["kb_bundle_id"]

    baseline_job = auth_client.post(
        "/api/jobs",
        json={
            "dataset_id": dataset_id,
            "kb_bundle_id": bundle_id,
            "run_label": "baseline-run",
            "retrieval_version": "retrieval-v1",
        },
    ).json()["job"]
    candidate_job = auth_client.post(
        "/api/jobs",
        json={
            "dataset_id": dataset_id,
            "kb_bundle_id": bundle_id,
            "run_label": "candidate-run",
            "retrieval_version": "retrieval-v2",
            "baseline_label": "baseline-run",
            "candidate_label": "candidate-run",
        },
    ).json()["job"]

    run_job(baseline_job["id"])
    run_job(candidate_job["id"])

    compare = auth_client.get(
        "/api/dashboard/version-compare?baseline=baseline-run&candidate=candidate-run&dataset=shared-dataset"
    )
    assert compare.status_code == 200
    result = compare.json()["result"]
    assert result["baseline"] == "baseline-run"
    assert result["candidate"] == "candidate-run"
    assert result["dataset"] == "shared-dataset"
    assert result["baseline_pass_count"] >= 0
    assert result["candidate_failures"] == result["candidate_failures"]
