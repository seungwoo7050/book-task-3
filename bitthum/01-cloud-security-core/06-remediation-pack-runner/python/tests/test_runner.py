import json
from pathlib import Path

from remediation_pack_runner.runner import approve, build_dry_run


def _finding() -> dict[str, object]:
    path = Path(__file__).resolve().parents[2] / "problem" / "data" / "sample_finding.json"
    return json.loads(path.read_text())


def test_build_dry_run_returns_patch_for_public_access_finding() -> None:
    plan = build_dry_run(_finding())
    assert plan.mode == "auto_patch_available"
    assert any("block_public_acls" in line for line in plan.commands_or_patch)
    assert plan.status == "pending_approval"


def test_approve_marks_plan_approved() -> None:
    plan = approve(build_dry_run(_finding()), "security.lead")
    assert plan.status == "approved"
    assert "security.lead" in plan.summary

