from __future__ import annotations

import hashlib
import hmac
import secrets
from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerifyMismatchError
from fastapi import Request
from fastapi.responses import Response

from app.core.config import Settings
from app.core.errors import AppError

password_hasher = PasswordHasher()


def now_utc() -> datetime:
    return datetime.now(UTC)


def generate_csrf_token() -> str:
    return secrets.token_urlsafe(24)


def hash_secret(secret: str, settings: Settings) -> str:
    return hmac.new(settings.secret_key.encode(), secret.encode(), hashlib.sha256).hexdigest()


def hash_password(password: str) -> str:
    return password_hasher.hash(password)


def verify_password(password_hash: str, password: str) -> bool:
    try:
        return password_hasher.verify(password_hash, password)
    except (VerifyMismatchError, InvalidHashError):
        return False


def build_access_token(user_id: str, handle: str, email: str, display_name: str, settings: Settings) -> str:
    issued_at = now_utc()
    payload = {
        "sub": user_id,
        "handle": handle,
        "email": email,
        "display_name": display_name,
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
        raise AppError(code="INVALID_ACCESS_TOKEN", message="Access token has an invalid type.", status_code=401)
    return payload


def validate_csrf(request: Request, settings: Settings) -> None:
    cookie_token = request.cookies.get(settings.csrf_cookie_name)
    header_token = request.headers.get(settings.csrf_header_name)
    if (
        not cookie_token
        or not header_token
        or not secrets.compare_digest(cookie_token, header_token)
    ):
        raise AppError(code="CSRF_VALIDATION_FAILED", message="CSRF token validation failed.", status_code=403)


def set_access_cookie(response: Response, token: str, settings: Settings) -> None:
    response.set_cookie(settings.access_cookie_name, token, httponly=True, secure=False, samesite="lax", path="/")


def set_refresh_cookie(response: Response, token: str, settings: Settings) -> None:
    response.set_cookie(settings.refresh_cookie_name, token, httponly=True, secure=False, samesite="lax", path="/")


def set_csrf_cookie(response: Response, token: str, settings: Settings) -> None:
    response.set_cookie(settings.csrf_cookie_name, token, httponly=False, secure=False, samesite="lax", path="/")


def clear_auth_cookies(response: Response, settings: Settings) -> None:
    response.delete_cookie(settings.access_cookie_name, path="/")
    response.delete_cookie(settings.refresh_cookie_name, path="/")
    response.delete_cookie(settings.csrf_cookie_name, path="/")
