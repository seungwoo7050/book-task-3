from __future__ import annotations

import json

from redis import Redis
from sqlalchemy.orm import Session

from app.core.config import Settings
from app.db.models.notifications import ConsumerReceipt, Notification
from app.repositories.notifications_repository import NotificationsRepository


class NotificationService:
    def __init__(self, session: Session, settings: Settings) -> None:
        self.session = session
        self.settings = settings
        self.repository = NotificationsRepository(session)
        self.redis = Redis.from_url(settings.redis_url) if settings.redis_url else None

    def consume(self) -> int:
        if self.redis is None:
            return 0
        processed = 0
        entries = self.redis.xread({self.settings.redis_stream_name: "0-0"}, count=100)
        for _, messages in entries:
            for _, raw_fields in messages:
                fields = {self._decode(key): self._decode(value) for key, value in raw_fields.items()}
                event_id = fields["event_id"]
                if self.repository.has_receipt(event_id):
                    continue
                payload = json.loads(fields["payload"])
                notification = Notification(
                    recipient_user_id=payload["recipient_user_id"],
                    message=payload["message"],
                    status="delivered",
                )
                self.repository.save(notification)
                self.repository.save(
                    ConsumerReceipt(
                        event_id=event_id,
                        event_name=fields["event_name"],
                    )
                )
                self.redis.publish(
                    self.settings.redis_pubsub_channel,
                    json.dumps(
                        {
                            "recipient_user_id": payload["recipient_user_id"],
                            "message": payload["message"],
                        }
                    ),
                )
                processed += 1
        self.session.commit()
        return processed

    def list_notifications(self, *, user_id: str) -> list[Notification]:
        return self.repository.list_notifications(user_id)

    @staticmethod
    def _decode(value) -> str:
        return value.decode() if isinstance(value, bytes) else str(value)
