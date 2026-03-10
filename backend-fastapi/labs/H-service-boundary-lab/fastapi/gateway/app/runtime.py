from __future__ import annotations

import asyncio
import json
import threading
import time
from collections import defaultdict
from collections.abc import Mapping
from typing import Any

import httpx
from fastapi import Request, WebSocket
from redis import Redis

from app.core.errors import AppError
from app.core.security import decode_access_token


class MetricsRegistry:
    def __init__(self) -> None:
        self.request_count = 0

    def increment(self) -> None:
        self.request_count += 1


class ConnectionManager:
    def __init__(self) -> None:
        self.connections: dict[str, set[WebSocket]] = defaultdict(set)
        self.loop: asyncio.AbstractEventLoop | None = None

    async def connect(self, *, user_id: str, websocket: WebSocket) -> None:
        self.loop = asyncio.get_running_loop()
        await websocket.accept()
        self.connections[user_id].add(websocket)

    def disconnect(self, *, user_id: str, websocket: WebSocket) -> None:
        self.connections[user_id].discard(websocket)

    async def send_notification(self, *, user_id: str, payload: dict[str, str]) -> None:
        for websocket in list(self.connections[user_id]):
            await websocket.send_json(payload)

    def dispatch_from_thread(self, *, user_id: str, payload: dict[str, str]) -> None:
        if self.loop is None:
            return
        asyncio.run_coroutine_threadsafe(self.send_notification(user_id=user_id, payload=payload), self.loop)


class PresenceTracker:
    def __init__(self, *, ttl_seconds: int) -> None:
        self.ttl_seconds = ttl_seconds
        self.last_seen: dict[str, float] = {}

    def heartbeat(self, user_id: str) -> None:
        self.last_seen[user_id] = time.monotonic()

    def is_online(self, user_id: str) -> bool:
        seen_at = self.last_seen.get(user_id)
        return seen_at is not None and (time.monotonic() - seen_at) < self.ttl_seconds


class RedisNotificationRelay:
    def __init__(self, *, redis_url: str | None, channel: str, manager: ConnectionManager) -> None:
        self.redis_url = redis_url
        self.channel = channel
        self.manager = manager
        self.stop_event = threading.Event()
        self.thread: threading.Thread | None = None

    def start(self) -> None:
        if not self.redis_url:
            return
        self.thread = threading.Thread(target=self._listen, daemon=True)
        self.thread.start()

    def stop(self) -> None:
        self.stop_event.set()
        if self.thread is not None:
            self.thread.join(timeout=1)

    def _listen(self) -> None:
        client = Redis.from_url(self.redis_url)
        pubsub = client.pubsub(ignore_subscribe_messages=True)
        pubsub.subscribe(self.channel)
        while not self.stop_event.is_set():
            message = pubsub.get_message(timeout=1.0)
            if not message or message["type"] != "message":
                continue
            payload = json.loads(message["data"].decode() if isinstance(message["data"], bytes) else message["data"])
            self.manager.dispatch_from_thread(user_id=str(payload["recipient_user_id"]), payload={"message": payload["message"]})
        pubsub.close()


class ServiceClient:
    def __init__(self, settings) -> None:
        self.settings = settings
        self.base_urls = {
            "identity": settings.identity_service_url,
            "workspace": settings.workspace_service_url,
            "notification": settings.notification_service_url,
        }

    def request(
        self,
        request: Request,
        service: str,
        method: str,
        path: str,
        *,
        json: Mapping[str, Any] | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> dict[str, Any]:
        outgoing_headers = {"X-Request-ID": request.state.request_id}
        if headers:
            outgoing_headers.update(headers)
        try:
            with httpx.Client(base_url=self.base_urls[service], timeout=self.settings.request_timeout_seconds) as client:
                response = client.request(method, path, json=json, headers=outgoing_headers)
        except httpx.RequestError as exc:
            raise AppError(
                code="UPSTREAM_UNAVAILABLE",
                message=f"{service} service is unavailable.",
                status_code=503,
                details={"service": service},
            ) from exc
        if response.status_code >= 400:
            payload = response.json()
            error = payload.get("error", {})
            raise AppError(
                code=error.get("code", "UPSTREAM_ERROR"),
                message=error.get("message", f"{service} request failed."),
                status_code=response.status_code,
                details={"service": service},
            )
        if not response.content:
            return {}
        return response.json()

    @staticmethod
    def decode_access(token: str, settings) -> dict[str, Any]:
        return decode_access_token(token, settings)
