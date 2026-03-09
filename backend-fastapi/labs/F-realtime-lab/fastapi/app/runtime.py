from __future__ import annotations

import time
from collections import defaultdict

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self) -> None:
        self.connections: dict[str, set[WebSocket]] = defaultdict(set)

    async def connect(self, *, user_id: str, token: str, websocket: WebSocket) -> None:
        if token != user_id:
            await websocket.close(code=1008)
            raise PermissionError("invalid websocket token")
        await websocket.accept()
        self.connections[user_id].add(websocket)

    def disconnect(self, *, user_id: str, websocket: WebSocket) -> None:
        self.connections[user_id].discard(websocket)

    async def send_notification(self, *, user_id: str, payload: dict[str, str]) -> None:
        for websocket in list(self.connections[user_id]):
            await websocket.send_json(payload)


class PresenceTracker:
    def __init__(self, *, ttl_seconds: int) -> None:
        self.ttl_seconds = ttl_seconds
        self.last_seen: dict[str, float] = {}

    def heartbeat(self, user_id: str) -> None:
        self.last_seen[user_id] = time.monotonic()

    def is_online(self, user_id: str) -> bool:
        seen_at = self.last_seen.get(user_id)
        return seen_at is not None and (time.monotonic() - seen_at) < self.ttl_seconds
