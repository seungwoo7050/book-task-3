from __future__ import annotations

import json
import os
from pathlib import Path

from cli.main import app
from core.config import load_settings
from typer.testing import CliRunner

runner = CliRunner()


def test_load_settings_rejects_invalid_enum():
    os.environ["QUALBOT_EVAL_MODE"] = "invalid-mode"
    try:
        load_settings()
    except ValueError as exc:
        assert "QUALBOT_EVAL_MODE must be one of" in str(exc)
    else:
        raise AssertionError("expected ValueError for invalid eval mode")


def test_dependency_health_endpoint_heuristic_ok(client):
    os.environ["QUALBOT_EVAL_MODE"] = "heuristic"
    os.environ["QUALBOT_RETRIEVAL_BACKEND"] = "keyword"
    os.environ["QUALBOT_ENABLE_OLLAMA"] = "0"
    os.environ["QUALBOT_ENABLE_CHROMA"] = "0"

    response = client.get("/api/system/dependency-health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["eval_mode"] == "heuristic"
    assert payload["policy"] == "strict"
    assert "ollama_reachable" in payload
    assert "chroma_reachable" in payload
    assert "models_configured" in payload


def test_dependency_health_endpoint_llm_unavailable_returns_503(client):
    os.environ["QUALBOT_EVAL_MODE"] = "llm"
    os.environ["QUALBOT_RETRIEVAL_BACKEND"] = "chroma"
    os.environ["QUALBOT_ENABLE_OLLAMA"] = "1"
    os.environ["QUALBOT_ENABLE_CHROMA"] = "1"
    os.environ["QUALBOT_OLLAMA_JUDGE_MODEL"] = "judge-model"
    os.environ["QUALBOT_OLLAMA_CLAIM_MODEL"] = "claim-model"
    os.environ["QUALBOT_OLLAMA_EVIDENCE_MODEL"] = "evidence-model"
    os.environ["QUALBOT_OLLAMA_BASE_URL"] = "http://127.0.0.1:19999"

    response = client.get("/api/system/dependency-health")
    assert response.status_code == 503
    payload = response.json()
    assert set(payload.keys()) == {"error_code", "message", "component"}
    assert payload["error_code"] == "DEPENDENCY_UNAVAILABLE"
    assert payload["component"] in {"ollama", "chroma", "runtime", "provider"}


def test_cli_preflight_returns_nonzero_when_llm_dependency_unavailable():
    os.environ["QUALBOT_EVAL_MODE"] = "llm"
    os.environ["QUALBOT_RETRIEVAL_BACKEND"] = "chroma"
    os.environ["QUALBOT_ENABLE_OLLAMA"] = "1"
    os.environ["QUALBOT_ENABLE_CHROMA"] = "1"
    os.environ["QUALBOT_OLLAMA_JUDGE_MODEL"] = "judge-model"
    os.environ["QUALBOT_OLLAMA_CLAIM_MODEL"] = "claim-model"
    os.environ["QUALBOT_OLLAMA_EVIDENCE_MODEL"] = "evidence-model"
    os.environ["QUALBOT_OLLAMA_BASE_URL"] = "http://127.0.0.1:19999"

    result = runner.invoke(app, ["preflight"])
    assert result.exit_code == 1
    assert "DEPENDENCY_UNAVAILABLE" in result.stdout


def test_cli_demo_proof_heuristic_writes_artifacts(monkeypatch):
    repo_root = Path(__file__).resolve().parents[2]
    monkeypatch.chdir(repo_root)
    os.environ["QUALBOT_EVAL_MODE"] = "heuristic"
    os.environ["QUALBOT_RETRIEVAL_BACKEND"] = "keyword"
    os.environ["QUALBOT_ENABLE_OLLAMA"] = "0"
    os.environ["QUALBOT_ENABLE_CHROMA"] = "0"

    result = runner.invoke(app, ["demo-proof", "--mode", "heuristic"])
    assert result.exit_code == 0

    artifact = repo_root.parent / "docs/demo/proof-artifacts/api-golden-run.json"
    assert artifact.exists()
    payload = json.loads(artifact.read_text(encoding="utf-8"))
    assert "pass_count" in payload
    assert "fail_count" in payload
    assert "assertion_failures" in payload
