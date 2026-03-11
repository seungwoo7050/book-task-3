from __future__ import annotations

import json
from pathlib import Path

import typer

from auth_threat_modeling.scenarios import check_scenarios_manifest, demo_profile

app = typer.Typer(add_completion=False, help="Evaluate auth design scenarios for threat-modeling gaps.")


@app.command("check-scenarios")
def check_scenarios(manifest: Path) -> None:
    result = check_scenarios_manifest(manifest)
    typer.echo(json.dumps(result, indent=2))
    if result["failed"]:
        raise typer.Exit(code=1)


@app.command()
def demo(profile: Path) -> None:
    typer.echo(json.dumps(demo_profile(profile), indent=2))


if __name__ == "__main__":
    app()

