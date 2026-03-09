from __future__ import annotations

from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.orm import Session

from app.core.config import Settings, get_settings
from app.core.errors import AppError
from app.core.security import decode_access_token, validate_csrf
from app.db.models.auth import User
from app.db.session import get_db
from app.domain.services.auth import AuthService
from app.domain.services.platform import PlatformService


def get_auth_service(db: Annotated[Session, Depends(get_db)]) -> AuthService:
    return AuthService(db, get_settings())


def get_mailbox(request: Request) -> list[dict[str, str]]:
    return request.app.state.mailbox


def require_csrf(request: Request, settings: Annotated[Settings, Depends(get_settings)]) -> None:
    validate_csrf(request, settings)


def get_current_user(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> User:
    access_token = request.cookies.get(settings.access_cookie_name)
    if not access_token:
        raise AppError(code="ACCESS_TOKEN_REQUIRED", message="Authentication required.", status_code=401)
    payload = decode_access_token(access_token, settings)
    user = db.get(User, str(payload["sub"]))
    if user is None:
        raise AppError(code="USER_NOT_FOUND", message="User not found.", status_code=404)
    return user


def get_platform_service(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
) -> PlatformService:
    return PlatformService(db, request.app.state.connection_manager, request.app.state.presence_tracker)
