import json
from pathlib import Path

from cloudtrail_log_basics.etl import (
    ingest_records,
    normalize_cloudtrail_events,
    normalize_vpc_flow_logs,
    summarize_by_actor,
    summarize_by_event_name,
    within_time_range,
)


def _problem_data(name: str) -> Path:
    return Path(__file__).resolve().parents[2] / "problem" / "data" / name


def test_etl_ingests_cloudtrail_and_vpc_flow_logs(tmp_path: Path) -> None:
    cloudtrail = json.loads(_problem_data("cloudtrail_events.json").read_text())
    vpc_flow = json.loads(_problem_data("vpc_flow_logs.json").read_text())
    records = normalize_cloudtrail_events(cloudtrail) + normalize_vpc_flow_logs(vpc_flow)

    db_path = tmp_path / "events.duckdb"
    parquet_path = tmp_path / "events.parquet"
    ingest_records(records, db_path, parquet_path)

    assert parquet_path.exists()
    assert summarize_by_event_name(db_path) == [
        ("CreateAccessKey", 1),
        ("PutBucketAcl", 1),
        ("flow:22", 1),
        ("flow:443", 1),
    ]
    assert summarize_by_actor(db_path)[0][1] == 1
    assert within_time_range(db_path, "2026-03-07T09:00:00Z", "2026-03-07T09:05:00Z") == 2

