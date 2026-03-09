from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.core.errors import AppError
from app.db.models.data import Comment, Project, Task
from app.repositories.data_repository import DataRepository


class DataApiService:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.repository = DataRepository(session)

    def create_project(self, *, title: str, status: str) -> Project:
        project = Project(title=title, status=status, version=1)
        self.repository.save(project)
        self.session.commit()
        self.session.refresh(project)
        return project

    def list_projects(
        self,
        *,
        status: str | None,
        sort: str,
        page: int,
        page_size: int,
        include_deleted: bool,
    ) -> tuple[list[Project], int]:
        return self.repository.list_projects(
            status=status,
            sort=sort,
            page=page,
            page_size=page_size,
            include_deleted=include_deleted,
        )

    def update_project(
        self,
        *,
        project_id: str,
        title: str | None,
        status: str | None,
        version: int,
    ) -> Project:
        project = self.repository.get_project(project_id)
        if project is None or project.deleted_at is not None:
            raise AppError(code="PROJECT_NOT_FOUND", message="Project not found.", status_code=404)
        if project.version != version:
            raise AppError(
                code="VERSION_CONFLICT",
                message="Project version conflict.",
                status_code=409,
            )
        if title is not None:
            project.title = title
        if status is not None:
            project.status = status
        project.version += 1
        self.session.commit()
        self.session.refresh(project)
        return project

    def delete_project(self, *, project_id: str) -> Project:
        project = self.repository.get_project(project_id)
        if project is None:
            raise AppError(code="PROJECT_NOT_FOUND", message="Project not found.", status_code=404)
        project.deleted_at = datetime.now(UTC)
        project.version += 1
        self.session.commit()
        self.session.refresh(project)
        return project

    def create_task(self, *, project_id: str, title: str, status: str, priority: int) -> Task:
        project = self.repository.get_project(project_id)
        if project is None or project.deleted_at is not None:
            raise AppError(code="PROJECT_NOT_FOUND", message="Project not found.", status_code=404)
        task = Task(project_id=project_id, title=title, status=status, priority=priority)
        self.repository.save(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def create_comment(self, *, task_id: str, body: str) -> Comment:
        task = self.repository.get_task(task_id)
        if task is None or task.deleted_at is not None:
            raise AppError(code="TASK_NOT_FOUND", message="Task not found.", status_code=404)
        comment = Comment(task_id=task_id, body=body)
        self.repository.save(comment)
        self.session.commit()
        self.session.refresh(comment)
        return comment
