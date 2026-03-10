from __future__ import annotations

import json
import logging
from contextvars import ContextVar
from datetime import UTC, datetime

service_name_ctx: ContextVar[str] = ContextVar("service_name", default="unknown")
request_id_ctx: ContextVar[str] = ContextVar("request_id", default="-")


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "service": service_name_ctx.get(),
            "request_id": request_id_ctx.get(),
            "message": record.getMessage(),
        }
        return json.dumps(payload)


def configure_logging(service_name: str) -> None:
    service_name_ctx.set(service_name)
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(logging.INFO)


def set_request_id(request_id: str):
    return request_id_ctx.set(request_id)


def reset_request_id(token) -> None:
    request_id_ctx.reset(token)
