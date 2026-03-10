from __future__ import annotations

from app.db.base import Base
from app.db.models.platform import Comment, Invite, Membership, OutboxEvent, Project, Task, Workspace
from app.db.session import get_engine

__all__ = [
    "Comment",
    "Invite",
    "Membership",
    "OutboxEvent",
    "Project",
    "Task",
    "Workspace",
    "initialize_schema",
]


def initialize_schema() -> None:
    Base.metadata.create_all(bind=get_engine())
