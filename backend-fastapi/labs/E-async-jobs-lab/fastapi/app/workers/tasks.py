from __future__ import annotations

from app.db.session import get_session_factory
from app.domain.services.jobs import JobsService
from app.workers.celery_app import celery_app


@celery_app.task(name="jobs.deliver_notification")
def deliver_notification(event_id: str) -> str:
    session = get_session_factory()()
    try:
        service = JobsService(session)
        event = service.process_event(event_id=event_id)
        return event.status
    finally:
        session.close()
