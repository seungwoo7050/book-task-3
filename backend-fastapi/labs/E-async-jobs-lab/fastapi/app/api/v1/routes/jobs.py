from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Header

from app.api.deps import get_jobs_service
from app.domain.services.jobs import JobsService
from app.repositories.jobs_repository import JobsRepository
from app.schemas.jobs import DrainResponse, JobCreateRequest, JobResponse
from app.workers.tasks import deliver_notification

router = APIRouter()


@router.post("/notifications", response_model=JobResponse)
def enqueue_notification(
    payload: JobCreateRequest,
    service: Annotated[JobsService, Depends(get_jobs_service)],
    idempotency_key: Annotated[str, Header(alias="Idempotency-Key")],
) -> JobResponse:
    job = service.enqueue_notification(
        idempotency_key=idempotency_key,
        recipient=payload.recipient,
        subject=payload.subject,
    )
    return JobResponse.model_validate(job)


@router.post("/outbox/drain", response_model=DrainResponse)
def drain_outbox(service: Annotated[JobsService, Depends(get_jobs_service)]) -> DrainResponse:
    repository = JobsRepository(service.session)
    dispatched = []
    for event in repository.list_pending_events():
        dispatched.append(deliver_notification.delay(event.id).get())
    return DrainResponse(processed=len(dispatched), statuses=dispatched)


@router.get("/notifications/{job_id}", response_model=JobResponse)
def get_job(
    job_id: str,
    service: Annotated[JobsService, Depends(get_jobs_service)],
) -> JobResponse:
    job = service.get_job(job_id)
    return JobResponse.model_validate(job)
