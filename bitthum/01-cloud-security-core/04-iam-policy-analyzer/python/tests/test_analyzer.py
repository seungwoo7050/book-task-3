import json
from pathlib import Path

from iam_policy_analyzer.analyzer import analyze_policy


def _policy(name: str) -> dict[str, object]:
    path = Path(__file__).resolve().parents[2] / "problem" / "data" / name
    return json.loads(path.read_text())


def test_broad_admin_policy_reports_multiple_findings() -> None:
    findings = analyze_policy(_policy("broad_admin_policy.json"))
    controls = {finding.control_id for finding in findings}
    assert controls == {"IAM-001", "IAM-002"}


def test_passrole_policy_reports_escalation_risk() -> None:
    findings = analyze_policy(_policy("passrole_policy.json"))
    assert any(finding.control_id == "IAM-003" for finding in findings)


def test_scoped_policy_reports_no_findings() -> None:
    findings = analyze_policy(_policy("scoped_policy.json"))
    assert findings == []

