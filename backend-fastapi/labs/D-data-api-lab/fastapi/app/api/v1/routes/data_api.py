from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.api.deps import get_data_service
from app.domain.services.data_api import DataApiService
from app.schemas.data_api import (
    CommentCreateRequest,
    CommentResponse,
    PageResponse,
    ProjectCreateRequest,
    ProjectResponse,
    ProjectUpdateRequest,
    TaskCreateRequest,
    TaskResponse,
)

router = APIRouter()


@router.post("/projects", response_model=ProjectResponse)
def create_project(
    payload: ProjectCreateRequest,
    service: Annotated[DataApiService, Depends(get_data_service)],
) -> ProjectResponse:
    project = service.create_project(title=payload.title, status=payload.status)
    return ProjectResponse.model_validate(project)


@router.get("/projects", response_model=PageResponse)
def list_projects(
    service: Annotated[DataApiService, Depends(get_data_service)],
    status: str | None = None,
    sort: str = "title",
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    include_deleted: bool = False,
) -> PageResponse:
    items, total = service.list_projects(
        status=status,
        sort=sort,
        page=page,
        page_size=page_size,
        include_deleted=include_deleted,
    )
    return PageResponse(
        items=[ProjectResponse.model_validate(item) for item in items],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.patch("/projects/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: str,
    payload: ProjectUpdateRequest,
    service: Annotated[DataApiService, Depends(get_data_service)],
) -> ProjectResponse:
    project = service.update_project(
        project_id=project_id,
        title=payload.title,
        status=payload.status,
        version=payload.version,
    )
    return ProjectResponse.model_validate(project)


@router.delete("/projects/{project_id}", response_model=ProjectResponse)
def delete_project(
    project_id: str,
    service: Annotated[DataApiService, Depends(get_data_service)],
) -> ProjectResponse:
    project = service.delete_project(project_id=project_id)
    return ProjectResponse.model_validate(project)


@router.post("/projects/{project_id}/tasks", response_model=TaskResponse)
def create_task(
    project_id: str,
    payload: TaskCreateRequest,
    service: Annotated[DataApiService, Depends(get_data_service)],
) -> TaskResponse:
    task = service.create_task(
        project_id=project_id,
        title=payload.title,
        status=payload.status,
        priority=payload.priority,
    )
    return TaskResponse.model_validate(task)


@router.post("/tasks/{task_id}/comments", response_model=CommentResponse)
def create_comment(
    task_id: str,
    payload: CommentCreateRequest,
    service: Annotated[DataApiService, Depends(get_data_service)],
) -> CommentResponse:
    comment = service.create_comment(task_id=task_id, body=payload.body)
    return CommentResponse.model_validate(comment)
