from __future__ import annotations

from typing import Annotated, Any

from fastapi import APIRouter, Depends

from app.api.deps import get_current_claims, get_workspace_service
from app.domain.services.platform import WorkspaceService
from app.schemas.platform import (
    CommentCreateRequest,
    CommentResponse,
    InviteCreateRequest,
    InviteResponse,
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
    claims: Annotated[dict[str, Any], Depends(get_current_claims)],
    service: Annotated[WorkspaceService, Depends(get_workspace_service)],
) -> WorkspaceResponse:
    workspace = service.create_workspace(claims=claims, name=payload.name)
    return WorkspaceResponse(id=workspace.id, name=workspace.name, owner_user_id=workspace.owner_user_id)


@router.post("/workspaces/{workspace_id}/invites", response_model=InviteResponse)
def invite_member(
    workspace_id: str,
    payload: InviteCreateRequest,
    claims: Annotated[dict[str, Any], Depends(get_current_claims)],
    service: Annotated[WorkspaceService, Depends(get_workspace_service)],
) -> InviteResponse:
    invite = service.invite_member(claims=claims, workspace_id=workspace_id, email=payload.email, role=payload.role)
    return InviteResponse(token=invite.token, email=invite.email, role=invite.role, status=invite.status)


@router.post("/invites/{token}/accept", response_model=dict[str, str])
def accept_invite(
    token: str,
    claims: Annotated[dict[str, Any], Depends(get_current_claims)],
    service: Annotated[WorkspaceService, Depends(get_workspace_service)],
) -> dict[str, str]:
    membership = service.accept_invite(claims=claims, token=token)
    return {"workspace_id": membership.workspace_id, "role": membership.role}


@router.post("/workspaces/{workspace_id}/projects", response_model=ProjectResponse)
def create_project(
    workspace_id: str,
    payload: ProjectCreateRequest,
    claims: Annotated[dict[str, Any], Depends(get_current_claims)],
    service: Annotated[WorkspaceService, Depends(get_workspace_service)],
) -> ProjectResponse:
    project = service.create_project(claims=claims, workspace_id=workspace_id, title=payload.title)
    return ProjectResponse(id=project.id, workspace_id=project.workspace_id, title=project.title)


@router.post("/projects/{project_id}/tasks", response_model=TaskResponse)
def create_task(
    project_id: str,
    payload: TaskCreateRequest,
    claims: Annotated[dict[str, Any], Depends(get_current_claims)],
    service: Annotated[WorkspaceService, Depends(get_workspace_service)],
) -> TaskResponse:
    task = service.create_task(claims=claims, project_id=project_id, title=payload.title)
    return TaskResponse(id=task.id, project_id=task.project_id, title=task.title)


@router.post("/tasks/{task_id}/comments", response_model=CommentResponse)
def create_comment(
    task_id: str,
    payload: CommentCreateRequest,
    claims: Annotated[dict[str, Any], Depends(get_current_claims)],
    service: Annotated[WorkspaceService, Depends(get_workspace_service)],
) -> CommentResponse:
    comment = service.create_comment(claims=claims, task_id=task_id, body=payload.body)
    return CommentResponse(id=comment.id, task_id=comment.task_id, author_user_id=comment.author_user_id, body=comment.body)


@router.post("/events/relay", response_model=dict[str, int])
def relay_outbox(service: Annotated[WorkspaceService, Depends(get_workspace_service)]) -> dict[str, int]:
    return {"relayed": service.relay_outbox()}


@router.get("/debug/outbox/pending", response_model=dict[str, int])
def pending_outbox(service: Annotated[WorkspaceService, Depends(get_workspace_service)]) -> dict[str, int]:
    return {"pending": service.pending_outbox()}
