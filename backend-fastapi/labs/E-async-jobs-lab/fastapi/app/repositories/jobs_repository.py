from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.jobs import NotificationJob, OutboxEvent


class JobsRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def save(self, entity):
        self.session.add(entity)
        self.session.flush()
        return entity

    def get_job_by_idempotency_key(self, key: str) -> NotificationJob | None:
        return self.session.execute(
            select(NotificationJob).where(NotificationJob.idempotency_key == key)
        ).scalar_one_or_none()

    def get_job(self, job_id: str) -> NotificationJob | None:
        return self.session.get(NotificationJob, job_id)

    def get_outbox_event(self, event_id: str) -> OutboxEvent | None:
        return self.session.get(OutboxEvent, event_id)

    def list_pending_events(self) -> list[OutboxEvent]:
        return list(
            self.session.execute(
                select(OutboxEvent).where(OutboxEvent.status.in_(["pending", "retrying"]))
            ).scalars()
        )
