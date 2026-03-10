from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.errors import AppError
from app.db.session import get_db
from app.schemas.common import HealthResponse

router = APIRouter()


@router.get("/live", response_model=HealthResponse)
def live() -> HealthResponse:
    return HealthResponse(status="ok")


@router.get("/ready", response_model=HealthResponse)
def ready(db: Annotated[Session, Depends(get_db)]) -> HealthResponse:
    try:
        db.execute(text("SELECT 1"))
    except Exception as exc:  # pragma: no cover
        raise AppError(code="DEPENDENCY_NOT_READY", message="Database is not ready.", status_code=503) from exc
    return HealthResponse(status="ok")
