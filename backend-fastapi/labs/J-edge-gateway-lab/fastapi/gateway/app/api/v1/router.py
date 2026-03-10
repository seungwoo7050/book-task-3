from __future__ import annotations

from fastapi import APIRouter

from app.api.v1.routes import auth, health, ops, platform

api_router = APIRouter()
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(ops.router, prefix="/ops", tags=["ops"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(platform.router, prefix="/platform", tags=["platform"])
