from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.platform import Invite, Membership, OutboxEvent, Project, Task


class PlatformRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def save(self, entity):
        self.session.add(entity)
        self.session.flush()
        return entity

    def get_membership(self, workspace_id: str, user_id: str) -> Membership | None:
        return self.session.execute(
            select(Membership).where(Membership.workspace_id == workspace_id, Membership.user_id == user_id)
        ).scalar_one_or_none()

    def get_invite(self, token: str) -> Invite | None:
        return self.session.execute(select(Invite).where(Invite.token == token)).scalar_one_or_none()

    def get_project(self, project_id: str) -> Project | None:
        return self.session.get(Project, project_id)

    def get_task(self, task_id: str) -> Task | None:
        return self.session.get(Task, task_id)

    def list_workspace_members(self, workspace_id: str) -> list[Membership]:
        return list(self.session.execute(select(Membership).where(Membership.workspace_id == workspace_id)).scalars())

    def list_pending_outbox(self) -> list[OutboxEvent]:
        return list(self.session.execute(select(OutboxEvent).where(OutboxEvent.status == "queued")).scalars())
