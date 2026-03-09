from __future__ import annotations

import json
from pathlib import Path

import typer

from container_guardrails.scanner import as_dicts, scan_image_metadata, scan_manifest

app = typer.Typer(add_completion=False, help="Scan Kubernetes manifests and image metadata for guardrail violations.")


@app.command()
def scan(manifest_path: Path, image_path: Path) -> None:
    findings = scan_manifest(manifest_path) + scan_image_metadata(image_path)
    typer.echo(json.dumps(as_dicts(findings), indent=2))


if __name__ == "__main__":
    app()

