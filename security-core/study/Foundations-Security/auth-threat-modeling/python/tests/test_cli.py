from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from auth_threat_modeling.cli import app

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "problem" / "data"
RUNNER = CliRunner()


def test_check_scenarios_cli_emits_deterministic_summary() -> None:
    result = RUNNER.invoke(app, ["check-scenarios", str(DATA_DIR / "scenario_bundle.json")])
    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["manifest"] == "scenario_bundle.json"
    assert payload["passed"] == 5
    assert payload["failed"] == 0
    assert payload["scenarios"][2]["actual_control_ids"] == ["AUTH-003", "AUTH-004", "AUTH-005"]


def test_demo_cli_emits_deterministic_profile_output() -> None:
    result = RUNNER.invoke(app, ["demo", str(DATA_DIR / "demo_profile.json")])
    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["profile"] == "oidc_cookie_hybrid_demo"
    assert payload["control_ids"] == ["AUTH-001", "AUTH-003", "AUTH-004", "AUTH-005", "AUTH-006", "AUTH-007", "AUTH-008"]
    assert payload["findings"][0]["control_id"] == "AUTH-001"
    assert payload["findings"][-1]["control_id"] == "AUTH-008"

