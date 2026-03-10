from __future__ import annotations

from contextlib import asynccontextmanager
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import get_settings
from app.core.errors import register_exception_handlers
from app.core.logging import configure_logging, reset_request_id, set_request_id
from app.runtime import ConnectionManager, MetricsRegistry, PresenceTracker, RedisNotificationRelay, ServiceClient


@asynccontextmanager
async def lifespan(app: FastAPI):
    relay = RedisNotificationRelay(
        redis_url=app.state.settings.redis_url,
        channel=app.state.settings.redis_pubsub_channel,
        manager=app.state.connection_manager,
    )
    app.state.relay = relay
    relay.start()
    yield
    relay.stop()


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
    app.state.settings = settings
    app.state.metrics = MetricsRegistry()
    app.state.connection_manager = ConnectionManager()
    app.state.presence_tracker = PresenceTracker(ttl_seconds=settings.presence_ttl_seconds)
    app.state.service_client = ServiceClient(settings)

    @app.middleware("http")
    async def request_context(request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", str(uuid4()))
        request.state.request_id = request_id
        token = set_request_id(request_id)
        app.state.metrics.increment()
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        reset_request_id(token)
        return response

    if settings.allowed_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.allowed_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    register_exception_handlers(app)
    app.include_router(api_router, prefix=settings.api_v1_prefix)
    return app


app = create_app()
