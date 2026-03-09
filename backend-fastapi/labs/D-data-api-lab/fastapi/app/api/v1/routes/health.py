from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends
from redis import Redis
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import Settings, get_settings
from app.core.errors import AppError
from app.db.session import get_db
from app.schemas.common import HealthResponse

router = APIRouter()


@router.get("/live", response_model=HealthResponse)
def live() -> HealthResponse:
    return HealthResponse(status="ok")


@router.get("/ready", response_model=HealthResponse)
def ready(
    db: Annotated[Session, Depends(get_db)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> HealthResponse:
    try:
        db.execute(text("SELECT 1"))
        if settings.redis_url:
            Redis.from_url(settings.redis_url).ping()
    except Exception as exc:  # pragma: no cover - exercised by smoke checks, not unit tests
        raise AppError(
            code="DEPENDENCY_NOT_READY",
            message="Database or Redis is not ready.",
            status_code=503,
        ) from exc
    return HealthResponse(status="ok")
