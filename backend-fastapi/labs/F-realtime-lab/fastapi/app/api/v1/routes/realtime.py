from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Query, WebSocket, WebSocketDisconnect

from app.api.deps import get_connection_manager, get_presence_tracker
from app.runtime import ConnectionManager, PresenceTracker
from app.schemas.realtime import NotificationRequest, PresenceHeartbeatRequest, PresenceResponse

router = APIRouter()


@router.post("/presence/heartbeat", response_model=PresenceResponse)
def heartbeat(
    payload: PresenceHeartbeatRequest,
    tracker: Annotated[PresenceTracker, Depends(get_presence_tracker)],
) -> PresenceResponse:
    tracker.heartbeat(payload.user_id)
    return PresenceResponse(user_id=payload.user_id, online=True)


@router.get("/presence/{user_id}", response_model=PresenceResponse)
def get_presence(
    user_id: str,
    tracker: Annotated[PresenceTracker, Depends(get_presence_tracker)],
) -> PresenceResponse:
    return PresenceResponse(user_id=user_id, online=tracker.is_online(user_id))


@router.post("/notifications", response_model=dict)
async def send_notification(
    payload: NotificationRequest,
    manager: Annotated[ConnectionManager, Depends(get_connection_manager)],
) -> dict[str, str]:
    await manager.send_notification(user_id=payload.user_id, payload={"message": payload.message})
    return {"status": "sent"}


@router.websocket("/ws/notifications/{user_id}")
async def notifications_ws(
    websocket: WebSocket,
    user_id: str,
    token: str = Query(...),
) -> None:
    manager: ConnectionManager = websocket.app.state.connection_manager
    tracker: PresenceTracker = websocket.app.state.presence_tracker
    try:
        await manager.connect(user_id=user_id, token=token, websocket=websocket)
        tracker.heartbeat(user_id)
        while True:
            await websocket.receive_text()
            tracker.heartbeat(user_id)
    except PermissionError:
        return
    except WebSocketDisconnect:
        manager.disconnect(user_id=user_id, websocket=websocket)
