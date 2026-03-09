from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.authorization import Document, Invite, Membership, User, Workspace


class AuthorizationRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def save(self, entity):
        self.session.add(entity)
        self.session.flush()
        return entity

    def get_user(self, user_id: str) -> User | None:
        return self.session.get(User, user_id)

    def get_user_by_email(self, email: str) -> User | None:
        return self.session.execute(select(User).where(User.email == email)).scalar_one_or_none()

    def get_workspace(self, workspace_id: str) -> Workspace | None:
        return self.session.get(Workspace, workspace_id)

    def get_membership(self, workspace_id: str, user_id: str) -> Membership | None:
        stmt = select(Membership).where(
            Membership.workspace_id == workspace_id,
            Membership.user_id == user_id,
        )
        return self.session.execute(stmt).scalar_one_or_none()

    def get_invite_by_token(self, token: str) -> Invite | None:
        return self.session.execute(
            select(Invite).where(Invite.token == token)
        ).scalar_one_or_none()

    def get_document(self, document_id: str) -> Document | None:
        return self.session.get(Document, document_id)
