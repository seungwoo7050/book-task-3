from __future__ import annotations

import os
import uuid

from core.json_utils import dumps_json
from db.database import session_scope
from db.models import Conversation, Turn
from evaluator.golden_assertion import evaluate_golden_case


def test_golden_assertion_subset_and_any_evidence_rule():
    evaluation = {
        "failure_types": ["FORBIDDEN_PROMISE", "MISSING_MANDATORY_STEP"],
        "evidence_results": {
            "claim_results": [
                {"evidence_doc_ids": ["policies__discount_policy.md"]},
                {"evidence_doc_ids": ["plans__basic_plan.md"]},
            ]
        },
    }
    assertion = evaluate_golden_case(
        case_id="gs-demo",
        expected_config={
            "expected_failure_types": ["FORBIDDEN_PROMISE"],
            "required_evidence_doc_ids": ["policies__discount_policy.md", "other.md"],
        },
        evaluation=evaluation,
        retrieved_doc_ids=[],
    )
    assert assertion.passed is True
    assert assertion.reason_codes == []


def test_golden_set_run_returns_assertion_summary(client):
    response = client.post("/api/golden-set/run", json={"prompt_version": "v1.0"})
    assert response.status_code == 200
    payload = response.json()
    assert "pass_count" in payload
    assert "fail_count" in payload
    assert "assertion_failures" in payload
    assert payload["pass_count"] + payload["fail_count"] == payload["count"]
    assert isinstance(payload["assertion_failures"], list)


def test_evaluate_turn_returns_503_on_dependency_unavailable(client):
    conversation_id = str(uuid.uuid4())
    turn_id = str(uuid.uuid4())
    with session_scope() as session:
        session.add(Conversation(id=conversation_id, prompt_version="v1.0", kb_version="v1.0"))
        session.add(
            Turn(
                id=turn_id,
                conversation_id=conversation_id,
                turn_index=1,
                user_message="프리미엄 요금제 해지 위약금 있나요?",
                assistant_response="해지 시 위약금은 없습니다.",
                retrieved_doc_ids=dumps_json([]),
                latency_ms=5,
            )
        )

    os.environ["QUALBOT_EVAL_MODE"] = "llm"
    os.environ["QUALBOT_RETRIEVAL_BACKEND"] = "chroma"
    os.environ["QUALBOT_ENABLE_OLLAMA"] = "0"
    os.environ["QUALBOT_ENABLE_CHROMA"] = "0"
    response = client.post(f"/api/evaluate/turn/{turn_id}", json={})
    assert response.status_code == 503
    payload = response.json()
    assert payload["error_code"] == "DEPENDENCY_UNAVAILABLE"
    assert payload["component"] in {"ollama", "chroma", "runtime"}


def test_golden_set_run_returns_503_on_dependency_unavailable(client):
    os.environ["QUALBOT_EVAL_MODE"] = "llm"
    os.environ["QUALBOT_RETRIEVAL_BACKEND"] = "chroma"
    os.environ["QUALBOT_ENABLE_OLLAMA"] = "0"
    os.environ["QUALBOT_ENABLE_CHROMA"] = "0"
    os.environ["QUALBOT_OLLAMA_JUDGE_MODEL"] = "judge-model"
    os.environ["QUALBOT_OLLAMA_CLAIM_MODEL"] = "claim-model"
    os.environ["QUALBOT_OLLAMA_EVIDENCE_MODEL"] = "evidence-model"

    response = client.post("/api/golden-set/run", json={})
    assert response.status_code == 503
    payload = response.json()
    assert set(payload.keys()) == {"error_code", "message", "component"}
    assert payload["error_code"] == "DEPENDENCY_UNAVAILABLE"
