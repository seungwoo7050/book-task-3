from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any
from uuid import uuid4


@dataclass(slots=True)
class ExceptionRecord:
    id: str
    scope_type: str
    scope_id: str
    reason: str
    expires_at: datetime
    approved_by: str | None
    status: str


@dataclass(slots=True)
class Evidence:
    id: str
    finding_id: str
    title: str
    uri: str
    added_at: datetime


@dataclass(slots=True)
class AuditEvent:
    id: str
    event_type: str
    entity_id: str
    created_at: datetime
    payload: dict[str, Any] = field(default_factory=dict)


class ExceptionManager:
    def __init__(self) -> None:
        self.exceptions: dict[str, ExceptionRecord] = {}
        self.evidence: list[Evidence] = []
        self.audit_events: list[AuditEvent] = []

    def create_exception(self, scope_type: str, scope_id: str, reason: str, days: int) -> ExceptionRecord:
        record = ExceptionRecord(
            id=str(uuid4()),
            scope_type=scope_type,
            scope_id=scope_id,
            reason=reason,
            expires_at=datetime.now(timezone.utc) + timedelta(days=days),
            approved_by=None,
            status="pending",
        )
        self.exceptions[record.id] = record
        self._append_event("exception.created", record.id, {"scope_id": scope_id})
        return record

    def approve_exception(self, exception_id: str, approved_by: str) -> ExceptionRecord:
        record = self.exceptions[exception_id]
        approved = ExceptionRecord(
            id=record.id,
            scope_type=record.scope_type,
            scope_id=record.scope_id,
            reason=record.reason,
            expires_at=record.expires_at,
            approved_by=approved_by,
            status="approved",
        )
        self.exceptions[exception_id] = approved
        self._append_event("exception.approved", exception_id, {"approved_by": approved_by})
        return approved

    def append_evidence(self, finding_id: str, title: str, uri: str) -> Evidence:
        evidence = Evidence(
            id=str(uuid4()),
            finding_id=finding_id,
            title=title,
            uri=uri,
            added_at=datetime.now(timezone.utc),
        )
        self.evidence.append(evidence)
        self._append_event("evidence.added", finding_id, {"uri": uri})
        return evidence

    def is_suppressed(self, scope_id: str, now: datetime | None = None) -> bool:
        current = now or datetime.now(timezone.utc)
        return any(
            record.scope_id == scope_id
            and record.status == "approved"
            and record.expires_at > current
            for record in self.exceptions.values()
        )

    def _append_event(self, event_type: str, entity_id: str, payload: dict[str, Any]) -> None:
        self.audit_events.append(
            AuditEvent(
                id=str(uuid4()),
                event_type=event_type,
                entity_id=entity_id,
                created_at=datetime.now(timezone.utc),
                payload=payload,
            )
        )

