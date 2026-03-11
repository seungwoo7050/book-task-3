from __future__ import annotations

import uuid

from core.json_utils import dumps_json
from db.database import session_scope
from db.models import Conversation, Turn
from evaluator.claim_extractor import extract_claims
from evaluator.evidence_verifier import verify_claims


def test_evidence_contradiction_detected():
    response = "프리미엄 요금제는 해지 시 위약금이 없습니다."
    claims = extract_claims(response)

    with session_scope() as session:
        result = verify_claims(session, claims)

    assert result.claim_results
    assert any(item.verdict in {"contradict", "support", "not_found"} for item in result.claim_results)
    # cancellation_policy 근거가 있으므로 부정 단정 문구는 모순 가능성이 높아야 한다.
    assert result.has_contradiction is True


def test_pipeline_marks_contradiction_as_critical(client):
    conversation_id = str(uuid.uuid4())
    turn_id = str(uuid.uuid4())
    with session_scope() as session:
        session.add(Conversation(id=conversation_id, prompt_version="v1.0", kb_version="v1.0"))
        session.add(
            Turn(
                id=turn_id,
                conversation_id=conversation_id,
                turn_index=1,
                user_message="프리미엄 요금제 해지 위약금이 있나요?",
                assistant_response="프리미엄 요금제는 해지 시 위약금이 없습니다.",
                retrieved_doc_ids=dumps_json([]),
                latency_ms=5,
            )
        )

    response = client.post(f"/api/evaluate/turn/{turn_id}", json={})
    assert response.status_code == 200
    evaluation = response.json()["evaluation"]
    assert evaluation["evidence_results"]["has_contradiction"] is True
    assert evaluation["grade"] == "CRITICAL"
    assert "CONTRADICTED_BY_SOURCE" in evaluation["failure_types"]


def test_negative_policy_statement_is_supported_when_source_has_same_negation():
    response = "상담원이 임의로 할인/면제/무료를 약속할 수 없습니다."
    claims = extract_claims(response)

    with session_scope() as session:
        result = verify_claims(session, claims)

    assert result.claim_results
    assert result.claim_results[0].verdict == "support"
    assert result.has_contradiction is False
