from __future__ import annotations

from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.session import get_db
from app.domain.services.notifications import NotificationService


def get_notification_service(db: Annotated[Session, Depends(get_db)]) -> NotificationService:
    return NotificationService(db, get_settings())
