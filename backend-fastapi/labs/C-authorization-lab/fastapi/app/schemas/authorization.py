from __future__ import annotations

from pydantic import BaseModel, EmailStr


class CreateUserRequest(BaseModel):
    email: EmailStr
    name: str


class CreateWorkspaceRequest(BaseModel):
    name: str


class CreateInviteRequest(BaseModel):
    email: EmailStr
    role: str


class RoleChangeRequest(BaseModel):
    role: str


class CreateDocumentRequest(BaseModel):
    title: str


class UserResponse(BaseModel):
    id: str
    email: EmailStr
    name: str


class WorkspaceResponse(BaseModel):
    id: str
    name: str
    owner_user_id: str


class InviteResponse(BaseModel):
    token: str
    status: str
    email: EmailStr
    role: str


class MembershipResponse(BaseModel):
    user_id: str
    workspace_id: str
    role: str


class DocumentResponse(BaseModel):
    id: str
    workspace_id: str
    owner_user_id: str
    title: str
