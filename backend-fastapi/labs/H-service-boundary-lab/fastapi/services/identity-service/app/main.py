from __future__ import annotations

from contextlib import asynccontextmanager
from uuid import uuid4

from fastapi import FastAPI, Request

from app.api.v1.router import api_router
from app.bootstrap import initialize_schema
from app.core.config import get_settings
from app.core.errors import register_exception_handlers
from app.core.logging import configure_logging, reset_request_id, set_request_id


class MetricsRegistry:
    def __init__(self) -> None:
        self.request_count = 0

    def increment(self) -> None:
        self.request_count += 1


@asynccontextmanager
async def lifespan(_: FastAPI):
    initialize_schema()
    yield


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging(settings.service_name)
    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        openapi_url=f"{settings.api_v1_prefix}/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )
    app.state.mailbox = []
    app.state.metrics = MetricsRegistry()

    @app.middleware("http")
    async def request_context(request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", str(uuid4()))
        token = set_request_id(request_id)
        app.state.metrics.increment()
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        reset_request_id(token)
        return response

    register_exception_handlers(app)
    app.include_router(api_router, prefix=settings.api_v1_prefix)
    return app


app = create_app()
