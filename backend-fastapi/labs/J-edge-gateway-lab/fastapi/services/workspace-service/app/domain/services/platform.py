from __future__ import annotations

import json
import secrets
from typing import Any

from redis import Redis
from sqlalchemy.orm import Session

from app.core.config import Settings
from app.core.errors import AppError
from app.db.models.platform import Comment, Invite, Membership, OutboxEvent, Project, Task, Workspace
from app.repositories.platform_repository import PlatformRepository


class WorkspaceService:
    def __init__(self, session: Session, settings: Settings) -> None:
        self.session = session
        self.settings = settings
        self.repository = PlatformRepository(session)
        self.redis = Redis.from_url(settings.redis_url) if settings.redis_url else None

    def create_workspace(self, *, claims: dict[str, Any], name: str) -> Workspace:
        workspace = Workspace(name=name, owner_user_id=str(claims["sub"]))
        self.repository.save(workspace)
        self.repository.save(
            Membership(
                user_id=str(claims["sub"]),
                user_email=str(claims["email"]),
                workspace_id=workspace.id,
                role="owner",
            )
        )
        self.session.commit()
        self.session.refresh(workspace)
        return workspace

    def invite_member(self, *, claims: dict[str, Any], workspace_id: str, email: str, role: str) -> Invite:
        membership = self.repository.get_membership(workspace_id, str(claims["sub"]))
        if membership is None or membership.role != "owner":
            raise AppError(code="FORBIDDEN", message="Only workspace owners can invite.", status_code=403)
        invite = Invite(
            workspace_id=workspace_id,
            email=email.lower(),
            role=role,
            token=secrets.token_urlsafe(18),
            status="pending",
        )
        self.repository.save(invite)
        self.session.commit()
        self.session.refresh(invite)
        return invite

    def accept_invite(self, *, claims: dict[str, Any], token: str) -> Membership:
        invite = self.repository.get_invite(token)
        if invite is None or invite.status != "pending":
            raise AppError(code="INVITE_NOT_FOUND", message="Invite not found.", status_code=404)
        if invite.email != str(claims["email"]).lower():
            raise AppError(code="INVITE_EMAIL_MISMATCH", message="Invite email mismatch.", status_code=403)
        invite.status = "accepted"
        membership = Membership(
            user_id=str(claims["sub"]),
            user_email=str(claims["email"]).lower(),
            workspace_id=invite.workspace_id,
            role=invite.role,
        )
        self.repository.save(membership)
        self.session.commit()
        self.session.refresh(membership)
        return membership

    def create_project(self, *, claims: dict[str, Any], workspace_id: str, title: str) -> Project:
        self._require_member(str(claims["sub"]), workspace_id)
        project = Project(workspace_id=workspace_id, title=title)
        self.repository.save(project)
        self.session.commit()
        self.session.refresh(project)
        return project

    def create_task(self, *, claims: dict[str, Any], project_id: str, title: str) -> Task:
        project = self.repository.get_project(project_id)
        if project is None:
            raise AppError(code="PROJECT_NOT_FOUND", message="Project not found.", status_code=404)
        self._require_member(str(claims["sub"]), project.workspace_id)
        task = Task(project_id=project.id, title=title)
        self.repository.save(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def create_comment(self, *, claims: dict[str, Any], task_id: str, body: str) -> Comment:
        task = self.repository.get_task(task_id)
        if task is None:
            raise AppError(code="TASK_NOT_FOUND", message="Task not found.", status_code=404)
        project = self.repository.get_project(task.project_id)
        if project is None:
            raise AppError(code="PROJECT_NOT_FOUND", message="Project not found.", status_code=404)
        actor_id = str(claims["sub"])
        self._require_member(actor_id, project.workspace_id)
        comment = Comment(task_id=task.id, author_user_id=actor_id, body=body)
        self.repository.save(comment)
        message = f"New comment on task {task.title}: {body}"
        for member in self.repository.list_workspace_members(project.workspace_id):
            if member.user_id == actor_id:
                continue
            payload = json.dumps(
                {
                    "message": message,
                    "recipient_user_id": member.user_id,
                    "workspace_id": project.workspace_id,
                    "task_id": task.id,
                }
            )
            self.repository.save(
                OutboxEvent(
                    event_name="comment.created.v1",
                    aggregate_id=comment.id,
                    recipient_user_id=member.user_id,
                    payload=payload,
                    status="queued",
                )
            )
        self.session.commit()
        self.session.refresh(comment)
        return comment

    def relay_outbox(self) -> int:
        events = self.repository.list_pending_outbox()
        for event in events:
            if self.redis is not None:
                self.redis.xadd(
                    self.settings.redis_stream_name,
                    {
                        "event_id": event.id,
                        "event_name": event.event_name,
                        "recipient_user_id": event.recipient_user_id,
                        "payload": event.payload,
                    },
                )
            event.status = "relayed"
        self.session.commit()
        return len(events)

    def pending_outbox(self) -> int:
        return len(self.repository.list_pending_outbox())

    def _require_member(self, user_id: str, workspace_id: str) -> Membership:
        membership = self.repository.get_membership(workspace_id, user_id)
        if membership is None:
            raise AppError(code="FORBIDDEN", message="Workspace membership required.", status_code=403)
        return membership
