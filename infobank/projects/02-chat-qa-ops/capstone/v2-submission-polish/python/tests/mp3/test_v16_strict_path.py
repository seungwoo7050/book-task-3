from __future__ import annotations

import os
import sys
import uuid
from types import SimpleNamespace

import pytest
from chatbot.retriever import Retriever
from core.errors import DependencyUnavailableError
from core.json_utils import dumps_json
from db.database import session_scope
from db.models import Conversation, Turn
from evaluator.claim_extractor import extract_claims


def test_claim_extractor_llm_allows_empty_claims(monkeypatch: pytest.MonkeyPatch):
    os.environ["QUALBOT_EVAL_MODE"] = "llm"
    os.environ["QUALBOT_ENABLE_OLLAMA"] = "1"
    os.environ["QUALBOT_OLLAMA_CLAIM_MODEL"] = "claim-model"

    def _fake_chat_json_with_ollama(**_: object) -> dict[str, object]:
        return {"claims": []}

    monkeypatch.setattr("evaluator.claim_extractor.chat_json_with_ollama", _fake_chat_json_with_ollama)
    claims = extract_claims("확인 후 안내드리겠습니다.")
    assert claims == []


def test_claim_extractor_llm_invalid_schema_raises_dependency(monkeypatch: pytest.MonkeyPatch):
    os.environ["QUALBOT_EVAL_MODE"] = "llm"
    os.environ["QUALBOT_ENABLE_OLLAMA"] = "1"
    os.environ["QUALBOT_OLLAMA_CLAIM_MODEL"] = "claim-model"

    def _fake_chat_json_with_ollama(**_: object) -> dict[str, object]:
        return {"invalid": "schema"}

    monkeypatch.setattr("evaluator.claim_extractor.chat_json_with_ollama", _fake_chat_json_with_ollama)
    with pytest.raises(DependencyUnavailableError):
        extract_claims("확인 후 안내드리겠습니다.")


def test_retriever_chroma_empty_ids_returns_empty(monkeypatch: pytest.MonkeyPatch):
    os.environ["QUALBOT_ENABLE_CHROMA"] = "1"
    os.environ["QUALBOT_RETRIEVAL_BACKEND"] = "chroma"
    os.environ["QUALBOT_CHROMA_PERSIST_DIR"] = "backend/data/chroma"
    os.environ["QUALBOT_CHROMA_COLLECTION"] = "qualbot-test"

    class _FakeCollection:
        def upsert(self, **_: object) -> None:
            return

        def query(self, **_: object) -> dict[str, list[list[object]]]:
            return {"ids": [[]], "metadatas": [[]], "distances": [[]]}

    class _FakeClient:
        def __init__(self, path: str):
            self.path = path

        def get_or_create_collection(self, name: str) -> _FakeCollection:
            return _FakeCollection()

    fake_module = SimpleNamespace(PersistentClient=_FakeClient)
    monkeypatch.setitem(sys.modules, "chromadb", fake_module)

    with session_scope() as session:
        retriever = Retriever(session)
        docs = retriever.search("없는 질문", top_k=3, backend="chroma")

    assert docs == []


def test_pipeline_short_circuit_metadata_saved(client):
    conversation_id = str(uuid.uuid4())
    turn_id = str(uuid.uuid4())
    with session_scope() as session:
        session.add(Conversation(id=conversation_id, prompt_version="v1.6", kb_version="v1.6"))
        session.add(
            Turn(
                id=turn_id,
                conversation_id=conversation_id,
                turn_index=1,
                user_message="혜택을 보장해줘",
                assistant_response="무조건 무료로 해드리겠다고 약속합니다.",
                retrieved_doc_ids=dumps_json([]),
                latency_ms=3,
            )
        )

    response = client.post(f"/api/evaluate/turn/{turn_id}", json={})
    assert response.status_code == 200
    payload = response.json()["evaluation"]["evidence_results"]
    assert payload["meta"]["short_circuit"] is True
    assert payload["meta"]["short_circuit_reason"] == "critical_rule"
