from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, EmailStr, Field


class AuthUserResponse(BaseModel):
    id: str
    handle: str
    email: EmailStr
    display_name: str
    avatar_url: str | None
    two_factor_enabled: bool


class GoogleLoginResponse(BaseModel):
    provider: Literal["google"]
    authorization_url: str


class AuthSessionResponse(BaseModel):
    status: Literal["authenticated", "requires_2fa"]
    user: AuthUserResponse


class MeResponse(BaseModel):
    user: AuthUserResponse


class TwoFactorSetupResponse(BaseModel):
    secret: str
    provisioning_uri: str


class TwoFactorCodeRequest(BaseModel):
    code: str = Field(min_length=6, max_length=8)


class TwoFactorChallengeRequest(BaseModel):
    code: str | None = Field(default=None, min_length=6, max_length=8)
    recovery_code: str | None = Field(default=None, min_length=9, max_length=9)


class RecoveryCodesResponse(BaseModel):
    recovery_codes: list[str]
