from __future__ import annotations

from pydantic import BaseModel


class NotificationResponse(BaseModel):
    id: str
    recipient_user_id: str
    message: str
    status: str
