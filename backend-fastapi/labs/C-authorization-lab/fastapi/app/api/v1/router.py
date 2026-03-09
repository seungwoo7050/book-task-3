from __future__ import annotations

from fastapi import APIRouter

from app.api.v1.routes import authorization, health

api_router = APIRouter()
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(authorization.router, prefix="/authorization", tags=["authorization"])
