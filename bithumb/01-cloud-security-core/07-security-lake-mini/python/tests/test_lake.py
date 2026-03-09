from pathlib import Path

from security_lake_mini.lake import ingest_cloudtrail, run_detection_queries


def test_security_lake_generates_expected_alerts(tmp_path: Path) -> None:
    cloudtrail = Path(__file__).resolve().parents[2] / "problem" / "data" / "cloudtrail_suspicious.json"
    db_path = tmp_path / "lake.duckdb"
    parquet_path = tmp_path / "lake.parquet"

    ingest_cloudtrail(cloudtrail, db_path, parquet_path)
    alerts = run_detection_queries(db_path)

    assert parquet_path.exists()
    assert [alert.control_id for alert in alerts] == [
        "LAKE-001",
        "LAKE-002",
        "LAKE-003",
        "LAKE-004",
        "LAKE-005",
    ]

