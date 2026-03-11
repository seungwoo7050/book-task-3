from __future__ import annotations

import json
from pathlib import Path

import typer

from owasp_backend_mitigations.cases import check_case_manifest, demo_profile

app = typer.Typer(add_completion=False, help="Evaluate backend endpoint designs for missing OWASP mitigations.")


@app.command("check-cases")
def check_cases(manifest: Path) -> None:
    result = check_case_manifest(manifest)
    typer.echo(json.dumps(result, indent=2))
    if result["failed"]:
        raise typer.Exit(code=1)


@app.command()
def demo(profile: Path) -> None:
    typer.echo(json.dumps(demo_profile(profile), indent=2))


if __name__ == "__main__":
    app()

