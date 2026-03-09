from __future__ import annotations

import json
from pathlib import Path

import typer

from iam_policy_analyzer.analyzer import analyze_policy, findings_as_dicts

app = typer.Typer(add_completion=False, help="Analyze IAM policies for broad permissions.")


@app.command()
def analyze(policy_path: Path) -> None:
    policy = json.loads(policy_path.read_text())
    typer.echo(json.dumps(findings_as_dicts(analyze_policy(policy)), indent=2))


if __name__ == "__main__":
    app()

