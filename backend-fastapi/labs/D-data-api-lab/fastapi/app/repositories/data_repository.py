from __future__ import annotations

from sqlalchemy import asc, desc, func, select
from sqlalchemy.orm import Session

from app.db.models.data import Project, Task


class DataRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def save(self, entity):
        self.session.add(entity)
        self.session.flush()
        return entity

    def get_project(self, project_id: str) -> Project | None:
        return self.session.get(Project, project_id)

    def list_projects(
        self,
        *,
        status: str | None,
        sort: str,
        page: int,
        page_size: int,
        include_deleted: bool,
    ) -> tuple[list[Project], int]:
        stmt = select(Project)
        count_stmt = select(func.count(Project.id))
        if status:
            stmt = stmt.where(Project.status == status)
            count_stmt = count_stmt.where(Project.status == status)
        if not include_deleted:
            stmt = stmt.where(Project.deleted_at.is_(None))
            count_stmt = count_stmt.where(Project.deleted_at.is_(None))

        order = desc(Project.title) if sort == "-title" else asc(Project.title)
        stmt = stmt.order_by(order).offset((page - 1) * page_size).limit(page_size)
        items = list(self.session.execute(stmt).scalars())
        total = int(self.session.execute(count_stmt).scalar_one())
        return items, total

    def get_task(self, task_id: str) -> Task | None:
        return self.session.get(Task, task_id)
