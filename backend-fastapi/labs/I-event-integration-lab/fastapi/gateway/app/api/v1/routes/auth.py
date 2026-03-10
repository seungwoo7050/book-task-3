from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse

from app.api.deps import get_current_claims, get_service_client, require_csrf
from app.core.config import Settings, get_settings
from app.core.security import clear_auth_cookies, set_access_cookie, set_csrf_cookie, set_refresh_cookie
from app.runtime import ServiceClient
from app.schemas.auth import (
    AuthSessionResponse,
    AuthUserResponse,
    GoogleLoginRequest,
    LoginRequest,
    MeResponse,
    RegisterRequest,
    VerifyEmailRequest,
)
from app.schemas.common import MessageResponse

router = APIRouter()


def _user_payload(claims: dict[str, str]) -> AuthUserResponse:
    return AuthUserResponse(
        id=str(claims["sub"]),
        handle=str(claims["handle"]),
        email=str(claims["email"]),
        display_name=str(claims["display_name"]),
        email_verified=True,
    )


@router.post("/register", response_model=MessageResponse)
def register(
    payload: RegisterRequest,
    request: Request,
    client: Annotated[ServiceClient, Depends(get_service_client)],
) -> MessageResponse:
    client.request(request, "identity", "POST", "/internal/auth/register", json=payload.model_dump(mode="json"))
    return MessageResponse(message="Registration complete.")


@router.post("/verify-email", response_model=MessageResponse)
def verify_email(
    payload: VerifyEmailRequest,
    request: Request,
    client: Annotated[ServiceClient, Depends(get_service_client)],
) -> MessageResponse:
    client.request(request, "identity", "POST", "/internal/auth/verify-email", json=payload.model_dump(mode="json"))
    return MessageResponse(message="Email verified.")


@router.post("/login", response_model=AuthSessionResponse)
def login(
    payload: LoginRequest,
    request: Request,
    client: Annotated[ServiceClient, Depends(get_service_client)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> JSONResponse:
    bundle = client.request(request, "identity", "POST", "/internal/auth/login", json=payload.model_dump(mode="json"))
    response = JSONResponse(AuthSessionResponse(status="authenticated", user=AuthUserResponse(**bundle["user"])).model_dump(mode="json"))
    clear_auth_cookies(response, settings)
    set_access_cookie(response, bundle["access_token"], settings)
    set_refresh_cookie(response, bundle["refresh_token"], settings)
    set_csrf_cookie(response, bundle["csrf_token"], settings)
    return response


@router.post("/google/login", response_model=AuthSessionResponse)
def google_login(
    payload: GoogleLoginRequest,
    request: Request,
    client: Annotated[ServiceClient, Depends(get_service_client)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> JSONResponse:
    bundle = client.request(request, "identity", "POST", "/internal/auth/google-login", json=payload.model_dump(mode="json"))
    response = JSONResponse(AuthSessionResponse(status="authenticated", user=AuthUserResponse(**bundle["user"])).model_dump(mode="json"))
    clear_auth_cookies(response, settings)
    set_access_cookie(response, bundle["access_token"], settings)
    set_refresh_cookie(response, bundle["refresh_token"], settings)
    set_csrf_cookie(response, bundle["csrf_token"], settings)
    return response


@router.get("/me", response_model=MeResponse)
def me(claims: Annotated[dict[str, str], Depends(get_current_claims)]) -> MeResponse:
    return MeResponse(user=_user_payload(claims))


@router.post("/token/refresh", response_model=AuthSessionResponse, dependencies=[Depends(require_csrf)])
def refresh(
    request: Request,
    client: Annotated[ServiceClient, Depends(get_service_client)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> JSONResponse:
    raw_token = request.cookies.get(settings.refresh_cookie_name)
    bundle = client.request(request, "identity", "POST", "/internal/auth/refresh", json={"refresh_token": raw_token})
    response = JSONResponse(AuthSessionResponse(status="authenticated", user=AuthUserResponse(**bundle["user"])).model_dump(mode="json"))
    set_access_cookie(response, bundle["access_token"], settings)
    set_refresh_cookie(response, bundle["refresh_token"], settings)
    set_csrf_cookie(response, bundle["csrf_token"], settings)
    return response


@router.post("/logout", response_model=MessageResponse, dependencies=[Depends(require_csrf)])
def logout(
    request: Request,
    client: Annotated[ServiceClient, Depends(get_service_client)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> JSONResponse:
    raw_token = request.cookies.get(settings.refresh_cookie_name)
    if raw_token:
        client.request(request, "identity", "POST", "/internal/auth/revoke", json={"refresh_token": raw_token})
    response = JSONResponse(MessageResponse(message="Logged out.").model_dump(mode="json"))
    clear_auth_cookies(response, settings)
    return response
