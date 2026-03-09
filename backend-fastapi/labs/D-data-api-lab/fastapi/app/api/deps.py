from __future__ import annotations

from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.domain.services.data_api import DataApiService


def get_data_service(db: Annotated[Session, Depends(get_db)]) -> DataApiService:
    return DataApiService(db)
