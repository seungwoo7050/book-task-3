from __future__ import annotations

import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path

import typer

from cloud_security_control_plane import db
from cloud_security_control_plane.metrics import Metrics
from cloud_security_control_plane.reporting import generate_markdown_report
from cloud_security_control_plane.scanners import ingest_cloudtrail, scan_iam_policy, scan_k8s_manifest, scan_terraform_plan
from cloud_security_control_plane.workers import list_exceptions, process_pending_remediations, process_pending_scans

app = typer.Typer(add_completion=False, help="Control plane CLI.")
scan_app = typer.Typer()
ingest_app = typer.Typer()
findings_app = typer.Typer()
exceptions_app = typer.Typer()
remediation_app = typer.Typer()
report_app = typer.Typer()
workers_app = typer.Typer()

app.add_typer(scan_app, name="scan")
app.add_typer(ingest_app, name="ingest")
app.add_typer(findings_app, name="findings")
app.add_typer(exceptions_app, name="exceptions")
app.add_typer(remediation_app, name="remediations")
app.add_typer(report_app, name="report")
app.add_typer(workers_app, name="workers")


def _database_url() -> str:
    return os.environ.get("DATABASE_URL", db.default_database_url())


def _lake_dir() -> Path:
    return Path(os.environ.get("CONTROL_PLANE_LAKE_DIR", ".artifacts/capstone/lake"))


@scan_app.command("terraform-plan")
def scan_terraform_plan_command(path: Path) -> None:
    findings = scan_terraform_plan(path)
    typer.echo(json.dumps([finding.model_dump(mode="json") for finding in findings], indent=2))


@scan_app.command("iam-policy")
def scan_iam_policy_command(path: Path) -> None:
    findings = scan_iam_policy(path)
    typer.echo(json.dumps([finding.model_dump(mode="json") for finding in findings], indent=2))


@ingest_app.command("cloudtrail")
def ingest_cloudtrail_command(path: Path) -> None:
    _, findings = ingest_cloudtrail(path, _lake_dir())
    typer.echo(json.dumps([finding.model_dump(mode="json") for finding in findings], indent=2))


@ingest_app.command("k8s-manifest")
def ingest_k8s_manifest_command(path: Path) -> None:
    findings = scan_k8s_manifest(path)
    typer.echo(json.dumps([finding.model_dump(mode="json") for finding in findings], indent=2))


@findings_app.command("list")
def findings_list_command() -> None:
    session_factory = db.make_session_factory(_database_url())
    with session_factory() as session:
        findings = db.list_findings(session)
    typer.echo(json.dumps([finding.model_dump(mode="json") for finding in findings], indent=2))


@exceptions_app.command("create")
def exceptions_create_command(scope_type: str, scope_id: str, reason: str, approved_by: str = "security.manager", days: int = 7) -> None:
    session_factory = db.make_session_factory(_database_url())
    with session_factory() as session:
        record = db.create_exception(
            session,
            scope_type,
            scope_id,
            reason,
            datetime.now(timezone.utc) + timedelta(days=days),
            approved_by,
        )
        session.commit()
    typer.echo(json.dumps({"id": record.id, "status": record.status}, indent=2))


@remediation_app.command("dry-run")
def remediation_dry_run_command(finding_id: str) -> None:
    session_factory = db.make_session_factory(_database_url())
    with session_factory() as session:
        db.create_remediation_request(session, finding_id)
        session.commit()
    plans = process_pending_remediations(_database_url(), Metrics())
    typer.echo(json.dumps([plan.model_dump() for plan in plans], indent=2))


@report_app.command("generate")
def report_generate_command(format: str = "markdown", output: Path | None = None) -> None:
    if format != "markdown":
        raise typer.BadParameter("only markdown is supported in v1")
    session_factory = db.make_session_factory(_database_url())
    with session_factory() as session:
        findings = db.list_findings(session)
        remediations = db.list_remediation_plans(session)
    markdown = generate_markdown_report(findings, list_exceptions(_database_url()), remediations)
    if output is not None:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(markdown)
    typer.echo(markdown)


@workers_app.command("scan-once")
def workers_scan_once_command() -> None:
    processed = process_pending_scans(_database_url(), _lake_dir(), Metrics())
    typer.echo(json.dumps({"processed_jobs": processed}, indent=2))


@workers_app.command("remediation-once")
def workers_remediation_once_command() -> None:
    plans = process_pending_remediations(_database_url(), Metrics())
    typer.echo(json.dumps([plan.model_dump() for plan in plans], indent=2))


if __name__ == "__main__":
    app()

