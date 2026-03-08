from __future__ import annotations

import os
from pathlib import Path

import pytest
from api.main import app
from db.database import init_db, reset_engines
from evaluator.pipeline_stats import reset_stats_store
from fastapi.testclient import TestClient


@pytest.fixture(autouse=True)
def isolated_db(tmp_path: Path) -> None:
    db_path = tmp_path / "qualbot-test.db"
    storage_root = tmp_path / "storage"
    os.environ["QUALBOT_DATABASE_URL"] = f"sqlite:///{db_path}"
    os.environ["QUALBOT_EVAL_MODE"] = "heuristic"
    os.environ["QUALBOT_RETRIEVAL_BACKEND"] = "keyword"
    os.environ["QUALBOT_ENABLE_OLLAMA"] = "0"
    os.environ["QUALBOT_ENABLE_CHROMA"] = "0"
    os.environ["QUALBOT_SESSION_SECRET"] = "test-session-secret"
    os.environ["QUALBOT_ADMIN_EMAIL"] = "admin@example.com"
    os.environ["QUALBOT_ADMIN_PASSWORD"] = "password123"
    os.environ["QUALBOT_STORAGE_ROOT"] = str(storage_root)
    os.environ.pop("QUALBOT_OLLAMA_JUDGE_MODEL", None)
    os.environ.pop("QUALBOT_OLLAMA_CLAIM_MODEL", None)
    os.environ.pop("QUALBOT_OLLAMA_EVIDENCE_MODEL", None)
    reset_stats_store()
    reset_engines()
    init_db()
    yield
    reset_stats_store()
    reset_engines()


@pytest.fixture()
def client() -> TestClient:
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture()
def auth_client(client: TestClient) -> TestClient:
    response = client.post(
        "/api/auth/login",
        json={"email": "admin@example.com", "password": "password123"},
    )
    assert response.status_code == 200
    return client


@pytest.fixture()
def temp_jsonl(tmp_path: Path) -> Path:
    path = tmp_path / "import.jsonl"
    path.write_text(
        "\n".join(
            [
                '{"conversation_external_id":"conv-a","turn_index":1,"user_message":"환불 접수됐나요?","assistant_response":"환불은 본인확인 후 접수 상태를 확인해야 합니다.","tags":["refund"],"metadata":{"channel":"web"}}',
                '{"conversation_external_id":"conv-b","turn_index":1,"user_message":"가족결합 할인 확정 가능한가요?","assistant_response":"가족결합은 조건에 따라 달라 확정 안내가 어렵습니다.","tags":["plan"],"metadata":{"channel":"app"}}',
            ]
        ),
        encoding="utf-8",
    )
    return path
