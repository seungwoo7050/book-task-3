from __future__ import annotations

import io
import json
import zipfile
from pathlib import Path

from fastapi.testclient import TestClient


def _build_kb_zip(with_manifest: bool) -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        archive.writestr(
            "docs/policies/refund.md",
            "# Refund\n환불은 본인확인 후 접수 상태와 처리 일정을 확인해야 합니다.\n",
        )
        archive.writestr(
            "docs/procedures/verification.md",
            "# Verification\n환불이나 해지 전에는 본인확인 절차가 필요합니다.\n",
        )
        if with_manifest:
            archive.writestr(
                "manifest.json",
                json.dumps(
                    {
                        "docs": {
                            "docs/policies/refund.md": {
                                "title": "Refund Policy",
                                "category": "policies",
                                "aliases": ["환불", "환불 접수"],
                                "keywords": ["영업일", "본인확인"],
                                "risk_tags": ["policy"],
                            }
                        }
                    }
                ),
            )
    return buffer.getvalue()


def test_dataset_import_contract_returns_record_count(auth_client: TestClient, temp_jsonl: Path) -> None:
    with temp_jsonl.open("rb") as handle:
        response = auth_client.post(
            "/api/datasets/import",
            files={"file": ("support.jsonl", handle, "application/x-ndjson")},
            data={"name": "imported-support"},
        )

    assert response.status_code == 200
    payload = response.json()
    assert payload["record_count"] == 2
    assert payload["warnings"] == []
    assert isinstance(payload["dataset_id"], str)


def test_dataset_import_validation_surfaces_line_errors(auth_client: TestClient, tmp_path: Path) -> None:
    bad_path = tmp_path / "bad.jsonl"
    bad_path.write_text('{"conversation_external_id":"conv-a","turn_index":"x"}\n', encoding="utf-8")

    with bad_path.open("rb") as handle:
        response = auth_client.post(
            "/api/datasets/import",
            files={"file": ("bad.jsonl", handle, "application/x-ndjson")},
        )

    assert response.status_code == 422
    detail = response.json()["detail"]
    assert detail["errors"][0]["line"] == 1


def test_kb_bundle_import_supports_manifest_and_derived_categories(auth_client: TestClient) -> None:
    response = auth_client.post(
        "/api/kb-bundles/import",
        files={"file": ("kb.zip", io.BytesIO(_build_kb_zip(with_manifest=True)), "application/zip")},
        data={"name": "support-kb"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["doc_count"] == 2
    assert "policies" in payload["derived_categories"]


def test_kb_bundle_import_without_manifest_still_indexes_markdown(auth_client: TestClient) -> None:
    response = auth_client.post(
        "/api/kb-bundles/import",
        files={"file": ("kb-no-manifest.zip", io.BytesIO(_build_kb_zip(with_manifest=False)), "application/zip")},
        data={"name": "support-kb-no-manifest"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["doc_count"] == 2
    assert set(payload["derived_categories"]) >= {"policies", "procedures"}
