from __future__ import annotations

from app.db.base import Base
from app.db.models import NotificationJob, OutboxEvent
from app.db.session import get_engine

__all__ = [
    "NotificationJob",
    "OutboxEvent",
    "initialize_schema",
]


def initialize_schema() -> None:
    Base.metadata.create_all(bind=get_engine())
