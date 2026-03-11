from __future__ import annotations

from pathlib import Path

from owasp_backend_mitigations.cases import check_case_manifest, load_json
from owasp_backend_mitigations.evaluator import case_control_ids

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "problem" / "data"


def _case(name: str) -> dict[str, object]:
    bundle = load_json(DATA_DIR / "case_bundle.json")
    return next(case for case in bundle["cases"] if case["name"] == name)


def test_secure_baseline_has_no_findings() -> None:
    assert case_control_ids(_case("secure_baseline")) == []


def test_each_negative_case_returns_expected_control() -> None:
    assert case_control_ids(_case("raw_sql_login")) == ["OWASP-001"]
    assert case_control_ids(_case("idor_profile_read")) == ["OWASP-002"]
    assert case_control_ids(_case("webhook_ssrf")) == ["OWASP-003"]
    assert case_control_ids(_case("debug_trace_leak")) == ["OWASP-004"]
    assert case_control_ids(_case("unsafe_file_download")) == ["OWASP-005"]


def test_manifest_summary_passes_all_cases() -> None:
    result = check_case_manifest(DATA_DIR / "case_bundle.json")
    assert result["failed"] == 0

