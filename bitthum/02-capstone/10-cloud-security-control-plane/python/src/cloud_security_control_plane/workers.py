from __future__ import annotations

from pathlib import Path

from cloud_security_control_plane import db
from cloud_security_control_plane.metrics import Metrics
from cloud_security_control_plane.remediation import build_remediation
from cloud_security_control_plane.scanners import ingest_cloudtrail, scan_iam_policy, scan_k8s_manifest, scan_terraform_plan
from cloud_security_control_plane.schemas import ExceptionRecord, RemediationPlan


def process_pending_scans(database_url: str, lake_dir: Path, metrics: Metrics) -> int:
    session_factory = db.make_session_factory(database_url)
    processed = 0
    with session_factory() as session:
        jobs = db.pending_scan_jobs(session)
        for job in jobs:
            if job.source == "terraform-plan":
                findings = scan_terraform_plan(Path(job.path))
            elif job.source == "iam-policy":
                findings = scan_iam_policy(Path(job.path))
            else:
                findings = []
            db.save_findings(session, findings)
            db.complete_scan_job(session, job, len(findings))
            metrics.inc("scan_jobs_processed_total")
            metrics.inc("findings_created_total", len(findings))
            processed += 1
        session.commit()
    return processed


def ingest_cloudtrail_and_save(database_url: str, lake_dir: Path, path: Path, metrics: Metrics) -> int:
    session_factory = db.make_session_factory(database_url)
    _, findings = ingest_cloudtrail(path, lake_dir)
    with session_factory() as session:
        db.save_findings(session, findings)
        db.record_audit_event(session, "cloudtrail.ingested", str(path), {"finding_count": str(len(findings))})
        session.commit()
    metrics.inc("cloudtrail_ingestions_total")
    metrics.inc("findings_created_total", len(findings))
    return len(findings)


def ingest_k8s_and_save(database_url: str, path: Path, metrics: Metrics) -> int:
    session_factory = db.make_session_factory(database_url)
    findings = scan_k8s_manifest(path)
    with session_factory() as session:
        db.save_findings(session, findings)
        db.record_audit_event(session, "k8s.ingested", str(path), {"finding_count": str(len(findings))})
        session.commit()
    metrics.inc("k8s_ingestions_total")
    metrics.inc("findings_created_total", len(findings))
    return len(findings)


def process_pending_remediations(database_url: str, metrics: Metrics) -> list[RemediationPlan]:
    session_factory = db.make_session_factory(database_url)
    created: list[RemediationPlan] = []
    with session_factory() as session:
        for request in db.pending_remediation_requests(session):
            finding = db.get_finding(session, request.finding_id)
            if finding is None:
                db.complete_remediation_request(session, request)
                continue
            plan = build_remediation(finding)
            db.save_remediation_plan(session, plan)
            db.complete_remediation_request(session, request)
            created.append(plan)
            metrics.inc("remediation_requests_total")
        session.commit()
    return created


def list_exceptions(database_url: str) -> list[ExceptionRecord]:
    session_factory = db.make_session_factory(database_url)
    with session_factory() as session:
        rows = session.query(db.ExceptionRow).order_by(db.ExceptionRow.created_at).all()
        return [
            ExceptionRecord(
                id=row.id,
                scope_type=row.scope_type,
                scope_id=row.scope_id,
                reason=row.reason,
                expires_at=row.expires_at,
                approved_by=row.approved_by,
                status=row.status,
            )
            for row in rows
        ]

