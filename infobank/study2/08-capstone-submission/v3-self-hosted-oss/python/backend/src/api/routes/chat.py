from __future__ import annotations

import uuid
from datetime import UTC, datetime

from chatbot.bot import ChatbotService
from core.config import load_settings
from core.json_utils import dumps_json, loads_json
from db.models import (
    AdminUser,
    Conversation,
    Evaluation,
    EvaluationJob,
    EvaluationRun,
    KnowledgeBaseBundle,
    Turn,
)
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from api.dependencies import get_current_admin, get_session
from api.schemas import ChatRequest

router = APIRouter(prefix="/api", tags=["chat"])


def _resolve_run(session: Session, *, run_id: str | None, job_id: str | None) -> EvaluationRun | None:
    if run_id:
        return session.get(EvaluationRun, run_id)
    if job_id:
        job = session.get(EvaluationJob, job_id)
        if job is None or not job.run_id:
            return None
        return session.get(EvaluationRun, job.run_id)
    latest_job = session.scalar(
        select(EvaluationJob).where(EvaluationJob.run_id.is_not(None)).order_by(EvaluationJob.created_at.desc()).limit(1)
    )
    if latest_job is None or not latest_job.run_id:
        return None
    return session.get(EvaluationRun, latest_job.run_id)


def _sample_bundle_id(session: Session) -> str | None:
    bundle = session.scalar(
        select(KnowledgeBaseBundle).where(KnowledgeBaseBundle.is_sample.is_(True)).order_by(KnowledgeBaseBundle.created_at.asc()).limit(1)
    )
    return bundle.id if bundle is not None else None


