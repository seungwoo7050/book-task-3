from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse

from app.api.deps import get_auth_service, get_current_user, get_google_oidc_service, require_csrf
from app.core.config import Settings, get_settings
from app.core.errors import AppError
from app.core.rate_limit import RateLimiter
from app.core.security import (
    clear_auth_cookies,
    decode_pending_auth_token,
    generate_csrf_token,
    get_client_ip,
    get_user_agent,
    set_access_cookie,
    set_csrf_cookie,
    set_oauth_state_cookie,
    set_pending_auth_cookie,
    set_refresh_cookie,
    sign_oauth_state,
    unsign_oauth_state,
)
from app.db.models.user import User
from app.domain.services.auth import AuthService
from app.domain.services.google_oidc import GoogleOIDCService
from app.schemas.auth import (
    AuthSessionResponse,
    AuthUserResponse,
    GoogleLoginResponse,
    MeResponse,
    RecoveryCodesResponse,
    TwoFactorChallengeRequest,
    TwoFactorCodeRequest,
    TwoFactorSetupResponse,
)
from app.schemas.common import MessageResponse

router = APIRouter()


def _user_payload(user: User) -> AuthUserResponse:
    return AuthUserResponse(
        id=user.id,
        handle=user.handle,
        email=user.email,
        display_name=user.display_name,
        avatar_url=user.avatar_url,
        two_factor_enabled=user.two_factor_enabled,
    )


