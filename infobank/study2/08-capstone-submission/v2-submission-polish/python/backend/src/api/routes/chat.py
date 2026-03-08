from __future__ import annotations

import uuid
from datetime import UTC, datetime

from chatbot.bot import ChatbotService
from core.config import load_settings
from core.json_utils import dumps_json, loads_json
from db.models import Conversation, Evaluation, Turn
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from api.dependencies import get_session
from api.schemas import ChatRequest

router = APIRouter(prefix="/api", tags=["chat"])


@router.post("/chat")
def post_chat(payload: ChatRequest, session: Session = Depends(get_session)) -> dict[str, object]:
    settings = load_settings()
    conversation_id = payload.conversation_id or str(uuid.uuid4())

    conversation = session.get(Conversation, conversation_id)
    if conversation is None:
        conversation = Conversation(
            id=conversation_id,
            prompt_version=payload.prompt_version or settings.prompt_version,
            kb_version=payload.kb_version or settings.kb_version,
            created_at=datetime.now(UTC),
        )
        session.add(conversation)

    turn_index = session.scalar(
        select(func.coalesce(func.max(Turn.turn_index), 0)).where(Turn.conversation_id == conversation_id)
    )
    turn_index = int(turn_index or 0) + 1

    bot = ChatbotService(session)
    reply = bot.answer(payload.user_message)

    turn = Turn(
        id=str(uuid.uuid4()),
        conversation_id=conversation_id,
        turn_index=turn_index,
        user_message=payload.user_message,
        assistant_response=reply.assistant_response,
        retrieved_doc_ids=dumps_json(reply.retrieved_doc_ids),
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
def list_conversations(limit: int = 50, session: Session = Depends(get_session)) -> dict[str, object]:
    rows = session.scalars(select(Conversation).order_by(Conversation.created_at.desc()).limit(limit)).all()
    data = []
    for row in rows:
        turn_count = session.scalar(select(func.count(Turn.id)).where(Turn.conversation_id == row.id)) or 0
        data.append(
            {
                "id": row.id,
                "created_at": row.created_at.isoformat(),
                "prompt_version": row.prompt_version,
                "kb_version": row.kb_version,
                "session_score": row.session_score,
                "session_grade": row.session_grade,
                "run_id": row.run_id,
                "turn_count": int(turn_count),
            }
        )
    return {"items": data}


@router.get("/conversations/{conversation_id}")
def get_conversation(conversation_id: str, session: Session = Depends(get_session)) -> dict[str, object]:
    conversation = session.get(Conversation, conversation_id)
    if conversation is None:
        raise HTTPException(status_code=404, detail="conversation not found")

    turns = session.scalars(
        select(Turn).where(Turn.conversation_id == conversation_id).order_by(Turn.turn_index.asc())
    ).all()

    turn_items: list[dict[str, object]] = []
    for turn in turns:
        eval_item = session.scalar(
            select(Evaluation)
            .where(Evaluation.turn_id == turn.id)
            .order_by(Evaluation.created_at.desc())
            .limit(1)
        )
        turn_items.append(
            {
                "id": turn.id,
                "turn_index": turn.turn_index,
                "user_message": turn.user_message,
                "assistant_response": turn.assistant_response,
                "retrieved_doc_ids": loads_json(turn.retrieved_doc_ids, []),
                "latency_ms": turn.latency_ms,
                "created_at": turn.created_at.isoformat(),
                "evaluation": None
                if eval_item is None
                else {
                    "id": eval_item.id,
                    "grade": eval_item.grade,
                    "total_score": eval_item.total_score,
                    "failure_types": loads_json(eval_item.failure_types, []),
                    "lineage": loads_json(eval_item.lineage_json, {}),
                    "judge_trace": loads_json(eval_item.judge_trace, {}),
                },
            }
        )

    return {
        "conversation": {
            "id": conversation.id,
            "prompt_version": conversation.prompt_version,
            "kb_version": conversation.kb_version,
            "session_score": conversation.session_score,
            "session_grade": conversation.session_grade,
            "run_id": conversation.run_id,
            "created_at": conversation.created_at.isoformat(),
        },
        "turns": turn_items,
    }
