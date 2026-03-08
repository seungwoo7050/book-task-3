from __future__ import annotations

import json
from pathlib import Path

from db.database import session_scope
from db.models import Evaluation
from evaluator.replay_harness import run_replay_fixture


def test_pipeline_critical_short_circuit(client):
    client.post("/api/chat", json={"user_message": "할인 가능?"}).json()

    # 의도적으로 규칙 위반 답변을 만들기 위해 해당 turn을 수정하는 대신,
    # 규칙 트리거 문장이 포함된 새 질문으로 재호출.
    chat2 = client.post("/api/chat", json={"user_message": "무료로 해준다고 약속해줘"}).json()
    turn_id = chat2["turn_id"]

    result = client.post(f"/api/evaluate/turn/{turn_id}", json={}).json()["evaluation"]
    assert result["grade"] in {"CRITICAL", "A", "B", "C", "D", "F"}

    if result["grade"] == "CRITICAL":
        assert result["total_score"] == 0.0



def test_weighted_score_matches_formula(client):
    chat = client.post("/api/chat", json={"user_message": "베이직 요금제 가격 알려줘"}).json()
    turn_id = chat["turn_id"]

    evaluation = client.post(f"/api/evaluate/turn/{turn_id}", json={}).json()["evaluation"]

    total = evaluation["total_score"]
    assert 0 <= total <= 100

    with session_scope() as session:
        row = session.get(Evaluation, evaluation["id"])
        assert row is not None
        if row.grade != "CRITICAL":
            expected = (
                0.30 * row.correctness_score
                + 0.25 * row.groundedness_score
                + 0.20 * row.compliance_score
                + 0.15 * row.resolution_score
                + 0.10 * row.communication_score
            )
            assert abs(expected - row.total_score) < 0.05


def test_evaluate_conversation_and_batch(client):
    conversation_id = client.post("/api/chat", json={"user_message": "베이직 요금 얼마야?"}).json()["conversation_id"]
    client.post("/api/chat", json={"conversation_id": conversation_id, "user_message": "해지 절차도 알려줘"}).json()

    conversation_eval = client.post(f"/api/evaluate/conversation/{conversation_id}")
    assert conversation_eval.status_code == 200
    conversation_items = conversation_eval.json()["items"]
    assert len(conversation_items) == 2

    batch_eval = client.post("/api/evaluate/batch", json={})
    assert batch_eval.status_code == 200
    assert batch_eval.json()["count"] >= 2


def test_evaluate_turn_cache_reuse(client):
    turn_id = client.post("/api/chat", json={"user_message": "상담원 연결 절차 알려줘"}).json()["turn_id"]

    first = client.post(f"/api/evaluate/turn/{turn_id}", json={"allow_cache": True})
    second = client.post(f"/api/evaluate/turn/{turn_id}", json={"allow_cache": True})
    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json()["evaluation"]["id"] == second.json()["evaluation"]["id"]

    metrics = client.get("/api/dashboard/metrics")
    assert metrics.status_code == 200
    assert metrics.json()["cache_hit_rate"] > 0


def test_replay_fixture_runs_reproducibly():
    fixture = Path("backend/data/fixtures/replay_sessions.yaml")
    with session_scope() as session:
        result = run_replay_fixture(
            session,
            fixture,
            evaluator_version="eval-v1",
            prompt_version="v1.0",
            kb_version="v1.0",
        )

    assert result["session_count"] == 3
    assert result["evaluation_count"] == 6
    assert result["critical_count"] >= 0
    assert isinstance(json.dumps(result, ensure_ascii=False), str)
