from __future__ import annotations

from pathlib import Path

from auth_threat_modeling.evaluator import scenario_control_ids
from auth_threat_modeling.scenarios import check_scenarios_manifest, load_json

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "problem" / "data"


def _scenario(name: str) -> dict[str, object]:
    bundle = load_json(DATA_DIR / "scenario_bundle.json")
    return next(s for s in bundle["scenarios"] if s["name"] == name)


def test_secure_baseline_has_no_findings() -> None:
    assert scenario_control_ids(_scenario("secure_baseline")) == []


def test_oauth_missing_state_and_pkce_returns_expected_controls() -> None:
    assert scenario_control_ids(_scenario("oauth_missing_state_and_pkce")) == ["AUTH-001", "AUTH-002"]


def test_jwt_validation_gap_returns_expected_controls() -> None:
    assert scenario_control_ids(_scenario("jwt_validation_gap")) == ["AUTH-003", "AUTH-004", "AUTH-005"]


def test_cookie_without_csrf_returns_expected_control() -> None:
    assert scenario_control_ids(_scenario("cookie_without_csrf")) == ["AUTH-006"]


def test_recovery_and_rate_limit_gap_returns_expected_controls() -> None:
    assert scenario_control_ids(_scenario("recovery_and_rate_limit_gap")) == ["AUTH-007", "AUTH-008"]


def test_manifest_summary_passes_all_scenarios() -> None:
    result = check_scenarios_manifest(DATA_DIR / "scenario_bundle.json")
    assert result["failed"] == 0

