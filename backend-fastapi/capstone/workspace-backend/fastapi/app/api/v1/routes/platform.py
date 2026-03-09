from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Query, WebSocket, WebSocketDisconnect

from app.api.deps import get_current_user, get_platform_service
from app.core.config import get_settings
from app.core.security import decode_access_token
from app.db.models.auth import User
from app.domain.services.platform import PlatformService
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


@router.post("/workspaces", response_model=WorkspaceResponse)
def create_workspace(
    payload: WorkspaceCreateRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[PlatformService, Depends(get_platform_service)],
) -> WorkspaceResponse:
    workspace = service.create_workspace(user=current_user, name=payload.name)
    return WorkspaceResponse(id=workspace.id, name=workspace.name, owner_user_id=workspace.owner_user_id)


@router.post("/workspaces/{workspace_id}/invites", response_model=InviteResponse)
def invite_member(
    workspace_id: str,
    payload: InviteCreateRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[PlatformService, Depends(get_platform_service)],
) -> InviteResponse:
    invite = service.invite_member(actor=current_user, workspace_id=workspace_id, email=payload.email, role=payload.role)
    return InviteResponse(token=invite.token, email=invite.email, role=invite.role, status=invite.status)


@router.post("/invites/{token}/accept", response_model=dict)
def accept_invite(
    token: str,
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[PlatformService, Depends(get_platform_service)],
) -> dict[str, str]:
    membership = service.accept_invite(actor=current_user, token=token)
    return {"workspace_id": membership.workspace_id, "role": membership.role}


@router.post("/workspaces/{workspace_id}/projects", response_model=ProjectResponse)
def create_project(
    workspace_id: str,
    payload: ProjectCreateRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[PlatformService, Depends(get_platform_service)],
) -> ProjectResponse:
    project = service.create_project(actor=current_user, workspace_id=workspace_id, title=payload.title)
    return ProjectResponse(id=project.id, workspace_id=project.workspace_id, title=project.title)


@router.post("/projects/{project_id}/tasks", response_model=TaskResponse)
def create_task(
    project_id: str,
    payload: TaskCreateRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[PlatformService, Depends(get_platform_service)],
) -> TaskResponse:
    task = service.create_task(actor=current_user, project_id=project_id, title=payload.title)
    return TaskResponse(id=task.id, project_id=task.project_id, title=task.title)


@router.post("/tasks/{task_id}/comments", response_model=CommentResponse)
def create_comment(
    task_id: str,
    payload: CommentCreateRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[PlatformService, Depends(get_platform_service)],
) -> CommentResponse:
    comment = service.create_comment(actor=current_user, task_id=task_id, body=payload.body)
    return CommentResponse(id=comment.id, task_id=comment.task_id, author_user_id=comment.author_user_id, body=comment.body)


@router.post("/notifications/drain", response_model=dict)
async def drain_notifications(
    service: Annotated[PlatformService, Depends(get_platform_service)],
) -> dict[str, int]:
    return {"processed": await service.drain_notifications()}


@router.post("/presence/heartbeat", response_model=PresenceResponse)
def heartbeat(
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[PlatformService, Depends(get_platform_service)],
) -> PresenceResponse:
    service.heartbeat(user_id=current_user.id)
    return PresenceResponse(user_id=current_user.id, online=True)


@router.get("/presence/{user_id}", response_model=PresenceResponse)
def presence(
    user_id: str,
    service: Annotated[PlatformService, Depends(get_platform_service)],
) -> PresenceResponse:
    return PresenceResponse(user_id=user_id, online=service.is_online(user_id=user_id))


@router.websocket("/ws/notifications")
async def notifications_ws(websocket: WebSocket, access_token: str = Query(...)) -> None:
    settings = get_settings()
    payload = decode_access_token(access_token, settings)
    user_id = str(payload["sub"])
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
