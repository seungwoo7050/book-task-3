from __future__ import annotations

from fastapi import Request

from app.runtime import ConnectionManager, PresenceTracker


def get_connection_manager(request: Request) -> ConnectionManager:
    return request.app.state.connection_manager


def get_presence_tracker(request: Request) -> PresenceTracker:
    return request.app.state.presence_tracker
