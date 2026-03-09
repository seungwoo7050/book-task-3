from __future__ import annotations

import secrets

from sqlalchemy.orm import Session

from app.core.errors import AppError
from app.db.models.auth import User
from app.db.models.platform import Comment, Invite, Membership, Notification, Project, Task, Workspace
from app.repositories.platform_repository import PlatformRepository
from app.runtime import ConnectionManager, PresenceTracker


class PlatformService:
    def __init__(self, session: Session, manager: ConnectionManager, presence: PresenceTracker) -> None:
        self.session = session
        self.repository = PlatformRepository(session)
        self.manager = manager
        self.presence = presence

    def create_workspace(self, *, user: User, name: str) -> Workspace:
        workspace = Workspace(name=name, owner_user_id=user.id)
        self.repository.save(workspace)
        self.repository.save(Membership(user_id=user.id, workspace_id=workspace.id, role="owner"))
        self.session.commit()
        self.session.refresh(workspace)
        return workspace

    def invite_member(self, *, actor: User, workspace_id: str, email: str, role: str) -> Invite:
        membership = self.repository.get_membership(workspace_id, actor.id)
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

    def accept_invite(self, *, actor: User, token: str) -> Membership:
        invite = self.repository.get_invite(token)
        if invite is None or invite.status != "pending":
            raise AppError(code="INVITE_NOT_FOUND", message="Invite not found.", status_code=404)
        if invite.email != actor.email:
            raise AppError(code="INVITE_EMAIL_MISMATCH", message="Invite email mismatch.", status_code=403)
        invite.status = "accepted"
        membership = Membership(user_id=actor.id, workspace_id=invite.workspace_id, role=invite.role)
        self.repository.save(membership)
        self.session.commit()
        self.session.refresh(membership)
        return membership

    def create_project(self, *, actor: User, workspace_id: str, title: str) -> Project:
        self._require_member(actor.id, workspace_id)
        project = Project(workspace_id=workspace_id, title=title)
        self.repository.save(project)
        self.session.commit()
        self.session.refresh(project)
        return project

    def create_task(self, *, actor: User, project_id: str, title: str) -> Task:
        project = self.repository.get_project(project_id)
        if project is None:
            raise AppError(code="PROJECT_NOT_FOUND", message="Project not found.", status_code=404)
        self._require_member(actor.id, project.workspace_id)
        task = Task(project_id=project.id, title=title)
        self.repository.save(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def create_comment(self, *, actor: User, task_id: str, body: str) -> Comment:
        task = self.repository.get_task(task_id)
        if task is None:
            raise AppError(code="TASK_NOT_FOUND", message="Task not found.", status_code=404)
        project = self.repository.get_project(task.project_id)
        assert project is not None
        self._require_member(actor.id, project.workspace_id)
        comment = Comment(task_id=task.id, author_user_id=actor.id, body=body)
        self.repository.save(comment)
        for member in self.repository.list_workspace_members(project.workspace_id):
            if member.user_id != actor.id:
                self.repository.save(
                    Notification(
                        recipient_user_id=member.user_id,
                        message=f"New comment on task {task.title}: {body}",
                        status="queued",
                    )
                )
        self.session.commit()
        self.session.refresh(comment)
        return comment

    async def drain_notifications(self) -> int:
        notifications = self.repository.list_queued_notifications()
        for notification in notifications:
            await self.manager.send_notification(
                user_id=notification.recipient_user_id,
                payload={"message": notification.message},
            )
            notification.status = "sent"
        self.session.commit()
        return len(notifications)

    def heartbeat(self, *, user_id: str) -> bool:
        self.presence.heartbeat(user_id)
        return True

    def is_online(self, *, user_id: str) -> bool:
        return self.presence.is_online(user_id)

    def _require_member(self, user_id: str, workspace_id: str) -> Membership:
        membership = self.repository.get_membership(workspace_id, user_id)
        if membership is None:
            raise AppError(code="FORBIDDEN", message="Workspace membership required.", status_code=403)
        return membership
