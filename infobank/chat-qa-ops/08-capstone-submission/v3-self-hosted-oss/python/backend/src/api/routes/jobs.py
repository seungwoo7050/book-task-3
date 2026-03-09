from __future__ import annotations

import uuid
from datetime import UTC, datetime

from core.config import load_settings
from db.models import (
    AdminUser,
    Conversation,
    ConversationBatch,
    Evaluation,
    EvaluationJob,
    EvaluationRun,
    KnowledgeBaseBundle,
    Turn,
)
from evaluator.run_registry import create_evaluation_run
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from api.dependencies import get_current_admin, get_session
from api.schemas import JobCreateRequest

router = APIRouter(prefix="/api/jobs", tags=["jobs"])


def _serialize_job(session: Session, job: EvaluationJob) -> dict[str, object]:
    run = session.get(EvaluationRun, job.run_id) if job.run_id else None
    batch = session.get(ConversationBatch, job.batch_id)
    bundle = session.get(KnowledgeBaseBundle, job.kb_bundle_id)
    evaluation_count = 0
    avg_score = 0.0
    critical_count = 0
    if run is not None:
        rows = list(session.scalars(select(Evaluation).where(Evaluation.run_id == run.id)).all())
        evaluation_count = len(rows)
        if rows:
            avg_score = round(sum(item.total_score for item in rows) / len(rows), 2)
            critical_count = sum(1 for item in rows if item.is_critical)
    return {
        "id": job.id,
        "status": job.status,
        "progress_completed": job.progress_completed,
        "progress_total": job.progress_total,
        "error_summary": job.error_summary,
        "run_id": job.run_id,
        "run_label": run.run_label if run is not None else None,
        "dataset_id": job.batch_id,
        "dataset_name": batch.name if batch is not None else None,
        "kb_bundle_id": job.kb_bundle_id,
        "kb_bundle_name": bundle.name if bundle is not None else None,
        "evaluation_count": evaluation_count,
        "avg_score": avg_score,
        "critical_count": critical_count,
        "created_at": job.created_at.isoformat(),
        "updated_at": job.updated_at.isoformat(),
    }


@router.get("")
def list_jobs(
    _: AdminUser = Depends(get_current_admin),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    rows = list(session.scalars(select(EvaluationJob).order_by(EvaluationJob.created_at.desc())).all())
    return {"items": [_serialize_job(session, row) for row in rows]}


@router.post("")
def create_job(
    payload: JobCreateRequest,
    _: AdminUser = Depends(get_current_admin),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    settings = load_settings()
    batch = session.get(ConversationBatch, payload.dataset_id)
    bundle = session.get(KnowledgeBaseBundle, payload.kb_bundle_id)
    if batch is None:
        raise HTTPException(status_code=404, detail="dataset not found")
    if bundle is None:
        raise HTTPException(status_code=404, detail="kb bundle not found")

    run = create_evaluation_run(
        session,
        batch_id=batch.id,
        kb_bundle_id=bundle.id,
        run_label=payload.run_label or f"{batch.name}-{datetime.now(UTC).strftime('%Y%m%d-%H%M%S')}",
        dataset_name=batch.name,
        baseline_label=payload.baseline_label,
        candidate_label=payload.candidate_label,
        prompt_version=payload.prompt_version or settings.prompt_version,
        kb_version=payload.kb_version or settings.kb_version,
        evaluator_version=payload.evaluator_version or settings.evaluator_version,
        retrieval_version=payload.retrieval_version or settings.retrieval_version,
    )

    job = EvaluationJob(
        id=str(uuid.uuid4()),
        run_id=run.id,
        batch_id=batch.id,
        kb_bundle_id=bundle.id,
        status="pending",
        progress_completed=0,
        progress_total=int(
            session.scalar(
                select(func.count(Turn.id))
                .join_from(Turn, Conversation, Conversation.id == Turn.conversation_id)
                .where(Conversation.batch_id == batch.id)
            )
            or 0
        ),
        metadata_json="{}",
        error_summary="",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    session.add(job)
    session.flush()
    run.job_id = job.id
    session.commit()
    return {"job": _serialize_job(session, job)}


@router.get("/{job_id}")
def get_job(
    job_id: str,
    _: AdminUser = Depends(get_current_admin),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    row = session.get(EvaluationJob, job_id)
    if row is None:
        raise HTTPException(status_code=404, detail="job not found")
    return {"job": _serialize_job(session, row)}
