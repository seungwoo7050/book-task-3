from __future__ import annotations

import re

from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from app.db.models.user import User


class UserRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_id(self, user_id: str) -> User | None:
        return self.session.get(User, user_id)

    def get_by_email(self, email: str) -> User | None:
        return self.session.execute(select(User).where(User.email == email)).scalar_one_or_none()

    def get_by_handle(self, handle: str) -> User | None:
        stmt: Select[tuple[User]] = select(User).where(User.handle == handle)
        return self.session.execute(stmt).scalar_one_or_none()

    def save(self, entity: User) -> User:
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

    @staticmethod
    def _normalize_handle(value: str) -> str:
        lowered = value.lower().strip()
        normalized = re.sub(r"[^a-z0-9]+", "-", lowered).strip("-")
        return normalized[:32] or "player"
