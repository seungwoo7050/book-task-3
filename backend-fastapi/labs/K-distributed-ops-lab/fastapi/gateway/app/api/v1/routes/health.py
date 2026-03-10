from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Request
from redis import Redis

from app.api.deps import get_service_client
from app.core.config import Settings, get_settings
from app.core.errors import AppError
from app.runtime import ServiceClient
from app.schemas.common import HealthResponse

router = APIRouter()


@router.get("/live", response_model=HealthResponse)
def live() -> HealthResponse:
    return HealthResponse(status="ok")


@router.get("/ready", response_model=HealthResponse)
def ready(
    request: Request,
    client: Annotated[ServiceClient, Depends(get_service_client)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> HealthResponse:
    try:
        client.request(request, "identity", "GET", "/health/ready")
        client.request(request, "workspace", "GET", "/health/ready")
        client.request(request, "notification", "GET", "/health/ready")
        if settings.redis_url:
            Redis.from_url(settings.redis_url).ping()
    except Exception as exc:  # pragma: no cover
        raise AppError(code="DEPENDENCY_NOT_READY", message="One or more upstream services are not ready.", status_code=503) from exc
    return HealthResponse(status="ok")
