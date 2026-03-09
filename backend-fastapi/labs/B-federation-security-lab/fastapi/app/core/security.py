from __future__ import annotations

import base64
import hashlib
import hmac
import secrets
from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
from fastapi import Request
from fastapi.responses import Response
from itsdangerous import BadSignature, URLSafeSerializer

from app.core.config import Settings
from app.core.errors import AppError


def now_utc() -> datetime:
    return datetime.now(UTC)


def generate_random_token() -> str:
    return secrets.token_urlsafe(32)


def generate_csrf_token() -> str:
    return secrets.token_urlsafe(24)


def hash_secret(secret: str, settings: Settings) -> str:
    return hmac.new(settings.secret_key.encode(), secret.encode(), hashlib.sha256).hexdigest()


def build_access_token(user_id: str, handle: str, settings: Settings) -> str:
    issued_at = now_utc()
    payload = {
        "sub": user_id,
        "handle": handle,
        "type": "access",
        "iss": settings.token_issuer,
        "iat": int(issued_at.timestamp()),
        "exp": int((issued_at + timedelta(seconds=settings.access_token_ttl_seconds)).timestamp()),
    }
    return jwt.encode(payload, settings.secret_key, algorithm=settings.token_algorithm)


def decode_access_token(token: str, settings: Settings) -> dict[str, Any]:
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.token_algorithm],
            issuer=settings.token_issuer,
        )
    except jwt.PyJWTError as exc:
        raise AppError(
            code="INVALID_ACCESS_TOKEN",
            message="Access token is invalid or expired.",
            status_code=401,
        ) from exc

    if payload.get("type") != "access":
        raise AppError(
            code="INVALID_ACCESS_TOKEN",
            message="Access token has an invalid type.",
            status_code=401,
        )
    return payload


def build_pending_auth_token(user_id: str, settings: Settings) -> str:
    issued_at = now_utc()
    payload = {
        "sub": user_id,
        "type": "pending_2fa",
        "iss": settings.token_issuer,
        "iat": int(issued_at.timestamp()),
        "exp": int((issued_at + timedelta(seconds=settings.pending_auth_ttl_seconds)).timestamp()),
    }
    return jwt.encode(payload, settings.secret_key, algorithm=settings.token_algorithm)


def decode_pending_auth_token(token: str, settings: Settings) -> dict[str, Any]:
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.token_algorithm],
            issuer=settings.token_issuer,
        )
    except jwt.PyJWTError as exc:
        raise AppError(
            code="INVALID_PENDING_AUTH_TOKEN",
            message="Pending authentication token is invalid or expired.",
            status_code=401,
        ) from exc

    if payload.get("type") != "pending_2fa":
        raise AppError(
            code="INVALID_PENDING_AUTH_TOKEN",
            message="Pending authentication token has an invalid type.",
            status_code=401,
        )
    return payload


def generate_pkce_verifier() -> str:
    return secrets.token_urlsafe(64)


def build_pkce_challenge(verifier: str) -> str:
    digest = hashlib.sha256(verifier.encode()).digest()
    return base64.urlsafe_b64encode(digest).decode().rstrip("=")


def sign_oauth_state(payload: dict[str, Any], settings: Settings) -> str:
    serializer = URLSafeSerializer(settings.secret_key, salt="google-oidc-state")
    return serializer.dumps(payload)


def unsign_oauth_state(value: str, settings: Settings) -> dict[str, Any]:
    serializer = URLSafeSerializer(settings.secret_key, salt="google-oidc-state")
    try:
        return serializer.loads(value)
    except BadSignature as exc:
        raise AppError(
            code="INVALID_OAUTH_STATE",
            message="OAuth state is invalid or has been tampered with.",
            status_code=400,
        ) from exc


def validate_csrf(request: Request, settings: Settings) -> None:
    cookie_token = request.cookies.get(settings.csrf_cookie_name)
    header_token = request.headers.get(settings.csrf_header_name)
    if (
        not cookie_token
        or not header_token
        or not secrets.compare_digest(cookie_token, header_token)
    ):
        raise AppError(
            code="CSRF_VALIDATION_FAILED",
            message="CSRF token validation failed.",
            status_code=403,
        )


def _cookie_kwargs(settings: Settings, *, httponly: bool) -> dict[str, Any]:
    return {
        "httponly": httponly,
        "secure": settings.secure_cookies,
        "samesite": "lax",
        "domain": settings.cookie_domain,
        "path": "/",
    }


def set_access_cookie(response: Response, token: str, settings: Settings) -> None:
    response.set_cookie(
        settings.access_cookie_name,
        token,
        max_age=settings.access_token_ttl_seconds,
        **_cookie_kwargs(settings, httponly=True),
    )


def set_refresh_cookie(response: Response, token: str, settings: Settings) -> None:
    response.set_cookie(
        settings.refresh_cookie_name,
        token,
        max_age=settings.refresh_token_ttl_seconds,
        **_cookie_kwargs(settings, httponly=True),
    )


def set_pending_auth_cookie(response: Response, token: str, settings: Settings) -> None:
    response.set_cookie(
        settings.pending_auth_cookie_name,
        token,
        max_age=settings.pending_auth_ttl_seconds,
        **_cookie_kwargs(settings, httponly=True),
    )


def set_csrf_cookie(response: Response, token: str, settings: Settings) -> None:
    response.set_cookie(
        settings.csrf_cookie_name,
        token,
        max_age=settings.refresh_token_ttl_seconds,
        **_cookie_kwargs(settings, httponly=False),
    )


def set_oauth_state_cookie(response: Response, token: str, settings: Settings) -> None:
    response.set_cookie(
        settings.oauth_state_cookie_name,
        token,
        max_age=600,
        **_cookie_kwargs(settings, httponly=True),
    )


def clear_auth_cookies(response: Response, settings: Settings) -> None:
    response.delete_cookie(settings.access_cookie_name, domain=settings.cookie_domain, path="/")
    response.delete_cookie(settings.refresh_cookie_name, domain=settings.cookie_domain, path="/")
    response.delete_cookie(
        settings.pending_auth_cookie_name, domain=settings.cookie_domain, path="/"
    )
    response.delete_cookie(settings.csrf_cookie_name, domain=settings.cookie_domain, path="/")
    response.delete_cookie(
        settings.oauth_state_cookie_name, domain=settings.cookie_domain, path="/"
    )


def get_client_ip(request: Request) -> str | None:
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else None


def get_user_agent(request: Request) -> str | None:
    return request.headers.get("user-agent")
