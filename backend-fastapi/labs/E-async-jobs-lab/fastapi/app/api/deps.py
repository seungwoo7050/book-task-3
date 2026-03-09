from __future__ import annotations

from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.domain.services.jobs import JobsService


def get_jobs_service(db: Annotated[Session, Depends(get_db)]) -> JobsService:
    return JobsService(db)
