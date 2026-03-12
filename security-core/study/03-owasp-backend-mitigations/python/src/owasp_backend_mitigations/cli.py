from __future__ import annotations

import json
from pathlib import Path

import typer

from owasp_backend_mitigations.cases import check_case_manifest, demo_profile

app = typer.Typer(add_completion=False, help="backend endpoint 설계를 평가해 누락된 OWASP 방어를 반환합니다.")


@app.command("check-cases")
def check_cases(manifest: Path) -> None:
    result = check_case_manifest(manifest)
    typer.echo(json.dumps(result, indent=2, ensure_ascii=False))
    if result["failed"]:
        raise typer.Exit(code=1)


@app.command()
def demo(profile: Path) -> None:
    typer.echo(json.dumps(demo_profile(profile), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    app()
