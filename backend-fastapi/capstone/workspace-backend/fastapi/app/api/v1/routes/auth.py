from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse

from app.api.deps import get_auth_service, get_current_user, get_mailbox, require_csrf
from app.core.config import Settings, get_settings
from app.core.errors import AppError
from app.core.security import clear_auth_cookies, set_access_cookie, set_csrf_cookie, set_refresh_cookie
from app.db.models.auth import User
from app.domain.services.auth import AuthService
from app.schemas.auth import AuthSessionResponse, AuthUserResponse, GoogleLoginRequest, LoginRequest, MeResponse, RegisterRequest, VerifyEmailRequest
from app.schemas.common import MessageResponse

router = APIRouter()


def _user_payload(user: User) -> AuthUserResponse:
    return AuthUserResponse(
        id=user.id,
        handle=user.handle,
        email=user.email,
        display_name=user.display_name,
        email_verified=user.email_verified_at is not None,
    )


@router.post("/register", response_model=MessageResponse)
def register(
    payload: RegisterRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    mailbox: Annotated[list[dict[str, str]], Depends(get_mailbox)],
) -> MessageResponse:
    auth_service.register(handle=payload.handle, email=payload.email, password=payload.password, mailbox=mailbox)
    return MessageResponse(message="Registration complete.")


@router.post("/verify-email", response_model=MessageResponse)
def verify_email(
    payload: VerifyEmailRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> MessageResponse:
    auth_service.verify_email(raw_token=payload.token)
    return MessageResponse(message="Email verified.")


@router.post("/login", response_model=AuthSessionResponse)
def login(
    payload: LoginRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> JSONResponse:
    user = auth_service.login_local(email=payload.email, password=payload.password)
    access, refresh, csrf = auth_service.issue_session(user=user)
    response = JSONResponse(AuthSessionResponse(status="authenticated", user=_user_payload(user)).model_dump(mode="json"))
    clear_auth_cookies(response, settings)
    set_access_cookie(response, access, settings)
    set_refresh_cookie(response, refresh, settings)
    set_csrf_cookie(response, csrf, settings)
    return response


@router.post("/google/login", response_model=AuthSessionResponse)
def google_login(
    payload: GoogleLoginRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> JSONResponse:
    user = auth_service.login_google(subject=payload.subject, email=payload.email, display_name=payload.display_name)
    access, refresh, csrf = auth_service.issue_session(user=user)
    response = JSONResponse(AuthSessionResponse(status="authenticated", user=_user_payload(user)).model_dump(mode="json"))
    clear_auth_cookies(response, settings)
    set_access_cookie(response, access, settings)
    set_refresh_cookie(response, refresh, settings)
    set_csrf_cookie(response, csrf, settings)
    return response


@router.get("/me", response_model=MeResponse)
def me(current_user: Annotated[User, Depends(get_current_user)]) -> MeResponse:
    return MeResponse(user=_user_payload(current_user))


@router.post("/token/refresh", response_model=AuthSessionResponse, dependencies=[Depends(require_csrf)])
def refresh(
    request: Request,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> JSONResponse:
    raw_token = request.cookies.get(settings.refresh_cookie_name)
    if not raw_token:
        raise AppError(code="REFRESH_TOKEN_REQUIRED", message="Refresh token required.", status_code=401)
    user, session_bundle = auth_service.rotate_refresh(raw_token=raw_token)
    access, refresh_token, csrf = session_bundle
    response = JSONResponse(AuthSessionResponse(status="authenticated", user=_user_payload(user)).model_dump(mode="json"))
    set_access_cookie(response, access, settings)
    set_refresh_cookie(response, refresh_token, settings)
    set_csrf_cookie(response, csrf, settings)
    return response


@router.post("/logout", response_model=MessageResponse, dependencies=[Depends(require_csrf)])
def logout(
    request: Request,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> JSONResponse:
    auth_service.revoke_refresh(raw_token=request.cookies.get(settings.refresh_cookie_name))
    response = JSONResponse(MessageResponse(message="Logged out.").model_dump(mode="json"))
    clear_auth_cookies(response, settings)
    return response
