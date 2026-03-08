from __future__ import annotations

import time
from datetime import UTC, datetime

from core.errors import DependencyUnavailableError
from db.database import session_scope
from db.models import Conversation, EvaluationJob, EvaluationRun, KnowledgeBaseBundle, Turn
from evaluator.pipeline import EvaluationPipeline
from sqlalchemy import select


def _utc_now() -> datetime:
    return datetime.now(UTC)


def pick_pending_job() -> str | None:
    with session_scope() as session:
        job = session.scalar(
            select(EvaluationJob).where(EvaluationJob.status == "pending").order_by(EvaluationJob.created_at.asc()).limit(1)
        )
        if job is None:
            return None
        return job.id


def run_job(job_id: str) -> EvaluationJob:
    with session_scope() as session:
        job = session.get(EvaluationJob, job_id)
        if job is None:
            raise ValueError(f"job not found: {job_id}")
        run = session.get(EvaluationRun, job.run_id) if job.run_id else None
        bundle = session.get(KnowledgeBaseBundle, job.kb_bundle_id)
        if run is None:
            raise ValueError(f"run not found for job: {job_id}")
        if bundle is None:
            raise ValueError(f"kb bundle not found for job: {job_id}")

        turn_ids = list(
            session.scalars(
                select(Turn.id)
                .join(Conversation, Conversation.id == Turn.conversation_id)
                .where(Conversation.batch_id == job.batch_id)
                .order_by(Conversation.external_id.asc(), Turn.turn_index.asc())
            ).all()
        )
        job.progress_total = len(turn_ids)
        job.progress_completed = 0
        job.status = "running"
        job.error_summary = ""
        job.updated_at = _utc_now()
        session.flush()

        pipeline = EvaluationPipeline(session)
        try:
            for index, turn_id in enumerate(turn_ids, start=1):
                pipeline.evaluate_turn(
                    turn_id,
                    evaluator_version=run.evaluator_version,
                    prompt_version=run.prompt_version,
                    kb_version=run.kb_version,
                    retrieval_version=run.retrieval_version,
                    run=run,
                    kb_bundle_id=bundle.id,
                    allow_cache=False,
                )
                job.progress_completed = index
                job.updated_at = _utc_now()
                session.flush()
            job.status = "completed"
            job.updated_at = _utc_now()
            session.flush()
        except (DependencyUnavailableError, ValueError) as exc:
            job.status = "failed"
            job.error_summary = str(exc)
            job.updated_at = _utc_now()
            session.flush()
        session.refresh(job)
        return job


def run_worker_loop(*, poll_seconds: float, once: bool = False) -> None:
    while True:
        job_id = pick_pending_job()
        if job_id is None:
            if once:
                return
            time.sleep(poll_seconds)
            continue
        run_job(job_id)
        if once:
            return
