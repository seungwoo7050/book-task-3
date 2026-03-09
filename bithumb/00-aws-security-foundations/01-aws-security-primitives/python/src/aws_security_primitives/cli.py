from __future__ import annotations

import json
from pathlib import Path

import typer

from aws_security_primitives.engine import evaluate_policy

app = typer.Typer(add_completion=False, help="Explain IAM-style allow/deny decisions.")


@app.command()
def explain(policy_path: Path, request_path: Path) -> None:
    policy = json.loads(policy_path.read_text())
    request = json.loads(request_path.read_text())
    decision = evaluate_policy(policy, request)
    output = {
        "allowed": decision.allowed,
        "reason": decision.reason,
        "matches": [
            {
                "sid": match.sid,
                "effect": match.effect,
                "matched": match.matched,
                "reason": match.reason,
            }
            for match in decision.matches
        ],
    }
    typer.echo(json.dumps(output, indent=2))


if __name__ == "__main__":
    app()

