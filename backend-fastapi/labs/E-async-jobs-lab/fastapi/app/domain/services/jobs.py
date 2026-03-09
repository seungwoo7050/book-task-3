from __future__ import annotations

from sqlalchemy.orm import Session

from app.core.errors import AppError
from app.db.models.jobs import NotificationJob, OutboxEvent
from app.repositories.jobs_repository import JobsRepository


class JobsService:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.repository = JobsRepository(session)

    def enqueue_notification(self, *, idempotency_key: str, recipient: str, subject: str) -> NotificationJob:
        existing = self.repository.get_job_by_idempotency_key(idempotency_key)
        if existing:
            return existing
        job = NotificationJob(
            idempotency_key=idempotency_key,
            recipient=recipient,
            subject=subject,
            status="queued",
            attempt_count=0,
        )
        self.repository.save(job)
        self.repository.save(OutboxEvent(job_id=job.id, status="pending"))
        self.session.commit()
        self.session.refresh(job)
        return job

    def get_job(self, job_id: str) -> NotificationJob:
        job = self.repository.get_job(job_id)
        if job is None:
            raise AppError(code="JOB_NOT_FOUND", message="Job not found.", status_code=404)
        return job

    def process_event(self, *, event_id: str) -> OutboxEvent:
        event = self.repository.get_outbox_event(event_id)
        if event is None:
            raise AppError(code="EVENT_NOT_FOUND", message="Outbox event not found.", status_code=404)
        job = self.get_job(event.job_id)
        job.attempt_count += 1
        if job.recipient.startswith("retry@") and job.attempt_count == 1:
            job.status = "retrying"
            event.status = "retrying"
            self.session.commit()
            return event
        job.status = "sent"
        event.status = "delivered"
        self.session.commit()
        return event
