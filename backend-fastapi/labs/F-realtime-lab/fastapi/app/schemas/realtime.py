from __future__ import annotations

from pydantic import BaseModel


class PresenceHeartbeatRequest(BaseModel):
    user_id: str


class PresenceResponse(BaseModel):
    user_id: str
    online: bool


class NotificationRequest(BaseModel):
    user_id: str
    message: str
