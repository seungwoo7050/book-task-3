import json
from pathlib import Path

from cspm_rule_engine.scanner import scan_access_keys, scan_plan


def _data(name: str) -> dict[str, object]:
    path = Path(__file__).resolve().parents[2] / "problem" / "data" / name
    return json.loads(path.read_text())


def test_insecure_plan_reports_expected_findings() -> None:
    findings = scan_plan(_data("insecure_plan.json"))
    controls = {finding.control_id for finding in findings}
    assert controls == {"CSPM-001", "CSPM-002", "CSPM-003"}


def test_secure_plan_reports_no_findings() -> None:
    findings = scan_plan(_data("secure_plan.json"))
    assert findings == []


def test_access_key_snapshot_reports_old_key() -> None:
    findings = scan_access_keys(_data("access_keys_snapshot.json"))
    assert len(findings) == 1
    assert findings[0].control_id == "CSPM-004"

