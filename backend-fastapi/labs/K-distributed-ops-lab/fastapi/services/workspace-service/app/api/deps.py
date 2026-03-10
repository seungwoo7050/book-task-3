from __future__ import annotations

from typing import Annotated, Any

from fastapi import Depends, Header
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.errors import AppError
from app.core.security import decode_access_token
from app.db.session import get_db
from app.domain.services.platform import WorkspaceService


def get_current_claims(authorization: Annotated[str | None, Header()] = None) -> dict[str, Any]:
    if not authorization or not authorization.startswith("Bearer "):
        raise AppError(code="ACCESS_TOKEN_REQUIRED", message="Bearer token required.", status_code=401)
    return decode_access_token(authorization.removeprefix("Bearer ").strip(), get_settings())


def get_workspace_service(db: Annotated[Session, Depends(get_db)]) -> WorkspaceService:
    return WorkspaceService(db, get_settings())
