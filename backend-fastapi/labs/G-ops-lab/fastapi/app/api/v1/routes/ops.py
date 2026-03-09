from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Response

from app.api.deps import get_metrics_registry
from app.core.config import get_settings
from app.runtime import MetricsRegistry

router = APIRouter()


@router.get("/ready", response_model=dict)
def ready() -> dict[str, object]:
    settings = get_settings()
    return {
        "status": "ok",
        "checks": {
            "database": "configured" if settings.database_url else "missing",
            "redis": "configured" if settings.redis_url else "skipped",
        },
    }


@router.get("/metrics")
def metrics(
    registry: Annotated[MetricsRegistry, Depends(get_metrics_registry)],
) -> Response:
    body = (
        "# HELP app_requests_total Total HTTP requests handled\n"
        "# TYPE app_requests_total counter\n"
        f"app_requests_total {registry.request_count}\n"
    )
    return Response(content=body, media_type="text/plain; version=0.0.4")
