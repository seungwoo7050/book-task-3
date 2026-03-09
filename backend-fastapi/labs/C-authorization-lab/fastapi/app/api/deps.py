from __future__ import annotations

from typing import Annotated

from fastapi import Depends, Header
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.domain.services.authorization import AuthorizationService


def get_authorization_service(db: Annotated[Session, Depends(get_db)]) -> AuthorizationService:
    return AuthorizationService(db)


def get_actor_id(x_user_id: Annotated[str, Header(alias="X-User-Id")]) -> str:
    return x_user_id
