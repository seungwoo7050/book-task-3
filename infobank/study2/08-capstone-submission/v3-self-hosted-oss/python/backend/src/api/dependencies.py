from __future__ import annotations

from collections.abc import Iterator

from core.auth import SESSION_COOKIE_NAME, parse_session_cookie
from core.config import load_settings
from db.database import get_db
from db.models import AdminUser
from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session


def get_session() -> Iterator[Session]:
    yield from get_db()


def get_current_admin(
    request: Request,
    session: Session = Depends(get_session),
) -> AdminUser:
    settings = load_settings()
    cookie = request.cookies.get(SESSION_COOKIE_NAME)
    if not cookie:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="authentication required")
    parsed = parse_session_cookie(
        secret=settings.session_secret,
        cookie_value=cookie,
        max_age_seconds=settings.session_max_age_seconds,
    )
    if parsed is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid session")
    admin = session.get(AdminUser, parsed["user_id"])
    if admin is None or not admin.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="admin session not found")
    return admin


def get_current_admin_optional(
    request: Request,
    session: Session = Depends(get_session),
) -> AdminUser | None:
    settings = load_settings()
    cookie = request.cookies.get(SESSION_COOKIE_NAME)
    if not cookie:
        return None
    parsed = parse_session_cookie(
        secret=settings.session_secret,
        cookie_value=cookie,
        max_age_seconds=settings.session_max_age_seconds,
    )
    if parsed is None:
        return None
    admin = session.get(AdminUser, parsed["user_id"])
    if admin is None or not admin.is_active:
        return None
    return admin
