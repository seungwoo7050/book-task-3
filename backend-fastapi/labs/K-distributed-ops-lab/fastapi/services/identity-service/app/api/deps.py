from __future__ import annotations

from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.session import get_db
from app.domain.services.auth import AuthService


def get_auth_service(db: Annotated[Session, Depends(get_db)]) -> AuthService:
    return AuthService(db, get_settings())


def get_mailbox(request: Request) -> list[dict[str, str]]:
    return request.app.state.mailbox