@router.get(
    "/google/login",
    response_model=GoogleLoginResponse,
    dependencies=[Depends(RateLimiter(limit=10, window_seconds=60, prefix="auth:google-login"))],
)
def google_login(
    oidc_service: Annotated[GoogleOIDCService, Depends(get_google_oidc_service)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> JSONResponse:
    request_data = oidc_service.build_authorization_request()
    signed_state = sign_oauth_state(
        {
            "state": request_data.state,
            "nonce": request_data.nonce,
            "code_verifier": request_data.code_verifier,
        },
        settings,
    )
    response = JSONResponse(
        GoogleLoginResponse(
            provider="google",
            authorization_url=request_data.authorization_url,
        ).model_dump(mode="json")
    )
    set_oauth_state_cookie(response, signed_state, settings)
    return response


@router.get(
    "/google/callback",
    response_model=AuthSessionResponse,
    dependencies=[Depends(RateLimiter(limit=15, window_seconds=60, prefix="auth:google-callback"))],
)
def google_callback(
    request: Request,
    code: str,
    state: str,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    oidc_service: Annotated[GoogleOIDCService, Depends(get_google_oidc_service)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> JSONResponse:
    signed_state = request.cookies.get(settings.oauth_state_cookie_name)
    if not signed_state:
        raise AppError(
            code="OAUTH_STATE_REQUIRED",
            message="OAuth state cookie is missing.",
            status_code=400,
        )
    oauth_state = unsign_oauth_state(signed_state, settings)
    if oauth_state["state"] != state:
        raise AppError(
            code="OAUTH_STATE_MISMATCH",
            message="OAuth state value did not match.",
            status_code=400,
        )

    token_response = oidc_service.exchange_code_for_tokens(code, str(oauth_state["code_verifier"]))
    id_payload = oidc_service.validate_id_token(
        str(token_response["id_token"]), str(oauth_state["nonce"])
    )
    userinfo = oidc_service.fetch_userinfo(str(token_response["access_token"]))
    merged_profile = {**userinfo, **id_payload}
    user = auth_service.sync_google_user(profile=merged_profile)
    response = JSONResponse(
        AuthSessionResponse(
            status="requires_2fa" if user.two_factor_enabled else "authenticated",
            user=_user_payload(user),
        ).model_dump(mode="json")
    )
    clear_auth_cookies(response, settings)

    client_ip = get_client_ip(request)
    user_agent = get_user_agent(request)

    if user.two_factor_enabled:
        pending_token = auth_service.start_pending_second_factor(
            user=user,
            ip_address=client_ip,
            user_agent=user_agent,
        )
        set_pending_auth_cookie(response, pending_token, settings)
        set_csrf_cookie(response, generate_csrf_token(), settings)
        return response

    bundle = auth_service.issue_session(
        user=user,
        ip_address=client_ip,
        user_agent=user_agent,
        audit_event_type="auth.login.success",
    )
    set_access_cookie(response, bundle.access_token, settings)
    set_refresh_cookie(response, bundle.refresh_token, settings)
    set_csrf_cookie(response, bundle.csrf_token, settings)
    return response


@router.get("/me", response_model=MeResponse)
def me(current_user: Annotated[User, Depends(get_current_user)]) -> MeResponse:
    return MeResponse(user=_user_payload(current_user))


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
    set_csrf_cookie(response, bundle.csrf_token, settings)
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


@router.post(
    "/2fa/setup", response_model=TwoFactorSetupResponse, dependencies=[Depends(require_csrf)]
)
def setup_two_factor(
    current_user: Annotated[User, Depends(get_current_user)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> TwoFactorSetupResponse:
    secret, provisioning_uri = auth_service.begin_two_factor_setup(current_user)
    return TwoFactorSetupResponse(secret=secret, provisioning_uri=provisioning_uri)


@router.post(
    "/2fa/confirm", response_model=RecoveryCodesResponse, dependencies=[Depends(require_csrf)]
)
def confirm_two_factor(
    request: Request,
    payload: TwoFactorCodeRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> RecoveryCodesResponse:
    codes = auth_service.confirm_two_factor_setup(
        user=current_user,
        code=payload.code,
        ip_address=get_client_ip(request),
        user_agent=get_user_agent(request),
    )
    return RecoveryCodesResponse(recovery_codes=codes)


@router.post(
    "/2fa/verify",
    response_model=AuthSessionResponse,
    dependencies=[
        Depends(require_csrf),
        Depends(RateLimiter(limit=10, window_seconds=60, prefix="auth:2fa-verify")),
    ],
)
def verify_two_factor(
    request: Request,
    payload: TwoFactorChallengeRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> JSONResponse:
    pending_token = request.cookies.get(settings.pending_auth_cookie_name)
    if not pending_token:
        raise AppError(
            code="PENDING_AUTH_REQUIRED",
            message="Pending second-factor authentication token is required.",
            status_code=401,
        )
    claims = decode_pending_auth_token(pending_token, settings)
    user = auth_service.user_repository.get_by_id(str(claims["sub"]))
    if user is None:
        raise AppError(code="USER_NOT_FOUND", message="User not found.", status_code=404)

    auth_service.verify_two_factor_challenge(
        user=user,
        code=payload.code,
        recovery_code=payload.recovery_code,
        ip_address=get_client_ip(request),
        user_agent=get_user_agent(request),
    )
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


@router.post(
    "/2fa/recovery-codes/regenerate",
    response_model=RecoveryCodesResponse,
    dependencies=[Depends(require_csrf)],
)
def regenerate_recovery_codes(
    request: Request,
    payload: TwoFactorChallengeRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> RecoveryCodesResponse:
    codes = auth_service.regenerate_recovery_codes(
        user=current_user,
        code=payload.code,
        recovery_code=payload.recovery_code,
        ip_address=get_client_ip(request),
        user_agent=get_user_agent(request),
    )
    return RecoveryCodesResponse(recovery_codes=codes)


@router.post("/2fa/disable", response_model=MessageResponse, dependencies=[Depends(require_csrf)])
def disable_two_factor(
    request: Request,
    payload: TwoFactorChallengeRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> MessageResponse:
    auth_service.disable_two_factor(
        user=current_user,
        code=payload.code,
        recovery_code=payload.recovery_code,
        ip_address=get_client_ip(request),
        user_agent=get_user_agent(request),
    )
    return MessageResponse(message="Two-factor authentication disabled.")
