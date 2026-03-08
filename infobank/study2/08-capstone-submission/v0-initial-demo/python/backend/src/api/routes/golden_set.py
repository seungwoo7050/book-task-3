from __future__ import annotations

import uuid
from datetime import UTC, datetime

from chatbot.bot import ChatbotService
from core.errors import DependencyUnavailableError
from core.json_utils import dumps_json, loads_json
from db.models import Conversation, GoldenSet, Turn
from evaluator.golden_assertion import evaluate_golden_case, summarize_assertions
from evaluator.pipeline import EvaluationPipeline, serialize_evaluation
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from api.dependencies import get_session
from api.error_responses import dependency_unavailable_response
from api.schemas import GoldenSetCreateRequest, GoldenSetRunRequest

router = APIRouter(prefix="/api", tags=["golden-set"])


@router.get("/golden-set")
def list_golden_set(session: Session = Depends(get_session)) -> dict[str, object]:
    rows = list(session.scalars(select(GoldenSet).order_by(GoldenSet.id.asc())).all())
    return {
        "items": [
            {
                "id": row.id,
                "category": row.category,
                "user_message": row.user_message,
                "expected_config": loads_json(row.expected_config, {}),
                "tags": loads_json(row.tags, []),
            }
            for row in rows
        ]
    }


@router.post("/golden-set")
def create_golden_set(payload: GoldenSetCreateRequest, session: Session = Depends(get_session)) -> dict[str, object]:
    item = session.get(GoldenSet, payload.id)
    expected = {
        "expected_failure_types": payload.expected_failure_types,
        "required_evidence_doc_ids": payload.required_evidence_doc_ids,
    }
    if item is None:
        item = GoldenSet(
            id=payload.id,
            category=payload.category,
            user_message=payload.user_message,
            expected_config=dumps_json(expected),
            tags=dumps_json(payload.tags),
        )
        session.add(item)
    else:
        item.category = payload.category
        item.user_message = payload.user_message
        item.expected_config = dumps_json(expected)
        item.tags = dumps_json(payload.tags)

    session.commit()
    return {"id": item.id}


@router.post("/golden-set/run")
def run_golden_set(payload: GoldenSetRunRequest, session: Session = Depends(get_session)) -> dict[str, object]:
    rows = list(session.scalars(select(GoldenSet).order_by(GoldenSet.id.asc())).all())
    if payload.limit:
        rows = rows[: payload.limit]

    bot = ChatbotService(session)
    pipeline = EvaluationPipeline(session)

    evaluation_items = []
    assertions = []
    try:
        for row in rows:
            conversation = Conversation(
                id=str(uuid.uuid4()),
                created_at=datetime.now(UTC),
                prompt_version=payload.prompt_version or "v1.0",
                kb_version=payload.kb_version or "v1.0",
            )
            session.add(conversation)
            session.flush()

            reply = bot.answer(row.user_message)
            turn = Turn(
                id=str(uuid.uuid4()),
                conversation_id=conversation.id,
                turn_index=1,
                user_message=row.user_message,
                assistant_response=reply.assistant_response,
                retrieved_doc_ids=dumps_json(reply.retrieved_doc_ids),
                latency_ms=reply.latency_ms,
                created_at=datetime.now(UTC),
            )
            session.add(turn)
            session.flush()

            evaluation = pipeline.evaluate_turn(
                turn.id,
                evaluator_version=payload.evaluator_version,
                prompt_version=payload.prompt_version,
                kb_version=payload.kb_version,
                allow_cache=False,
            )
            serialized = serialize_evaluation(evaluation)
            expected_config = loads_json(row.expected_config, {})
            assertion = evaluate_golden_case(
                case_id=row.id,
                expected_config=expected_config,
                evaluation=serialized,
                retrieved_doc_ids=reply.retrieved_doc_ids,
            )
            serialized["assertion"] = assertion.to_dict()
            evaluation_items.append(serialized)
            assertions.append(assertion)

        session.commit()
    except DependencyUnavailableError as exc:
        session.rollback()
        return dependency_unavailable_response(exc)  # type: ignore[return-value]

    total_score = 0.0
    for item in evaluation_items:
        raw = item.get("total_score")
        if isinstance(raw, int | float):
            total_score += float(raw)
    avg_score = round(total_score / len(evaluation_items), 2) if evaluation_items else 0.0
    assertion_summary = summarize_assertions(assertions).to_dict()

    payload_out: dict[str, object] = {
        "count": len(evaluation_items),
        "avg_score": avg_score,
        "critical_count": sum(1 for item in evaluation_items if bool(item["is_critical"])),
        "items": evaluation_items,
    }
    payload_out.update(assertion_summary)
    return payload_out
