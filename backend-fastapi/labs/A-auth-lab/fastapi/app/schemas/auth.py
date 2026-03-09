from __future__ import annotations

from pydantic import BaseModel, EmailStr, Field


class AuthUserResponse(BaseModel):
    id: str
    handle: str
    email: EmailStr
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


class VerifyEmailRequest(BaseModel):
    token: str = Field(min_length=10)


class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordResetConfirmRequest(BaseModel):
    token: str = Field(min_length=10)
    new_password: str = Field(min_length=8, max_length=128)


class MeResponse(BaseModel):
    user: AuthUserResponse
