from __future__ import annotations

import json
from pathlib import Path

import typer

from auth_threat_modeling.scenarios import check_scenarios_manifest, demo_profile

app = typer.Typer(add_completion=False, help="auth 설계 시나리오를 평가해 위협 finding을 반환합니다.")


@app.command("check-scenarios")
def check_scenarios(manifest: Path) -> None:
    result = check_scenarios_manifest(manifest)
    typer.echo(json.dumps(result, indent=2, ensure_ascii=False))
    if result["failed"]:
        raise typer.Exit(code=1)


@app.command()
def demo(profile: Path) -> None:
    typer.echo(json.dumps(demo_profile(profile), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    app()