@router.post("/chat")
def post_chat(
    payload: ChatRequest,
    _: AdminUser = Depends(get_current_admin),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    settings = load_settings()
    conversation_id = payload.conversation_id or str(uuid.uuid4())

    conversation = session.get(Conversation, conversation_id)
    if conversation is None:
        conversation = Conversation(
            id=conversation_id,
            prompt_version=payload.prompt_version or settings.prompt_version,
            kb_version=payload.kb_version or settings.kb_version,
            created_at=datetime.now(UTC),
            metadata_json="{}",
        )
        session.add(conversation)

    turn_index = session.scalar(
        select(func.coalesce(func.max(Turn.turn_index), 0)).where(Turn.conversation_id == conversation_id)
    )
    turn_index = int(turn_index or 0) + 1

    bot = ChatbotService(session)
    reply = bot.answer(payload.user_message, kb_bundle_id=payload.kb_bundle_id or _sample_bundle_id(session))

    turn = Turn(
        id=str(uuid.uuid4()),
        conversation_id=conversation_id,
        turn_index=turn_index,
        user_message=payload.user_message,
        assistant_response=reply.assistant_response,
        retrieved_doc_ids=dumps_json(reply.retrieved_doc_ids),
        tags_json="[]",
        metadata_json="{}",
        source_timestamp=None,
        latency_ms=reply.latency_ms,
        created_at=datetime.now(UTC),
    )
    session.add(turn)
    session.commit()

    return {
        "conversation_id": conversation_id,
        "turn_id": turn.id,
        "assistant_response": reply.assistant_response,
        "retrieved_doc_ids": reply.retrieved_doc_ids,
        "latency_ms": reply.latency_ms,
        "guardrail_hits": reply.guardrail_hits,
        "provider_trace": reply.provider_trace,
    }


@router.get("/conversations")
def list_conversations(
    limit: int = 50,
    run_id: str | None = None,
    job_id: str | None = None,
    _: AdminUser = Depends(get_current_admin),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    run = _resolve_run(session, run_id=run_id, job_id=job_id)
    stmt = select(Conversation).order_by(Conversation.created_at.desc()).limit(limit)
    if run is not None and run.batch_id:
        stmt = select(Conversation).where(Conversation.batch_id == run.batch_id).order_by(Conversation.created_at.desc()).limit(limit)
    rows = session.scalars(stmt).all()

    items: list[dict[str, object]] = []
    for row in rows:
        turn_count = int(session.scalar(select(func.count(Turn.id)).where(Turn.conversation_id == row.id)) or 0)
        session_score = row.session_score
        session_grade = row.session_grade
        if run is not None:
            avg_score, eval_count = session.execute(
                select(func.avg(Evaluation.total_score), func.count(Evaluation.id))
                .join(Turn, Turn.id == Evaluation.turn_id)
                .where(Turn.conversation_id == row.id, Evaluation.run_id == run.id)
            ).one()
            if eval_count:
                session_score = round(float(avg_score or 0.0), 2)
                if session_score >= 90:
                    session_grade = "A"
                elif session_score >= 75:
                    session_grade = "B"
                elif session_score >= 60:
                    session_grade = "C"
                elif session_score >= 40:
                    session_grade = "D"
                else:
                    session_grade = "F"
        items.append(
            {
                "id": row.id,
                "external_id": row.external_id,
                "created_at": row.created_at.isoformat(),
                "prompt_version": row.prompt_version,
                "kb_version": row.kb_version,
                "session_score": session_score,
                "session_grade": session_grade,
                "run_id": run.id if run is not None else row.run_id,
                "turn_count": turn_count,
            }
        )
    return {"selected_run_id": run.id if run is not None else None, "items": items}


@router.get("/conversations/{conversation_id}")
def get_conversation(
    conversation_id: str,
    run_id: str | None = None,
    job_id: str | None = None,
    _: AdminUser = Depends(get_current_admin),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    conversation = session.get(Conversation, conversation_id)
    if conversation is None:
        raise HTTPException(status_code=404, detail="conversation not found")
    run = _resolve_run(session, run_id=run_id, job_id=job_id)

    turns = session.scalars(
        select(Turn).where(Turn.conversation_id == conversation_id).order_by(Turn.turn_index.asc())
    ).all()

    turn_items: list[dict[str, object]] = []
    for turn in turns:
        eval_stmt = select(Evaluation).where(Evaluation.turn_id == turn.id)
        if run is not None:
            eval_stmt = eval_stmt.where(Evaluation.run_id == run.id)
        eval_stmt = eval_stmt.order_by(Evaluation.created_at.desc()).limit(1)
        eval_item = session.scalar(eval_stmt)
        retrieved_doc_ids = loads_json(turn.retrieved_doc_ids, [])
        if not retrieved_doc_ids and eval_item is not None:
            trace_docs = loads_json(eval_item.retrieval_trace, [])
            derived_ids: list[str] = []
            for trace in trace_docs:
                if isinstance(trace, dict):
                    docs = trace.get("docs", [])
                    if isinstance(docs, list):
                        for doc in docs:
                            if isinstance(doc, dict) and isinstance(doc.get("doc_id"), str):
                                derived_ids.append(doc["doc_id"])
            retrieved_doc_ids = list(dict.fromkeys(derived_ids))
        turn_items.append(
            {
                "id": turn.id,
                "turn_index": turn.turn_index,
                "user_message": turn.user_message,
                "assistant_response": turn.assistant_response,
                "retrieved_doc_ids": retrieved_doc_ids,
                "latency_ms": turn.latency_ms,
                "created_at": turn.created_at.isoformat(),
                "tags": loads_json(turn.tags_json, []),
                "metadata": loads_json(turn.metadata_json, {}),
                "evaluation": None
                if eval_item is None
                else {
                    "id": eval_item.id,
                    "grade": eval_item.grade,
                    "total_score": eval_item.total_score,
                    "failure_types": loads_json(eval_item.failure_types, []),
                    "lineage": loads_json(eval_item.lineage_json, {}),
                    "judge_trace": loads_json(eval_item.judge_trace, {}),
                    "retrieval_trace": loads_json(eval_item.retrieval_trace, []),
                    "claim_trace": loads_json(eval_item.claim_trace, []),
                },
            }
        )

    return {
        "conversation": {
            "id": conversation.id,
            "external_id": conversation.external_id,
            "prompt_version": conversation.prompt_version,
            "kb_version": conversation.kb_version,
            "session_score": conversation.session_score,
            "session_grade": conversation.session_grade,
            "run_id": run.id if run is not None else conversation.run_id,
            "created_at": conversation.created_at.isoformat(),
        },
        "turns": turn_items,
    }
