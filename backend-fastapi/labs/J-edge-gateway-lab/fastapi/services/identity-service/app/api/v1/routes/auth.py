from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.api.deps import get_auth_service, get_mailbox
from app.core.errors import AppError
from app.db.models.auth import User
from app.domain.services.auth import AuthService
from app.schemas.auth import (
    AuthSessionBundleResponse,
    AuthUserResponse,
    GoogleLoginRequest,
    LoginRequest,
    RefreshRequest,
    RegisterRequest,
    RevokeRequest,
    VerifyEmailRequest,
)
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


@router.post("/login", response_model=AuthSessionBundleResponse)
def login(
    payload: LoginRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> AuthSessionBundleResponse:
    user = auth_service.login_local(email=payload.email, password=payload.password)
    access, refresh, csrf = auth_service.issue_session(user=user)
    return AuthSessionBundleResponse(
        access_token=access,
        refresh_token=refresh,
        csrf_token=csrf,
        user=_user_payload(user),
    )


@router.post("/google-login", response_model=AuthSessionBundleResponse)
def google_login(
    payload: GoogleLoginRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> AuthSessionBundleResponse:
    user = auth_service.login_google(subject=payload.subject, email=payload.email, display_name=payload.display_name)
    access, refresh, csrf = auth_service.issue_session(user=user)
    return AuthSessionBundleResponse(
        access_token=access,
        refresh_token=refresh,
        csrf_token=csrf,
        user=_user_payload(user),
    )


@router.post("/refresh", response_model=AuthSessionBundleResponse)
def refresh(
    payload: RefreshRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> AuthSessionBundleResponse:
    user, session_bundle = auth_service.rotate_refresh(raw_token=payload.refresh_token)
    access, refresh_token, csrf = session_bundle
    return AuthSessionBundleResponse(
        access_token=access,
        refresh_token=refresh_token,
        csrf_token=csrf,
        user=_user_payload(user),
    )


@router.post("/revoke", response_model=MessageResponse)
def revoke(
    payload: RevokeRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> MessageResponse:
    auth_service.revoke_refresh(raw_token=payload.refresh_token)
    return MessageResponse(message="Refresh token revoked.")


@router.get("/debug/mailbox/latest")
def latest_mailbox_token(
    mailbox: Annotated[list[dict[str, str]], Depends(get_mailbox)],
    email: str,
    kind: str = Query(default="verify_email"),
) -> dict[str, str]:
    for item in reversed(mailbox):
        if item.get("email") == email.lower() and item.get("kind") == kind:
            return item
    raise AppError(code="MAILBOX_TOKEN_NOT_FOUND", message="Mailbox token not found.", status_code=404)
