from __future__ import annotations

import json
from pathlib import Path

import typer

from remediation_pack_runner.runner import as_dict, build_dry_run

app = typer.Typer(add_completion=False, help="Create dry-run remediation plans.")


@app.command()
def dry_run(finding_path: Path) -> None:
    finding = json.loads(finding_path.read_text())
    typer.echo(json.dumps(as_dict(build_dry_run(finding)), indent=2))


if __name__ == "__main__":
    app()

