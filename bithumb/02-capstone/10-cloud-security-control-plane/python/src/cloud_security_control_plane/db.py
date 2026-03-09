from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from sqlalchemy import DateTime, Integer, String, Text, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

from cloud_security_control_plane.schemas import ExceptionRecord, Finding, RemediationPlan


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def ensure_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def default_database_url() -> str:
    return os.environ.get("DATABASE_URL", "sqlite+pysqlite:///.artifacts/capstone/control-plane.sqlite3")


def normalize_database_url(url: str) -> str:
    if url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql+psycopg://", 1)
    return url


class Base(DeclarativeBase):
    pass


class FindingRecord(Base):
    __tablename__ = "findings"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    source: Mapped[str] = mapped_column(String(32))
    control_id: Mapped[str] = mapped_column(String(32))
    severity: Mapped[str] = mapped_column(String(16))
    resource_type: Mapped[str] = mapped_column(String(64))
    resource_id: Mapped[str] = mapped_column(String(128))
    title: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(32), default="open")
    detected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    evidence_ref: Mapped[str | None] = mapped_column(String(255), nullable=True)


class ExceptionRow(Base):
    __tablename__ = "exceptions"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    scope_type: Mapped[str] = mapped_column(String(32))
    scope_id: Mapped[str] = mapped_column(String(128))
    reason: Mapped[str] = mapped_column(Text)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    approved_by: Mapped[str | None] = mapped_column(String(64), nullable=True)
    status: Mapped[str] = mapped_column(String(32))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class AuditEventRow(Base):
    __tablename__ = "audit_events"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    event_type: Mapped[str] = mapped_column(String(64))
    entity_id: Mapped[str] = mapped_column(String(128))
    payload_json: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class RemediationRequestRow(Base):
    __tablename__ = "remediation_requests"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    finding_id: Mapped[str] = mapped_column(String(64))
    status: Mapped[str] = mapped_column(String(32), default="pending")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class RemediationPlanRow(Base):
    __tablename__ = "remediation_plans"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    finding_id: Mapped[str] = mapped_column(String(64))
    mode: Mapped[str] = mapped_column(String(32))
    summary: Mapped[str] = mapped_column(Text)
    commands_or_patch_json: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(32))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class ScanJobRow(Base):
    __tablename__ = "scan_jobs"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    source: Mapped[str] = mapped_column(String(32))
    path: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(32), default="pending")
    finding_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


def make_session_factory(database_url: str | None = None) -> sessionmaker[Session]:
    url = normalize_database_url(database_url or default_database_url())
    Path(".artifacts/capstone").mkdir(parents=True, exist_ok=True)
    connect_args = {"check_same_thread": False} if url.startswith("sqlite") else {}
    engine = create_engine(url, future=True, connect_args=connect_args)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine, expire_on_commit=False)


def record_audit_event(session: Session, event_type: str, entity_id: str, payload: dict[str, str]) -> None:
    session.add(
        AuditEventRow(
            id=str(uuid4()),
            event_type=event_type,
            entity_id=entity_id,
            payload_json=json.dumps(payload),
            created_at=utcnow(),
        )
    )


def save_findings(session: Session, findings: list[Finding]) -> None:
    for finding in findings:
        session.merge(
            FindingRecord(
                id=finding.id,
                source=finding.source,
                control_id=finding.control_id,
                severity=finding.severity,
                resource_type=finding.resource_type,
                resource_id=finding.resource_id,
                title=finding.title,
                status=finding.status,
                detected_at=finding.detected_at,
                evidence_ref=finding.evidence_ref,
            )
        )


def create_scan_job(session: Session, source: str, path: str) -> ScanJobRow:
    job = ScanJobRow(id=str(uuid4()), source=source, path=path, status="pending", finding_count=0, created_at=utcnow(), updated_at=utcnow())
    session.add(job)
    record_audit_event(session, "scan.created", job.id, {"source": source, "path": path})
    return job


def pending_scan_jobs(session: Session) -> list[ScanJobRow]:
    return list(session.scalars(select(ScanJobRow).where(ScanJobRow.status == "pending")).all())


