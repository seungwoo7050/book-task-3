from __future__ import annotations

from core.auth import SESSION_COOKIE_NAME, create_session_cookie, verify_password
from core.config import load_settings
from db.models import AdminUser
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from api.dependencies import get_current_admin_optional, get_session
from api.schemas import LoginRequest

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login")
def login(payload: LoginRequest, response: Response, session: Session = Depends(get_session)) -> dict[str, object]:
    settings = load_settings()
    admin = session.scalar(select(AdminUser).where(AdminUser.email == payload.email).limit(1))
    if admin is None or not verify_password(payload.password, admin.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid credentials")
    cookie_value = create_session_cookie(secret=settings.session_secret, user_id=admin.id, email=admin.email)
    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=cookie_value,
        httponly=True,
        samesite="lax",
        secure=False,
        max_age=settings.session_max_age_seconds,
    )
    return {"authenticated": True, "email": admin.email}


@router.post("/logout")
def logout(response: Response) -> dict[str, bool]:
    response.delete_cookie(SESSION_COOKIE_NAME)
    return {"ok": True}


@router.get("/session")
def current_session(admin: AdminUser | None = Depends(get_current_admin_optional)) -> dict[str, object]:
    if admin is None:
        return {"authenticated": False, "email": None}
    return {"authenticated": True, "email": admin.email}
