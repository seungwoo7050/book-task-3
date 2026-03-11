from __future__ import annotations

import json
from pathlib import Path

import typer

from collab_saas_security_review.review import build_review, load_json, write_artifacts

app = typer.Typer(add_completion=False, help="Run a consolidated offline security review for a collaboration SaaS bundle.")


@app.command()
def review(bundle: Path, output_dir: Path | None = typer.Option(None, "--output-dir")) -> None:
    payload = load_json(bundle)
    consolidated = build_review(payload)
    if output_dir is not None:
        write_artifacts(payload, consolidated, output_dir)
    typer.echo(json.dumps(consolidated, indent=2))


@app.command()
def demo(bundle: Path, output_dir: Path | None = typer.Option(None, "--output-dir")) -> None:
    target = output_dir or Path(".artifacts/capstone/demo")
    payload = load_json(bundle)
    consolidated = build_review(payload)
    write_artifacts(payload, consolidated, target)
    typer.echo(f"demo assets written to {target}")


if __name__ == "__main__":
    app()
