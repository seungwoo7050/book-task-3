from __future__ import annotations

import json
from pathlib import Path

import typer

from security_lake_mini.lake import ingest_cloudtrail, run_detection_queries

app = typer.Typer(add_completion=False, help="Build a local security lake from CloudTrail fixtures.")


@app.command()
def ingest(cloudtrail_path: Path, db_path: Path, parquet_path: Path) -> None:
    ingest_cloudtrail(cloudtrail_path, db_path, parquet_path)
    typer.echo(json.dumps([alert.__dict__ for alert in run_detection_queries(db_path)], indent=2))


if __name__ == "__main__":
    app()

