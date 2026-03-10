from __future__ import annotations

from typing import Annotated, Any

from fastapi import Depends, Request

from app.core.config import Settings, get_settings
from app.core.errors import AppError
from app.core.security import decode_access_token, validate_csrf
from app.runtime import ServiceClient


def get_service_client(request: Request) -> ServiceClient:
    return request.app.state.service_client


def get_current_claims(request: Request, settings: Annotated[Settings, Depends(get_settings)]) -> dict[str, Any]:
    access_token = request.cookies.get(settings.access_cookie_name)
    if not access_token:
        raise AppError(code="ACCESS_TOKEN_REQUIRED", message="Authentication required.", status_code=401)
    return decode_access_token(access_token, settings)


def require_csrf(request: Request, settings: Annotated[Settings, Depends(get_settings)]) -> None:
    validate_csrf(request, settings)
