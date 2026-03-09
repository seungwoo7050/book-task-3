from __future__ import annotations

import threading
import time

from fastapi import Request
from redis import Redis

from app.core.config import get_settings
from app.core.errors import AppError


class RateLimiter:
    _memory_store: dict[str, tuple[int, float]] = {}
    _memory_lock = threading.Lock()

    def __init__(self, *, limit: int, window_seconds: int, prefix: str) -> None:
        self.limit = limit
        self.window_seconds = window_seconds
        self.prefix = prefix
        settings = get_settings()
        self.redis = Redis.from_url(settings.redis_url) if settings.redis_url else None

    def __call__(self, request: Request) -> None:
        client_ip = request.headers.get(
            "x-forwarded-for", request.client.host if request.client else "unknown"
        )
        key = f"{self.prefix}:{client_ip}"
        count = self._increment(key)
        if count > self.limit:
            raise AppError(
                code="RATE_LIMITED",
                message="Too many requests. Slow down and try again shortly.",
                status_code=429,
                details={
                    "key": self.prefix,
                    "limit": self.limit,
                    "window_seconds": self.window_seconds,
                },
            )

    def _increment(self, key: str) -> int:
        if self.redis is not None:
            pipeline = self.redis.pipeline()
            pipeline.incr(key)
            pipeline.expire(key, self.window_seconds)
            count, _ = pipeline.execute()
            return int(count)

        now = time.monotonic()
        with self._memory_lock:
            count, reset_at = self._memory_store.get(key, (0, now + self.window_seconds))
            if now >= reset_at:
                count = 0
                reset_at = now + self.window_seconds
            count += 1
            self._memory_store[key] = (count, reset_at)
            return count
