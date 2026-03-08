from datetime import datetime, timedelta, timezone
from pathlib import Path

from fastapi.testclient import TestClient

from cloud_security_control_plane.app import create_app


def _data(name: str) -> str:
    return str(Path(__file__).resolve().parents[2] / "problem" / "data" / name)


def test_control_plane_end_to_end(tmp_path: Path) -> None:
    db_url = f"sqlite+pysqlite:///{tmp_path / 'control-plane.sqlite3'}"
    lake_dir = tmp_path / "lake"
    client = TestClient(create_app(database_url=db_url, lake_dir=str(lake_dir)))

    terraform_job = client.post("/v1/scans", json={"source": "terraform-plan", "path": _data("insecure_plan.json")})
    iam_job = client.post("/v1/scans", json={"source": "iam-policy", "path": _data("broad_admin_policy.json")})
    assert terraform_job.status_code == 200
    assert iam_job.status_code == 200

    worker = client.post("/v1/workers/scans/run")
    assert worker.status_code == 200
    assert worker.json()["processed_jobs"] == 2

    cloudtrail = client.post("/v1/ingestions/cloudtrail", json={"path": _data("cloudtrail_suspicious.json")})
    k8s = client.post("/v1/ingestions/k8s", json={"path": _data("insecure_k8s.yaml")})
    assert cloudtrail.json()["finding_count"] >= 1
    assert k8s.json()["finding_count"] >= 1

    findings_response = client.get("/v1/findings")
    findings = findings_response.json()["findings"]
    assert len(findings) >= 6

    first_finding_id = findings[0]["id"]
    exception_response = client.post(
        "/v1/exceptions",
        json={
            "scope_type": "finding",
            "scope_id": first_finding_id,
            "reason": "Temporary exception",
            "expires_at": (datetime.now(timezone.utc) + timedelta(days=7)).isoformat(),
            "approved_by": "security.manager",
        },
    )
    assert exception_response.status_code == 200

    suppressed = client.get("/v1/findings").json()["findings"]
    assert any(item["id"] == first_finding_id and item["status"] == "suppressed" for item in suppressed)

    target_finding_id = next(item["id"] for item in suppressed if item["id"] != first_finding_id)
    remediation = client.post(f"/v1/remediations/{target_finding_id}/dry-run")
    assert remediation.status_code == 200
    assert remediation.json()["remediation"]["finding_id"] == target_finding_id

    report = client.get("/v1/reports/latest")
    assert report.status_code == 200
    assert "## Findings" in report.json()["markdown"]
    assert (lake_dir / "events.parquet").exists()

