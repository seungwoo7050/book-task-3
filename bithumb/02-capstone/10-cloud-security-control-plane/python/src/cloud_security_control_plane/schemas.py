from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class Asset(BaseModel):
    source: str
    path: str


class Finding(BaseModel):
    id: str
    source: str
    control_id: str
    severity: str
    resource_type: str
    resource_id: str
    title: str
    status: str
    detected_at: datetime
    evidence_ref: str | None = None


class ExceptionRecord(BaseModel):
    id: str
    scope_type: str
    scope_id: str
    reason: str
    expires_at: datetime
    approved_by: str | None = None
    status: str


class RemediationPlan(BaseModel):
    id: str
    finding_id: str
    mode: str
    summary: str
    commands_or_patch: list[str]
    status: str


class AuditEvent(BaseModel):
    id: str
    event_type: str
    entity_id: str
    created_at: datetime
    payload: dict[str, str]


class EventRecord(BaseModel):
    occurred_at: str
    source: str
    event_name: str
    actor: str


class ScanRequest(BaseModel):
    source: Literal["terraform-plan", "iam-policy"]
    path: str


class PathRequest(BaseModel):
    path: str


class ExceptionCreateRequest(BaseModel):
    scope_type: str
    scope_id: str
    reason: str
    expires_at: datetime
    approved_by: str | None = None

