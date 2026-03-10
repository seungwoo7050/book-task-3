from __future__ import annotations

from uuid import uuid4

from sqlalchemy import String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin


class Workspace(TimestampMixin, Base):
    __tablename__ = "workspaces"

    id: Mapped[str] = mapped_column(Uuid(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    owner_user_id: Mapped[str] = mapped_column(Uuid(as_uuid=False), nullable=False)


class Membership(TimestampMixin, Base):
    __tablename__ = "memberships"

    id: Mapped[str] = mapped_column(Uuid(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
    user_id: Mapped[str] = mapped_column(Uuid(as_uuid=False), nullable=False)
    user_email: Mapped[str] = mapped_column(String(255), nullable=False)
    workspace_id: Mapped[str] = mapped_column(Uuid(as_uuid=False), nullable=False)
    role: Mapped[str] = mapped_column(String(16), nullable=False)


class Invite(TimestampMixin, Base):
    __tablename__ = "invites"

    id: Mapped[str] = mapped_column(Uuid(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
    workspace_id: Mapped[str] = mapped_column(Uuid(as_uuid=False), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(16), nullable=False)
    token: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="pending")


class Project(TimestampMixin, Base):
    __tablename__ = "projects"

    id: Mapped[str] = mapped_column(Uuid(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
    workspace_id: Mapped[str] = mapped_column(Uuid(as_uuid=False), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)


class Task(TimestampMixin, Base):
    __tablename__ = "tasks"

    id: Mapped[str] = mapped_column(Uuid(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
    project_id: Mapped[str] = mapped_column(Uuid(as_uuid=False), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)


class Comment(TimestampMixin, Base):
    __tablename__ = "comments"

    id: Mapped[str] = mapped_column(Uuid(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
    task_id: Mapped[str] = mapped_column(Uuid(as_uuid=False), nullable=False)
    author_user_id: Mapped[str] = mapped_column(Uuid(as_uuid=False), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)


class OutboxEvent(TimestampMixin, Base):
    __tablename__ = "outbox_events"

    id: Mapped[str] = mapped_column(Uuid(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
    event_name: Mapped[str] = mapped_column(String(64), nullable=False)
    aggregate_id: Mapped[str] = mapped_column(Uuid(as_uuid=False), nullable=False)
    recipient_user_id: Mapped[str] = mapped_column(Uuid(as_uuid=False), nullable=False)
    payload: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="queued")
