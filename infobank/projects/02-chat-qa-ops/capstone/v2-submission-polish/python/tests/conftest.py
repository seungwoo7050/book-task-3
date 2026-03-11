from __future__ import annotations

import os
from pathlib import Path

import pytest
from api.main import app
from db.database import init_db, reset_engines, session_scope
from db.seed import seed_golden_set, seed_knowledge_base
from evaluator.pipeline_stats import reset_stats_store
from fastapi.testclient import TestClient


@pytest.fixture(autouse=True)
def isolated_db(tmp_path: Path) -> None:
    db_path = tmp_path / "qualbot-test.db"
    os.environ["QUALBOT_DB_URL"] = f"sqlite:///{db_path}"
    os.environ["QUALBOT_EVAL_MODE"] = "heuristic"
    os.environ["QUALBOT_RETRIEVAL_BACKEND"] = "keyword"
    os.environ["QUALBOT_ENABLE_OLLAMA"] = "0"
    os.environ["QUALBOT_ENABLE_CHROMA"] = "0"
    os.environ.pop("QUALBOT_OLLAMA_JUDGE_MODEL", None)
    os.environ.pop("QUALBOT_OLLAMA_CLAIM_MODEL", None)
    os.environ.pop("QUALBOT_OLLAMA_EVIDENCE_MODEL", None)
    reset_stats_store()
    reset_engines()
    init_db()
    with session_scope() as session:
        seed_knowledge_base(session, Path("backend/knowledge_base"))
        seed_golden_set(session, Path("backend/golden_set/phase1_seed.yaml"))
    yield
    reset_stats_store()
    reset_engines()


@pytest.fixture()
def client() -> TestClient:
    return TestClient(app)
