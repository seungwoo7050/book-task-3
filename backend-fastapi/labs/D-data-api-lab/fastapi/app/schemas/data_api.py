from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ProjectCreateRequest(BaseModel):
    title: str
    status: str


class ProjectUpdateRequest(BaseModel):
    version: int
    title: str | None = None
    status: str | None = None


class TaskCreateRequest(BaseModel):
    title: str
    status: str
    priority: int


class CommentCreateRequest(BaseModel):
    body: str


class ProjectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    status: str
    version: int
    deleted_at: datetime | None


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    project_id: str
    title: str
    status: str
    priority: int
    deleted_at: datetime | None


class CommentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    task_id: str
    body: str


class PageResponse(BaseModel):
    items: list[ProjectResponse]
    total: int
    page: int
    page_size: int
