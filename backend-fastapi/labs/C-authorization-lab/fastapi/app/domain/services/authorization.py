from __future__ import annotations

import secrets

from sqlalchemy.orm import Session

from app.core.errors import AppError
from app.db.models.authorization import Document, Invite, Membership, User, Workspace
from app.repositories.authorization_repository import AuthorizationRepository

ROLE_ORDER = {"viewer": 1, "member": 2, "admin": 3, "owner": 4}


class AuthorizationService:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.repository = AuthorizationRepository(session)

    def create_user(self, *, email: str, name: str) -> User:
        existing = self.repository.get_user_by_email(email.lower())
        if existing:
            return existing
        user = User(email=email.lower(), name=name)
        self.repository.save(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def create_workspace(self, *, actor_id: str, name: str) -> Workspace:
        actor = self._require_user(actor_id)
        workspace = Workspace(name=name, owner_user_id=actor.id)
        self.repository.save(workspace)
        self.repository.save(Membership(user_id=actor.id, workspace_id=workspace.id, role="owner"))
        self.session.commit()
        self.session.refresh(workspace)
        return workspace

    def create_invite(self, *, actor_id: str, workspace_id: str, email: str, role: str) -> Invite:
        self._require_role(actor_id=actor_id, workspace_id=workspace_id, minimum="admin")
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

    def accept_invite(self, *, actor_id: str, token: str) -> Membership:
        actor = self._require_user(actor_id)
        invite = self._require_pending_invite(token)
        if actor.email != invite.email:
            raise AppError(
                code="INVITE_EMAIL_MISMATCH",
                message="Invite email does not match the acting user.",
                status_code=403,
            )
        invite.status = "accepted"
        membership = self.repository.get_membership(invite.workspace_id, actor.id)
        if membership is None:
            membership = Membership(
                user_id=actor.id,
                workspace_id=invite.workspace_id,
                role=invite.role,
            )
            self.repository.save(membership)
        self.session.commit()
        self.session.refresh(membership)
        return membership

    def decline_invite(self, *, actor_id: str, token: str) -> Invite:
        actor = self._require_user(actor_id)
        invite = self._require_pending_invite(token)
        if actor.email != invite.email:
            raise AppError(
                code="INVITE_EMAIL_MISMATCH",
                message="Invite email does not match the acting user.",
                status_code=403,
            )
        invite.status = "declined"
        self.session.commit()
        self.session.refresh(invite)
        return invite

    def change_role(
        self,
        *,
        actor_id: str,
        workspace_id: str,
        target_user_id: str,
        role: str,
    ) -> Membership:
        owner_membership = self._require_role(
            actor_id=actor_id,
            workspace_id=workspace_id,
            minimum="owner",
        )
        if owner_membership.role != "owner":
            raise AppError(
                code="FORBIDDEN",
                message="Only owners can change roles.",
                status_code=403,
            )
        membership = self.repository.get_membership(workspace_id, target_user_id)
        if membership is None:
            raise AppError(
                code="MEMBERSHIP_NOT_FOUND",
                message="Membership not found.",
                status_code=404,
            )
        membership.role = role
        self.session.commit()
        self.session.refresh(membership)
        return membership

    def create_document(self, *, actor_id: str, workspace_id: str, title: str) -> Document:
        self._require_role(actor_id=actor_id, workspace_id=workspace_id, minimum="member")
        document = Document(
            workspace_id=workspace_id,
            owner_user_id=actor_id,
            title=title,
        )
        self.repository.save(document)
        self.session.commit()
        self.session.refresh(document)
        return document

    def get_document(self, *, actor_id: str, document_id: str) -> Document:
        document = self.repository.get_document(document_id)
        if document is None:
            raise AppError(
                code="DOCUMENT_NOT_FOUND",
                message="Document not found.",
                status_code=404,
            )
        self._require_role(actor_id=actor_id, workspace_id=document.workspace_id, minimum="viewer")
        return document

    def _require_user(self, user_id: str) -> User:
        user = self.repository.get_user(user_id)
        if user is None:
            raise AppError(code="USER_NOT_FOUND", message="User not found.", status_code=404)
        return user

    def _require_pending_invite(self, token: str) -> Invite:
        invite = self.repository.get_invite_by_token(token)
        if invite is None or invite.status != "pending":
            raise AppError(code="INVITE_NOT_FOUND", message="Invite not found.", status_code=404)
        return invite

    def _require_role(self, *, actor_id: str, workspace_id: str, minimum: str) -> Membership:
        membership = self.repository.get_membership(workspace_id, actor_id)
        if membership is None or ROLE_ORDER[membership.role] < ROLE_ORDER[minimum]:
            raise AppError(code="FORBIDDEN", message="Forbidden.", status_code=403)
        return membership
