from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.db.models.auth import EmailToken, ExternalIdentity, RefreshToken, User


class AuthRepository:
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

    def get_user_by_identity(self, provider: str, subject: str) -> User | None:
        identity = self.session.execute(
            select(ExternalIdentity).where(
                ExternalIdentity.provider == provider,
                ExternalIdentity.provider_subject == subject,
            )
        ).scalar_one_or_none()
        return self.get_user(identity.user_id) if identity else None

    def create_refresh_token(self, token: RefreshToken) -> RefreshToken:
        self.session.add(token)
        self.session.flush()
        return token

    def get_refresh_token(self, token_hash: str) -> RefreshToken | None:
        return self.session.execute(
            select(RefreshToken).where(RefreshToken.token_hash == token_hash)
        ).scalar_one_or_none()

    def revoke_token_family(self, family_id: str) -> None:
        for token in self.session.execute(
            select(RefreshToken).where(RefreshToken.family_id == family_id)
        ).scalars():
            token.revoked_at = datetime.now(UTC)
        self.session.flush()

    def replace_email_token(self, *, user_id: str, kind: str, token_hash: str, expires_at: datetime) -> None:
        self.session.execute(delete(EmailToken).where(EmailToken.user_id == user_id, EmailToken.kind == kind))
        self.session.add(
            EmailToken(
                user_id=user_id,
                kind=kind,
                token_hash=token_hash,
                expires_at=expires_at,
                created_at=datetime.now(UTC),
            )
        )
        self.session.flush()

    def get_email_token(self, *, kind: str, token_hash: str) -> EmailToken | None:
        return self.session.execute(
            select(EmailToken).where(
                EmailToken.kind == kind,
                EmailToken.token_hash == token_hash,
                EmailToken.used_at.is_(None),
            )
        ).scalar_one_or_none()
