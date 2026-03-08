from __future__ import annotations

import json

import typer

from exception_evidence_manager.manager import ExceptionManager

app = typer.Typer(add_completion=False, help="Model finding exceptions and evidence.")


@app.command()
def demo() -> None:
    manager = ExceptionManager()
    record = manager.create_exception("finding", "finding-123", "Temporary business exception", 7)
    approved = manager.approve_exception(record.id, "security.manager")
    evidence = manager.append_evidence("finding-123", "risk memo", "s3://evidence/risk-memo.md")
    typer.echo(
        json.dumps(
            {
                "exception_id": approved.id,
                "approved_status": approved.status,
                "evidence_id": evidence.id,
                "audit_event_count": len(manager.audit_events),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    app()

