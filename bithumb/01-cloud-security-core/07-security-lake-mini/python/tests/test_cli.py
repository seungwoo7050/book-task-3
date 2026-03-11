from pathlib import Path

from typer.testing import CliRunner

from security_lake_mini.cli import app


def test_cli_ingest_returns_json_alerts(tmp_path: Path) -> None:
    runner = CliRunner()
    cloudtrail = Path(__file__).resolve().parents[2] / "problem" / "data" / "cloudtrail_suspicious.json"
    db_path = tmp_path / "lake.duckdb"
    parquet_path = tmp_path / "lake.parquet"

    result = runner.invoke(app, [str(cloudtrail), str(db_path), str(parquet_path)])

    assert result.exit_code == 0
    assert "\"control_id\": \"LAKE-001\"" in result.stdout
    assert parquet_path.exists()
