from __future__ import annotations

from fastapi import APIRouter, Request
from fastapi.responses import PlainTextResponse

router = APIRouter()


@router.get("/metrics", response_class=PlainTextResponse)
def metrics(request: Request) -> str:
    total = request.app.state.metrics.request_count
    return f'app_requests_total{{service="identity-service"}} {total}\n'
