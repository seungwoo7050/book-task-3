from __future__ import annotations

import re
from typing import Any

from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from app.db.models.user import ExternalIdentity, User


class UserRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_id(self, user_id: str) -> User | None:
        return self.session.get(User, user_id)

    def get_by_email(self, email: str) -> User | None:
        return self.session.execute(select(User).where(User.email == email)).scalar_one_or_none()

    def get_by_external_identity(self, provider: str, subject: str) -> User | None:
        stmt: Select[tuple[User]] = (
            select(User)
            .join(ExternalIdentity, ExternalIdentity.user_id == User.id)
            .where(
                ExternalIdentity.provider == provider,
                ExternalIdentity.provider_subject == subject,
            )
        )
        return self.session.execute(stmt).scalar_one_or_none()

    def get_external_identity(self, provider: str, subject: str) -> ExternalIdentity | None:
        stmt = select(ExternalIdentity).where(
            ExternalIdentity.provider == provider,
            ExternalIdentity.provider_subject == subject,
        )
        return self.session.execute(stmt).scalar_one_or_none()

    def save(self, entity: User | ExternalIdentity) -> User | ExternalIdentity:
        self.session.add(entity)
        self.session.flush()
        return entity

    def ensure_unique_handle(self, proposed: str) -> str:
        base = self._normalize_handle(proposed)
        handle = base
        counter = 1

        while self.session.execute(
            select(User.id).where(User.handle == handle)
        ).scalar_one_or_none():
            counter += 1
            handle = f"{base[:24]}-{counter}"
        return handle

    def link_external_identity(
        self,
        *,
        user: User,
        provider: str,
        subject: str,
        provider_email: str | None,
        email_verified: bool,
        profile: dict[str, Any],
    ) -> ExternalIdentity:
        identity = self.get_external_identity(provider, subject)
        if identity is None:
            identity = ExternalIdentity(
                user_id=user.id,
                provider=provider,
                provider_subject=subject,
                provider_email=provider_email,
                email_verified=email_verified,
                profile=profile,
            )
        else:
            identity.user_id = user.id
            identity.provider_email = provider_email
            identity.email_verified = email_verified
            identity.profile = profile
        self.session.add(identity)
        self.session.flush()
        return identity

    @staticmethod
    def _normalize_handle(value: str) -> str:
        lowered = value.lower().strip()
        normalized = re.sub(r"[^a-z0-9]+", "-", lowered).strip("-")
        return normalized[:32] or "player"
