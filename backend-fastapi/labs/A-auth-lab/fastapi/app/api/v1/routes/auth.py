from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse

from app.api.deps import get_auth_service, get_current_user, get_mailbox, require_csrf
from app.core.config import Settings, get_settings
from app.core.errors import AppError
from app.core.rate_limit import RateLimiter
from app.core.security import (
    clear_auth_cookies,
    generate_csrf_token,
    get_client_ip,
    get_user_agent,
    set_access_cookie,
    set_csrf_cookie,
    set_refresh_cookie,
)
from app.db.models.user import User
from app.domain.services.auth import AuthService
from app.schemas.auth import (
    AuthSessionResponse,
    AuthUserResponse,
    LoginRequest,
    MeResponse,
    PasswordResetConfirmRequest,
    PasswordResetRequest,
    RegisterRequest,
    VerifyEmailRequest,
)
from app.schemas.common import MessageResponse

router = APIRouter()


def _user_payload(user: User) -> AuthUserResponse:
    return AuthUserResponse(
        id=user.id,
        handle=user.handle,
        email=user.email,
        email_verified=user.email_verified_at is not None,
    )


@router.post(
    "/register",
    response_model=MessageResponse,
    dependencies=[Depends(RateLimiter(limit=15, window_seconds=60, prefix="auth:register"))],
)
def register(
    payload: RegisterRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    mailbox: Annotated[list[dict[str, str]], Depends(get_mailbox)],
) -> MessageResponse:
    auth_service.register_user(
        email=payload.email,
        handle=payload.handle,
        password=payload.password,
        mailbox=mailbox,
    )
    return MessageResponse(
        message="Registration complete. Verify the email address before signing in."
    )


@router.post(
    "/verify-email",
    response_model=MessageResponse,
    dependencies=[Depends(RateLimiter(limit=20, window_seconds=60, prefix="auth:verify-email"))],
)
def verify_email(
    payload: VerifyEmailRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> MessageResponse:
    auth_service.verify_email(raw_token=payload.token)
    return MessageResponse(message="Email address verified.")


@router.post(
    "/login",
    response_model=AuthSessionResponse,
    dependencies=[Depends(RateLimiter(limit=15, window_seconds=60, prefix="auth:login"))],
)
def login(
    request: Request,
    payload: LoginRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> JSONResponse:
    user = auth_service.authenticate_user(email=payload.email, password=payload.password)
    bundle = auth_service.issue_session(
        user=user,
        ip_address=get_client_ip(request),
        user_agent=get_user_agent(request),
        audit_event_type="auth.login.success",
    )
    response = JSONResponse(
        AuthSessionResponse(status="authenticated", user=_user_payload(user)).model_dump(
            mode="json"
        )
    )
    clear_auth_cookies(response, settings)
    set_access_cookie(response, bundle.access_token, settings)
    set_refresh_cookie(response, bundle.refresh_token, settings)
    set_csrf_cookie(response, bundle.csrf_token, settings)
    return response


@router.get("/me", response_model=MeResponse)
def me(current_user: Annotated[User, Depends(get_current_user)]) -> MeResponse:
    return MeResponse(user=_user_payload(current_user))


@router.post(
    "/password-reset/request",
    response_model=MessageResponse,
    dependencies=[Depends(RateLimiter(limit=10, window_seconds=60, prefix="auth:password-reset"))],
)
def request_password_reset(
    payload: PasswordResetRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    mailbox: Annotated[list[dict[str, str]], Depends(get_mailbox)],
) -> MessageResponse:
    auth_service.request_password_reset(email=payload.email, mailbox=mailbox)
    return MessageResponse(message="If the account exists, a reset email has been queued.")


@router.post(
    "/password-reset/confirm",
    response_model=MessageResponse,
    dependencies=[Depends(RateLimiter(limit=10, window_seconds=60, prefix="auth:password-reset"))],
)
def confirm_password_reset(
    payload: PasswordResetConfirmRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> MessageResponse:
    auth_service.reset_password(raw_token=payload.token, new_password=payload.new_password)
    return MessageResponse(message="Password updated.")


@router.post(
    "/token/refresh",
    response_model=AuthSessionResponse,
    dependencies=[
        Depends(require_csrf),
        Depends(RateLimiter(limit=20, window_seconds=60, prefix="auth:refresh")),
    ],
)
def refresh_token(
    request: Request,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> JSONResponse:
    refresh_token = request.cookies.get(settings.refresh_cookie_name)
    if not refresh_token:
        raise AppError(
            code="REFRESH_TOKEN_REQUIRED",
            message="Refresh token cookie is required.",
            status_code=401,
        )
    user, bundle = auth_service.rotate_refresh_token(
        raw_refresh_token=refresh_token,
        ip_address=get_client_ip(request),
        user_agent=get_user_agent(request),
    )
    response = JSONResponse(
        AuthSessionResponse(status="authenticated", user=_user_payload(user)).model_dump(
            mode="json"
        )
    )
    set_access_cookie(response, bundle.access_token, settings)
    set_refresh_cookie(response, bundle.refresh_token, settings)
    set_csrf_cookie(response, generate_csrf_token(), settings)
    return response


@router.post("/logout", response_model=MessageResponse, dependencies=[Depends(require_csrf)])
def logout(
    request: Request,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> JSONResponse:
    auth_service.revoke_refresh_token(
        raw_refresh_token=request.cookies.get(settings.refresh_cookie_name),
        ip_address=get_client_ip(request),
        user_agent=get_user_agent(request),
    )
    response = JSONResponse(MessageResponse(message="Logged out.").model_dump(mode="json"))
    clear_auth_cookies(response, settings)
    return response
