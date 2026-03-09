from __future__ import annotations

import json
from pathlib import Path

import typer

from cspm_rule_engine.scanner import findings_as_dicts, scan_access_keys, scan_plan

app = typer.Typer(add_completion=False, help="Scan Terraform plan JSON and snapshots for CSPM findings.")


@app.command()
def scan(plan_path: Path, access_key_snapshot_path: Path) -> None:
    plan = json.loads(plan_path.read_text())
    snapshot = json.loads(access_key_snapshot_path.read_text())
    findings = scan_plan(plan) + scan_access_keys(snapshot)
    typer.echo(json.dumps(findings_as_dicts(findings), indent=2))


if __name__ == "__main__":
    app()

