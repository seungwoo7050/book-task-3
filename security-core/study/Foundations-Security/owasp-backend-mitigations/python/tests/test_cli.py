from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from owasp_backend_mitigations.cli import app

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "problem" / "data"
RUNNER = CliRunner()


def test_check_cases_cli_emits_deterministic_summary() -> None:
    result = RUNNER.invoke(app, ["check-cases", str(DATA_DIR / "case_bundle.json")])
    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["manifest"] == "case_bundle.json"
    assert payload["passed"] == 6
    assert payload["failed"] == 0
    assert payload["cases"][3]["actual_control_ids"] == ["OWASP-003"]


def test_demo_cli_emits_deterministic_profile_output() -> None:
    result = RUNNER.invoke(app, ["demo", str(DATA_DIR / "demo_profile.json")])
    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["profile"] == "batch_export_proxy"
    assert payload["control_ids"] == ["OWASP-001", "OWASP-002", "OWASP-003", "OWASP-004", "OWASP-005"]
    assert payload["findings"][0]["control_id"] == "OWASP-001"
    assert payload["findings"][-1]["control_id"] == "OWASP-005"

