from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.notifications import ConsumerReceipt, Notification


class NotificationsRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def save(self, entity):
        self.session.add(entity)
        self.session.flush()
        return entity

    def has_receipt(self, event_id: str) -> bool:
        return self.session.execute(select(ConsumerReceipt).where(ConsumerReceipt.event_id == event_id)).scalar_one_or_none() is not None

    def list_notifications(self, user_id: str) -> list[Notification]:
        return list(self.session.execute(select(Notification).where(Notification.recipient_user_id == user_id)).scalars())
