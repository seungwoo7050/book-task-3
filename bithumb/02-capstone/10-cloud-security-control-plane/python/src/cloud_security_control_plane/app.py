from __future__ import annotations

import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse

from cloud_security_control_plane import db
from cloud_security_control_plane.metrics import Metrics
from cloud_security_control_plane.reporting import generate_markdown_report
from cloud_security_control_plane.schemas import ExceptionCreateRequest, PathRequest, ScanRequest
from cloud_security_control_plane.workers import (
    ingest_cloudtrail_and_save,
    ingest_k8s_and_save,
    list_exceptions,
    process_pending_remediations,
    process_pending_scans,
)


def create_app(database_url: str | None = None, lake_dir: str | None = None) -> FastAPI:
    app = FastAPI(title="Cloud Security Control Plane")
    app.state.database_url = db.normalize_database_url(database_url or db.default_database_url())
    app.state.lake_dir = Path(lake_dir or os.environ.get("CONTROL_PLANE_LAKE_DIR", ".artifacts/capstone/lake"))
    app.state.metrics = Metrics()
    app.state.session_factory = db.make_session_factory(app.state.database_url)

    @app.get("/healthz")
    def healthz() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/metrics", response_class=PlainTextResponse)
    def metrics() -> str:
        return app.state.metrics.render()

    @app.post("/v1/scans")
    def create_scan(payload: ScanRequest) -> dict[str, str]:
        with app.state.session_factory() as session:
            job = db.create_scan_job(session, payload.source, payload.path)
            session.commit()
        app.state.metrics.inc("scan_jobs_created_total")
        return {"id": job.id, "status": job.status}

    @app.post("/v1/ingestions/cloudtrail")
    def ingest_cloudtrail_route(payload: PathRequest) -> dict[str, int]:
        finding_count = ingest_cloudtrail_and_save(app.state.database_url, app.state.lake_dir, Path(payload.path), app.state.metrics)
        return {"finding_count": finding_count}

    @app.post("/v1/ingestions/k8s")
    def ingest_k8s_route(payload: PathRequest) -> dict[str, int]:
        finding_count = ingest_k8s_and_save(app.state.database_url, Path(payload.path), app.state.metrics)
        return {"finding_count": finding_count}

    @app.get("/v1/findings")
    def findings() -> dict[str, list[dict[str, object]]]:
        with app.state.session_factory() as session:
            items = db.list_findings(session)
        return {"findings": [item.model_dump() for item in items]}

    @app.post("/v1/exceptions")
    def exceptions(payload: ExceptionCreateRequest) -> dict[str, str]:
        with app.state.session_factory() as session:
            record = db.create_exception(
                session,
                payload.scope_type,
                payload.scope_id,
                payload.reason,
                payload.expires_at,
                payload.approved_by,
            )
            session.commit()
        return {"id": record.id, "status": record.status}

    @app.get("/v1/remediations")
    def remediations() -> dict[str, list[dict[str, object]]]:
        with app.state.session_factory() as session:
            plans = db.list_remediation_plans(session)
        return {"remediations": [plan.model_dump() for plan in plans]}

    @app.post("/v1/remediations/{finding_id}/dry-run")
    def remediation_dry_run(finding_id: str) -> dict[str, object]:
        with app.state.session_factory() as session:
            if db.get_finding(session, finding_id) is None:
                raise HTTPException(status_code=404, detail="finding not found")
            db.create_remediation_request(session, finding_id)
            session.commit()
        plans = process_pending_remediations(app.state.database_url, app.state.metrics)
        if not plans:
            raise HTTPException(status_code=500, detail="remediation plan was not created")
        return {"remediation": plans[-1].model_dump()}

    @app.get("/v1/reports/latest")
    def report_latest() -> dict[str, str]:
        with app.state.session_factory() as session:
            findings = db.list_findings(session)
            remediations = db.list_remediation_plans(session)
        markdown = generate_markdown_report(findings, list_exceptions(app.state.database_url), remediations)
        return {"markdown": markdown}

    @app.post("/v1/workers/scans/run")
    def run_scan_worker() -> dict[str, int]:
        processed = process_pending_scans(app.state.database_url, app.state.lake_dir, app.state.metrics)
        return {"processed_jobs": processed}

    return app

