from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request, WebSocket, WebSocketDisconnect

from app.api.deps import get_current_claims, get_service_client
from app.runtime import ServiceClient
from app.schemas.platform import (
    CommentCreateRequest,
    CommentResponse,
    InviteCreateRequest,
    InviteResponse,
    PresenceResponse,
    ProjectCreateRequest,
    ProjectResponse,
    TaskCreateRequest,
    TaskResponse,
    WorkspaceCreateRequest,
    WorkspaceResponse,
)

router = APIRouter()


def _auth_headers(request: Request) -> dict[str, str]:
    access_token = request.cookies.get("access_token", "")
    return {"Authorization": f"Bearer {access_token}"}


@router.post("/workspaces", response_model=WorkspaceResponse)
def create_workspace(
    payload: WorkspaceCreateRequest,
    request: Request,
    _: Annotated[dict[str, str], Depends(get_current_claims)],
    client: Annotated[ServiceClient, Depends(get_service_client)],
) -> WorkspaceResponse:
    data = client.request(request, "workspace", "POST", "/internal/workspaces", json=payload.model_dump(mode="json"), headers=_auth_headers(request))
    return WorkspaceResponse(**data)


@router.post("/workspaces/{workspace_id}/invites", response_model=InviteResponse)
def invite_member(
    workspace_id: str,
    payload: InviteCreateRequest,
    request: Request,
    _: Annotated[dict[str, str], Depends(get_current_claims)],
    client: Annotated[ServiceClient, Depends(get_service_client)],
) -> InviteResponse:
    data = client.request(
        request,
        "workspace",
        "POST",
        f"/internal/workspaces/{workspace_id}/invites",
        json=payload.model_dump(mode="json"),
        headers=_auth_headers(request),
    )
    return InviteResponse(**data)


@router.post("/invites/{token}/accept", response_model=dict[str, str])
def accept_invite(
    token: str,
    request: Request,
    _: Annotated[dict[str, str], Depends(get_current_claims)],
    client: Annotated[ServiceClient, Depends(get_service_client)],
) -> dict[str, str]:
    return client.request(request, "workspace", "POST", f"/internal/invites/{token}/accept", headers=_auth_headers(request))


@router.post("/workspaces/{workspace_id}/projects", response_model=ProjectResponse)
def create_project(
    workspace_id: str,
    payload: ProjectCreateRequest,
    request: Request,
    _: Annotated[dict[str, str], Depends(get_current_claims)],
    client: Annotated[ServiceClient, Depends(get_service_client)],
) -> ProjectResponse:
    data = client.request(
        request,
        "workspace",
        "POST",
        f"/internal/workspaces/{workspace_id}/projects",
        json=payload.model_dump(mode="json"),
        headers=_auth_headers(request),
    )
    return ProjectResponse(**data)


@router.post("/projects/{project_id}/tasks", response_model=TaskResponse)
def create_task(
    project_id: str,
    payload: TaskCreateRequest,
    request: Request,
    _: Annotated[dict[str, str], Depends(get_current_claims)],
    client: Annotated[ServiceClient, Depends(get_service_client)],
) -> TaskResponse:
    data = client.request(
        request,
        "workspace",
        "POST",
        f"/internal/projects/{project_id}/tasks",
        json=payload.model_dump(mode="json"),
        headers=_auth_headers(request),
    )
    return TaskResponse(**data)


@router.post("/tasks/{task_id}/comments", response_model=CommentResponse)
def create_comment(
    task_id: str,
    payload: CommentCreateRequest,
    request: Request,
    _: Annotated[dict[str, str], Depends(get_current_claims)],
    client: Annotated[ServiceClient, Depends(get_service_client)],
) -> CommentResponse:
    data = client.request(
        request,
        "workspace",
        "POST",
        f"/internal/tasks/{task_id}/comments",
        json=payload.model_dump(mode="json"),
        headers=_auth_headers(request),
    )
    return CommentResponse(**data)


@router.post("/notifications/drain", response_model=dict[str, int])
def drain_notifications(
    request: Request,
    client: Annotated[ServiceClient, Depends(get_service_client)],
) -> dict[str, int]:
    relayed = client.request(request, "workspace", "POST", "/internal/events/relay")
    processed = client.request(request, "notification", "POST", "/internal/notifications/consume")
    return {"relayed": relayed["relayed"], "processed": processed["processed"]}


@router.post("/presence/heartbeat", response_model=PresenceResponse)
def heartbeat(
    claims: Annotated[dict[str, str], Depends(get_current_claims)],
    request: Request,
) -> PresenceResponse:
    request.app.state.presence_tracker.heartbeat(str(claims["sub"]))
    return PresenceResponse(user_id=str(claims["sub"]), online=True)


@router.get("/presence/{user_id}", response_model=PresenceResponse)
def presence(user_id: str, request: Request) -> PresenceResponse:
    return PresenceResponse(user_id=user_id, online=request.app.state.presence_tracker.is_online(user_id))


@router.websocket("/ws/notifications")
async def notifications_ws(websocket: WebSocket, access_token: str = Query(...)) -> None:
    settings = websocket.app.state.settings
    claims = websocket.app.state.service_client.decode_access(access_token, settings)
    user_id = str(claims["sub"])
    manager = websocket.app.state.connection_manager
    presence = websocket.app.state.presence_tracker
    await manager.connect(user_id=user_id, websocket=websocket)
    presence.heartbeat(user_id)
    try:
        while True:
            await websocket.receive_text()
            presence.heartbeat(user_id)
    except WebSocketDisconnect:
        manager.disconnect(user_id=user_id, websocket=websocket)
