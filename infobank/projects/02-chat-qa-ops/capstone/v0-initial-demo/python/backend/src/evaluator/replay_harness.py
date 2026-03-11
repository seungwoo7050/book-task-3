from __future__ import annotations

import uuid
from pathlib import Path
from typing import Any

import yaml
from chatbot.bot import ChatbotService
from core.json_utils import dumps_json
from db.models import Conversation, Turn
from sqlalchemy.orm import Session

from evaluator.pipeline import EvaluationPipeline, serialize_evaluation


def load_replay_fixture(path: str | Path) -> list[dict[str, Any]]:
    fixture_path = Path(path)
    raw = yaml.safe_load(fixture_path.read_text(encoding="utf-8")) or {}
    sessions = raw.get("sessions", [])
    if not isinstance(sessions, list):
        raise ValueError("replay fixture must define a list under sessions")
    normalized: list[dict[str, Any]] = []
    for item in sessions:
        if not isinstance(item, dict):
            continue
        turns = item.get("turns", [])
        if not isinstance(turns, list):
            raise ValueError("replay fixture turns must be a list")
        normalized.append(item)
    return normalized


def run_replay_fixture(
    session: Session,
    fixture_path: str | Path,
    *,
    evaluator_version: str,
    prompt_version: str,
    kb_version: str,
) -> dict[str, Any]:
    fixture_sessions = load_replay_fixture(fixture_path)
    bot = ChatbotService(session)
    pipeline = EvaluationPipeline(session)

    replay_items: list[dict[str, Any]] = []
    for fixture in fixture_sessions:
        conversation = Conversation(
            id=str(uuid.uuid4()),
            prompt_version=prompt_version,
            kb_version=kb_version,
        )
        session.add(conversation)
        session.flush()

        turn_items: list[dict[str, Any]] = []
        for index, raw_turn in enumerate(fixture.get("turns", []), start=1):
            if not isinstance(raw_turn, dict):
                continue
            user_message = str(raw_turn.get("user_message", "")).strip()
            if not user_message:
                continue
            reply = bot.answer(user_message)
            turn = Turn(
                id=str(uuid.uuid4()),
                conversation_id=conversation.id,
                turn_index=index,
                user_message=user_message,
                assistant_response=reply.assistant_response,
                retrieved_doc_ids=dumps_json(reply.retrieved_doc_ids),
                latency_ms=reply.latency_ms,
            )
            session.add(turn)
            session.flush()
            evaluation = pipeline.evaluate_turn(
                turn.id,
                evaluator_version=evaluator_version,
                prompt_version=prompt_version,
                kb_version=kb_version,
                allow_cache=False,
            )
            turn_items.append(
                {
                    "turn_id": turn.id,
                    "user_message": user_message,
                    "assistant_response": reply.assistant_response,
                    "retrieved_doc_ids": reply.retrieved_doc_ids,
                    "evaluation": serialize_evaluation(evaluation),
                }
            )

        replay_items.append(
            {
                "fixture_id": fixture.get("id", conversation.id),
                "title": fixture.get("title", fixture.get("id", "session")),
                "conversation_id": conversation.id,
                "turns": turn_items,
            }
        )

    evaluation_count = sum(len(item["turns"]) for item in replay_items)
    critical_count = sum(
        1
        for item in replay_items
        for turn in item["turns"]
        if bool(turn["evaluation"]["is_critical"])
    )
    score_total = sum(
        float(turn["evaluation"]["total_score"])
        for item in replay_items
        for turn in item["turns"]
    )
    avg_score = round(score_total / evaluation_count, 2) if evaluation_count else 0.0

    return {
        "fixture": str(fixture_path),
        "session_count": len(replay_items),
        "evaluation_count": evaluation_count,
        "critical_count": critical_count,
        "avg_score": avg_score,
        "items": replay_items,
    }
