from __future__ import annotations

from uuid import uuid4

from sqlalchemy import String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin


class Notification(TimestampMixin, Base):
    __tablename__ = "notifications"

    id: Mapped[str] = mapped_column(Uuid(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
    recipient_user_id: Mapped[str] = mapped_column(Uuid(as_uuid=False), nullable=False, index=True)
    message: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="delivered")


class ConsumerReceipt(TimestampMixin, Base):
    __tablename__ = "consumer_receipts"

    id: Mapped[str] = mapped_column(Uuid(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
    event_id: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    event_name: Mapped[str] = mapped_column(String(64), nullable=False)