def complete_scan_job(session: Session, job: ScanJobRow, finding_count: int) -> None:
    job.status = "completed"
    job.finding_count = finding_count
    job.updated_at = utcnow()
    record_audit_event(session, "scan.completed", job.id, {"finding_count": str(finding_count)})


def create_exception(session: Session, scope_type: str, scope_id: str, reason: str, expires_at: datetime, approved_by: str | None) -> ExceptionRow:
    row = ExceptionRow(
        id=str(uuid4()),
        scope_type=scope_type,
        scope_id=scope_id,
        reason=reason,
        expires_at=expires_at,
        approved_by=approved_by,
        status="approved" if approved_by else "pending",
        created_at=utcnow(),
    )
    session.add(row)
    record_audit_event(session, "exception.created", row.id, {"scope_id": scope_id})
    return row


def active_exception_scope_ids(session: Session) -> set[str]:
    rows = session.scalars(select(ExceptionRow).where(ExceptionRow.status == "approved")).all()
    now = utcnow()
    return {row.scope_id for row in rows if ensure_utc(row.expires_at) > now}


def list_findings(session: Session) -> list[Finding]:
    suppressed = active_exception_scope_ids(session)
    rows = session.scalars(select(FindingRecord).order_by(FindingRecord.detected_at)).all()
    return [
        Finding(
            id=row.id,
            source=row.source,
            control_id=row.control_id,
            severity=row.severity,
            resource_type=row.resource_type,
            resource_id=row.resource_id,
            title=row.title,
            status="suppressed" if row.id in suppressed else row.status,
            detected_at=row.detected_at,
            evidence_ref=row.evidence_ref,
        )
        for row in rows
    ]


def create_remediation_request(session: Session, finding_id: str) -> RemediationRequestRow:
    row = RemediationRequestRow(id=str(uuid4()), finding_id=finding_id, status="pending", created_at=utcnow())
    session.add(row)
    record_audit_event(session, "remediation.requested", row.id, {"finding_id": finding_id})
    return row


def pending_remediation_requests(session: Session) -> list[RemediationRequestRow]:
    return list(session.scalars(select(RemediationRequestRow).where(RemediationRequestRow.status == "pending")).all())


def save_remediation_plan(session: Session, plan: RemediationPlan) -> None:
    session.merge(
        RemediationPlanRow(
            id=plan.id,
            finding_id=plan.finding_id,
            mode=plan.mode,
            summary=plan.summary,
            commands_or_patch_json=json.dumps(plan.commands_or_patch),
            status=plan.status,
            created_at=utcnow(),
        )
    )


def complete_remediation_request(session: Session, row: RemediationRequestRow) -> None:
    row.status = "completed"
    record_audit_event(session, "remediation.completed", row.id, {"finding_id": row.finding_id})


def list_remediation_plans(session: Session) -> list[RemediationPlan]:
    rows = session.scalars(select(RemediationPlanRow).order_by(RemediationPlanRow.created_at)).all()
    return [
        RemediationPlan(
            id=row.id,
            finding_id=row.finding_id,
            mode=row.mode,
            summary=row.summary,
            commands_or_patch=json.loads(row.commands_or_patch_json),
            status=row.status,
        )
        for row in rows
    ]


def get_finding(session: Session, finding_id: str) -> Finding | None:
    row = session.get(FindingRecord, finding_id)
    if row is None:
        return None
    suppressed = active_exception_scope_ids(session)
    return Finding(
        id=row.id,
        source=row.source,
        control_id=row.control_id,
        severity=row.severity,
        resource_type=row.resource_type,
        resource_id=row.resource_id,
        title=row.title,
        status="suppressed" if row.id in suppressed else row.status,
        detected_at=row.detected_at,
        evidence_ref=row.evidence_ref,
    )


def reset_state(session: Session) -> None:
    session.query(RemediationPlanRow).delete()
    session.query(RemediationRequestRow).delete()
    session.query(ExceptionRow).delete()
    session.query(ScanJobRow).delete()
    session.query(AuditEventRow).delete()
    session.query(FindingRecord).delete()
