from __future__ import annotations

from app.db.base import Base
from app.db.models.notifications import ConsumerReceipt, Notification
from app.db.session import get_engine


def initialize_schema() -> None:
    Base.metadata.create_all(bind=get_engine())


__all__ = ["ConsumerReceipt", "Notification", "initialize_schema"]
