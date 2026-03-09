from __future__ import annotations

from app.db.base import Base
from app.db.models import AuthAuditLog, EmailToken, RefreshToken, User
from app.db.session import get_engine

__all__ = [
    "AuthAuditLog",
    "EmailToken",
    "RefreshToken",
    "User",
    "initialize_schema",
]


def initialize_schema() -> None:
    Base.metadata.create_all(bind=get_engine())
