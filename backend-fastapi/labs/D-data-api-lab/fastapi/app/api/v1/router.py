from __future__ import annotations

from fastapi import APIRouter

from app.api.v1.routes import data_api, health

api_router = APIRouter()
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(data_api.router, prefix="/data", tags=["data"])
