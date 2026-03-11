from __future__ import annotations

import json
from pathlib import Path

import typer

from crypto_primitives_in_practice.vectors import check_vectors_manifest, demo_from_profile

app = typer.Typer(add_completion=False, help="Practice crypto primitives with reference vectors.")


@app.command("check-vectors")
def check_vectors(manifest: Path) -> None:
    result = check_vectors_manifest(manifest)
    typer.echo(json.dumps(result, indent=2))
    if result["failed"]:
        raise typer.Exit(code=1)


@app.command()
def demo(profile: Path) -> None:
    typer.echo(json.dumps(demo_from_profile(profile), indent=2))


if __name__ == "__main__":
    app()

