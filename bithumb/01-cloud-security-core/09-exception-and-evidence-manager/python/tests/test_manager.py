from datetime import datetime, timedelta, timezone

from exception_evidence_manager.manager import ExceptionManager


def test_exception_suppresses_scope_until_expiry() -> None:
    manager = ExceptionManager()
    created = manager.create_exception("finding", "finding-1", "temporary exception", 3)
    manager.approve_exception(created.id, "security.manager")
    assert manager.is_suppressed("finding-1") is True
    expired_time = datetime.now(timezone.utc) + timedelta(days=10)
    assert manager.is_suppressed("finding-1", now=expired_time) is False


def test_evidence_and_audit_events_are_appended() -> None:
    manager = ExceptionManager()
    created = manager.create_exception("finding", "finding-1", "temporary exception", 3)
    manager.approve_exception(created.id, "security.manager")
    manager.append_evidence("finding-1", "risk memo", "s3://bucket/risk.md")
    assert len(manager.audit_events) == 3
    assert manager.audit_events[0].event_type == "exception.created"

