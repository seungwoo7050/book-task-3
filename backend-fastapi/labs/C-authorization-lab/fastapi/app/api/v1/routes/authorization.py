from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps import get_actor_id, get_authorization_service
from app.domain.services.authorization import AuthorizationService
from app.schemas.authorization import (
    CreateDocumentRequest,
    CreateInviteRequest,
    CreateUserRequest,
    CreateWorkspaceRequest,
    DocumentResponse,
    InviteResponse,
    MembershipResponse,
    RoleChangeRequest,
    UserResponse,
    WorkspaceResponse,
)

router = APIRouter()


@router.post("/users", response_model=UserResponse)
def create_user(
    payload: CreateUserRequest,
    service: Annotated[AuthorizationService, Depends(get_authorization_service)],
) -> UserResponse:
    user = service.create_user(email=payload.email, name=payload.name)
    return UserResponse(id=user.id, email=user.email, name=user.name)


@router.post("/workspaces", response_model=WorkspaceResponse)
def create_workspace(
    payload: CreateWorkspaceRequest,
    actor_id: Annotated[str, Depends(get_actor_id)],
    service: Annotated[AuthorizationService, Depends(get_authorization_service)],
) -> WorkspaceResponse:
    workspace = service.create_workspace(actor_id=actor_id, name=payload.name)
    return WorkspaceResponse(
        id=workspace.id,
        name=workspace.name,
        owner_user_id=workspace.owner_user_id,
    )


@router.post("/workspaces/{workspace_id}/invites", response_model=InviteResponse)
def create_invite(
    workspace_id: str,
    payload: CreateInviteRequest,
    actor_id: Annotated[str, Depends(get_actor_id)],
    service: Annotated[AuthorizationService, Depends(get_authorization_service)],
) -> InviteResponse:
    invite = service.create_invite(
        actor_id=actor_id,
        workspace_id=workspace_id,
        email=payload.email,
        role=payload.role,
    )
    return InviteResponse(
        token=invite.token,
        status=invite.status,
        email=invite.email,
        role=invite.role,
    )


@router.post("/invites/{token}/accept", response_model=MembershipResponse)
def accept_invite(
    token: str,
    actor_id: Annotated[str, Depends(get_actor_id)],
    service: Annotated[AuthorizationService, Depends(get_authorization_service)],
) -> MembershipResponse:
    membership = service.accept_invite(actor_id=actor_id, token=token)
    return MembershipResponse(
        user_id=membership.user_id,
        workspace_id=membership.workspace_id,
        role=membership.role,
    )


@router.post("/invites/{token}/decline", response_model=InviteResponse)
def decline_invite(
    token: str,
    actor_id: Annotated[str, Depends(get_actor_id)],
    service: Annotated[AuthorizationService, Depends(get_authorization_service)],
) -> InviteResponse:
    invite = service.decline_invite(actor_id=actor_id, token=token)
    return InviteResponse(
        token=invite.token,
        status=invite.status,
        email=invite.email,
        role=invite.role,
    )


@router.patch("/workspaces/{workspace_id}/members/{user_id}", response_model=MembershipResponse)
def change_role(
    workspace_id: str,
    user_id: str,
    payload: RoleChangeRequest,
    actor_id: Annotated[str, Depends(get_actor_id)],
    service: Annotated[AuthorizationService, Depends(get_authorization_service)],
) -> MembershipResponse:
    membership = service.change_role(
        actor_id=actor_id,
        workspace_id=workspace_id,
        target_user_id=user_id,
        role=payload.role,
    )
    return MembershipResponse(
        user_id=membership.user_id,
        workspace_id=membership.workspace_id,
        role=membership.role,
    )


@router.post("/workspaces/{workspace_id}/documents", response_model=DocumentResponse)
def create_document(
    workspace_id: str,
    payload: CreateDocumentRequest,
    actor_id: Annotated[str, Depends(get_actor_id)],
    service: Annotated[AuthorizationService, Depends(get_authorization_service)],
) -> DocumentResponse:
    document = service.create_document(
        actor_id=actor_id,
        workspace_id=workspace_id,
        title=payload.title,
    )
    return DocumentResponse(
        id=document.id,
        workspace_id=document.workspace_id,
        owner_user_id=document.owner_user_id,
        title=document.title,
    )


@router.get("/documents/{document_id}", response_model=DocumentResponse)
def get_document(
    document_id: str,
    actor_id: Annotated[str, Depends(get_actor_id)],
    service: Annotated[AuthorizationService, Depends(get_authorization_service)],
) -> DocumentResponse:
    document = service.get_document(actor_id=actor_id, document_id=document_id)
    return DocumentResponse(
        id=document.id,
        workspace_id=document.workspace_id,
        owner_user_id=document.owner_user_id,
        title=document.title,
    )
