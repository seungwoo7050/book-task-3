from __future__ import annotations

from pydantic import BaseModel, EmailStr, Field


class AuthUserResponse(BaseModel):
    id: str
    handle: str
    email: EmailStr
    display_name: str
    email_verified: bool


class AuthSessionResponse(BaseModel):
    status: str
    user: AuthUserResponse


class RegisterRequest(BaseModel):
    handle: str = Field(min_length=3, max_length=32)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class GoogleLoginRequest(BaseModel):
    subject: str
    email: EmailStr
    display_name: str


class VerifyEmailRequest(BaseModel):
    token: str


class MeResponse(BaseModel):
    user: AuthUserResponse


class AuthSessionBundleResponse(BaseModel):
    access_token: str
    refresh_token: str
    csrf_token: str
    user: AuthUserResponse


class RefreshRequest(BaseModel):
    refresh_token: str


class RevokeRequest(BaseModel):
    refresh_token: str
