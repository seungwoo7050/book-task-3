from __future__ import annotations

import json
import os
import shutil
from datetime import datetime, timedelta, timezone
from pathlib import Path

from fastapi.testclient import TestClient

from cloud_security_control_plane.app import create_app
from cloud_security_control_plane import db


def main() -> None:
    project_root = Path(__file__).resolve().parents[3]
    asset_dir = project_root / ".artifacts" / "capstone" / "demo"
    asset_dir.mkdir(parents=True, exist_ok=True)

    database_url = os.environ.get("DATABASE_URL")
    lake_dir = os.environ.get("CONTROL_PLANE_LAKE_DIR")
    app = create_app(database_url=database_url, lake_dir=lake_dir)
    if app.state.lake_dir.exists():
        shutil.rmtree(app.state.lake_dir)
    with app.state.session_factory() as session:
        db.reset_state(session)
        session.commit()
    client = TestClient(app)

    data_dir = project_root / "problem" / "data"

    scan_responses: list[dict[str, object]] = []
    scan_responses.append(client.post("/v1/scans", json={"source": "terraform-plan", "path": str(data_dir / "insecure_plan.json")}).json())
    scan_responses.append(client.post("/v1/scans", json={"source": "iam-policy", "path": str(data_dir / "broad_admin_policy.json")}).json())
    worker_response = client.post("/v1/workers/scans/run").json()
    cloudtrail_response = client.post("/v1/ingestions/cloudtrail", json={"path": str(data_dir / "cloudtrail_suspicious.json")}).json()
    k8s_response = client.post("/v1/ingestions/k8s", json={"path": str(data_dir / "insecure_k8s.yaml")}).json()
    findings_response = client.get("/v1/findings").json()

    findings = findings_response["findings"]
    first_finding_id = findings[0]["id"]
    second_finding_id = findings[1]["id"]

    exception_response = client.post(
        "/v1/exceptions",
        json={
            "scope_type": "finding",
            "scope_id": first_finding_id,
            "reason": "Temporary business exception for demo",
            "expires_at": (datetime.now(timezone.utc) + timedelta(days=7)).isoformat(),
            "approved_by": "security.manager",
        },
    ).json()
    remediation_response = client.post(f"/v1/remediations/{second_finding_id}/dry-run").json()
    report_response = client.get("/v1/reports/latest").json()

    (asset_dir / "01-scan-requests.json").write_text(json.dumps(scan_responses, indent=2))
    (asset_dir / "02-worker-response.json").write_text(json.dumps(worker_response, indent=2))
    (asset_dir / "03-cloudtrail-response.json").write_text(json.dumps(cloudtrail_response, indent=2))
    (asset_dir / "04-k8s-response.json").write_text(json.dumps(k8s_response, indent=2))
    (asset_dir / "05-findings.json").write_text(json.dumps(findings_response, indent=2))
    (asset_dir / "06-exception.json").write_text(json.dumps(exception_response, indent=2))
    (asset_dir / "07-remediation.json").write_text(json.dumps(remediation_response, indent=2))
    (asset_dir / "08-report.md").write_text(report_response["markdown"])

    print(f"demo assets written to {asset_dir}")


if __name__ == "__main__":
    main()
