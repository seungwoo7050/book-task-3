from __future__ import annotations

from core.errors import DependencyUnavailableError
from core.json_utils import loads_json
from db.models import Evaluation, Turn
from evaluator.pipeline import EvaluationPipeline, serialize_evaluation
from evaluator.run_registry import create_evaluation_run
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from api.dependencies import get_session
from api.error_responses import dependency_unavailable_response
from api.schemas import EvaluateBatchRequest, EvaluateTurnRequest

router = APIRouter(prefix="/api", tags=["evaluation"])


@router.post("/evaluate/turn/{turn_id}")
def evaluate_turn(
    turn_id: str,
    payload: EvaluateTurnRequest,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    if session.get(Turn, turn_id) is None:
        raise HTTPException(status_code=404, detail="turn not found")

    try:
        pipeline = EvaluationPipeline(session)
        evaluation = pipeline.evaluate_turn(
            turn_id,
            evaluator_version=payload.evaluator_version,
            prompt_version=payload.prompt_version,
            kb_version=payload.kb_version,
            retrieval_version=payload.retrieval_version,
            allow_cache=payload.allow_cache,
        )
        session.commit()
        return {"evaluation": serialize_evaluation(evaluation)}
    except DependencyUnavailableError as exc:
        session.rollback()
        return dependency_unavailable_response(exc)  # type: ignore[return-value]


@router.post("/evaluate/conversation/{conversation_id}")
def evaluate_conversation(conversation_id: str, session: Session = Depends(get_session)) -> dict[str, object]:
    try:
        pipeline = EvaluationPipeline(session)
        evaluations = pipeline.evaluate_conversation(conversation_id)
        session.commit()
        return {"items": [serialize_evaluation(item) for item in evaluations]}
    except DependencyUnavailableError as exc:
        session.rollback()
        return dependency_unavailable_response(exc)  # type: ignore[return-value]


@router.post("/evaluate/batch")
def evaluate_batch(payload: EvaluateBatchRequest, session: Session = Depends(get_session)) -> dict[str, object]:
    try:
        pipeline = EvaluationPipeline(session)
        turn_ids = payload.turn_ids
        if not turn_ids:
            turn_ids = list(session.scalars(select(Turn.id).order_by(Turn.created_at.desc()).limit(50)).all())

        run = create_evaluation_run(
            session,
            run_label=payload.run_label or payload.prompt_version,
            dataset_name=payload.dataset or "batch-evaluate",
            prompt_version=payload.prompt_version,
            kb_version=payload.kb_version,
            evaluator_version=payload.evaluator_version,
            retrieval_version=payload.retrieval_version,
        )
        evaluations = []
        for turn_id in turn_ids:
            evaluation = pipeline.evaluate_turn(
                turn_id,
                evaluator_version=payload.evaluator_version,
                prompt_version=payload.prompt_version,
                kb_version=payload.kb_version,
                retrieval_version=payload.retrieval_version,
                run=run,
                allow_cache=False,
            )
            evaluations.append(evaluation)

        session.commit()
        return {"count": len(evaluations), "items": [serialize_evaluation(item) for item in evaluations]}
    except DependencyUnavailableError as exc:
        session.rollback()
        return dependency_unavailable_response(exc)  # type: ignore[return-value]


@router.get("/evaluations")
def list_evaluations(
    grade: str | None = None,
    failure_type: str | None = None,
    limit: int = 100,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    stmt = select(Evaluation).order_by(Evaluation.created_at.desc()).limit(limit)
    rows = list(session.scalars(stmt).all())

    data = []
    for row in rows:
        failures = loads_json(row.failure_types, [])
        if grade and row.grade != grade:
            continue
        if failure_type and failure_type not in failures:
            continue
        data.append(serialize_evaluation(row))

    return {"items": data}


@router.get("/evaluations/{evaluation_id}")
def get_evaluation(evaluation_id: str, session: Session = Depends(get_session)) -> dict[str, object]:
    row = session.get(Evaluation, evaluation_id)
    if row is None:
        raise HTTPException(status_code=404, detail="evaluation not found")
    return {"evaluation": serialize_evaluation(row)}
