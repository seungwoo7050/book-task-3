from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from collab_saas_security_review.cli import app

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "problem" / "data"
RUNNER = CliRunner()


def test_review_cli_emits_deterministic_consolidated_json() -> None:
    result = RUNNER.invoke(app, ["review", str(DATA_DIR / "review_bundle.json")])
    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["service"]["name"] == "workspace-api"
    assert payload["summary"] == {
        "crypto_findings": 4,
        "auth_findings": 8,
        "backend_findings": 5,
        "dependency_items": 4,
        "remediation_items": 21,
    }
    assert payload["remediation_board"][0]["id"] == "crypto:CRYPTO-001:workspace_session_crypto_gap"
    assert payload["remediation_board"][-1]["id"] == "dependency:CVE-2026-1003:pytest"


def test_review_cli_writes_all_artifacts_when_output_dir_is_provided(tmp_path: Path) -> None:
    result = RUNNER.invoke(
        app,
        ["review", str(DATA_DIR / "review_bundle.json"), "--output-dir", str(tmp_path)],
    )
    assert result.exit_code == 0
    assert sorted(path.name for path in tmp_path.iterdir()) == [
        "01-service-profile.json",
        "02-crypto-findings.json",
        "03-auth-findings.json",
        "04-backend-findings.json",
        "05-dependency-items.json",
        "06-remediation-board.json",
        "07-report.md",
    ]


def test_demo_cli_writes_demo_assets_and_report_sections(tmp_path: Path) -> None:
    result = RUNNER.invoke(
        app,
        ["demo", str(DATA_DIR / "demo_bundle.json"), "--output-dir", str(tmp_path)],
    )
    assert result.exit_code == 0
    assert result.stdout.strip() == f"demo 산출물을 {tmp_path}에 기록했습니다"
    report = (tmp_path / "07-report.md").read_text()
    assert "# 서비스 요약" in report
    assert "# 암호 finding" in report
    assert "# 인증 finding" in report
    assert "# 백엔드 finding" in report
    assert "# 의존성 큐" in report
    assert "# 조치 보드" in report
