from __future__ import annotations

from fastapi import Request

from app.runtime import MetricsRegistry


def get_metrics_registry(request: Request) -> MetricsRegistry:
    return request.app.state.metrics
