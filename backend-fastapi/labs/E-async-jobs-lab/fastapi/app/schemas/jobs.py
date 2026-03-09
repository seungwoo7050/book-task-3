from __future__ import annotations

from pydantic import BaseModel, ConfigDict, EmailStr


class JobCreateRequest(BaseModel):
    recipient: EmailStr
    subject: str


class JobResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    idempotency_key: str
    recipient: EmailStr
    subject: str
    status: str
    attempt_count: int


class DrainResponse(BaseModel):
    processed: int
    statuses: list[str]
