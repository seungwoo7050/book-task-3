from __future__ import annotations

from pydantic import BaseModel, EmailStr


class WorkspaceCreateRequest(BaseModel):
    name: str


class InviteCreateRequest(BaseModel):
    email: EmailStr
    role: str


class ProjectCreateRequest(BaseModel):
    title: str


class TaskCreateRequest(BaseModel):
    title: str


class CommentCreateRequest(BaseModel):
    body: str


class WorkspaceResponse(BaseModel):
    id: str
    name: str
    owner_user_id: str


class InviteResponse(BaseModel):
    token: str
    email: EmailStr
    role: str
    status: str


class ProjectResponse(BaseModel):
    id: str
    workspace_id: str
    title: str


class TaskResponse(BaseModel):
    id: str
    project_id: str
    title: str


class CommentResponse(BaseModel):
    id: str
    task_id: str
    author_user_id: str
    body: str


class PresenceResponse(BaseModel):
    user_id: str
    online: bool
