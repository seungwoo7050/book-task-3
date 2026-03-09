from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

import duckdb


@dataclass(slots=True)
class EventRecord:
    occurred_at: str
    source: str
    event_name: str
    actor: str
    resource_id: str
    action_result: str


def normalize_cloudtrail_events(payload: dict[str, Any]) -> list[EventRecord]:
    records: list[EventRecord] = []
    for entry in payload.get("Records", []):
        resource_id = (
            entry.get("requestParameters", {}).get("bucketName")
            or entry.get("requestParameters", {}).get("userName")
            or "unknown"
        )
        records.append(
            EventRecord(
                occurred_at=str(entry["eventTime"]),
                source=str(entry["eventSource"]),
                event_name=str(entry["eventName"]),
                actor=str(entry.get("userIdentity", {}).get("arn", "unknown")),
                resource_id=str(resource_id),
                action_result="cloudtrail",
            )
        )
    return records


def normalize_vpc_flow_logs(entries: list[dict[str, Any]]) -> list[EventRecord]:
    records: list[EventRecord] = []
    for entry in entries:
        records.append(
            EventRecord(
                occurred_at=str(entry["timestamp"]),
                source="vpc-flow-logs",
                event_name=f"flow:{entry['destination_port']}",
                actor=str(entry["source_ip"]),
                resource_id=str(entry["interface_id"]),
                action_result=str(entry["action"]),
            )
        )
    return records


def ingest_records(records: list[EventRecord], db_path: Path, parquet_path: Path) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    parquet_path.parent.mkdir(parents=True, exist_ok=True)
    connection = duckdb.connect(str(db_path))
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS event_records (
            occurred_at VARCHAR,
            source VARCHAR,
            event_name VARCHAR,
            actor VARCHAR,
            resource_id VARCHAR,
            action_result VARCHAR
        )
        """
    )
    connection.executemany(
        "INSERT INTO event_records VALUES (?, ?, ?, ?, ?, ?)",
        [tuple(asdict(record).values()) for record in records],
    )
    connection.execute(f"COPY event_records TO '{parquet_path}' (FORMAT PARQUET)")


def summarize_by_event_name(db_path: Path) -> list[tuple[str, int]]:
    connection = duckdb.connect(str(db_path))
    return connection.execute(
        "SELECT event_name, COUNT(*) AS count FROM event_records GROUP BY 1 ORDER BY 1"
    ).fetchall()


def summarize_by_actor(db_path: Path) -> list[tuple[str, int]]:
    connection = duckdb.connect(str(db_path))
    return connection.execute(
        "SELECT actor, COUNT(*) AS count FROM event_records GROUP BY 1 ORDER BY 1"
    ).fetchall()


def within_time_range(db_path: Path, start: str, end: str) -> int:
    connection = duckdb.connect(str(db_path))
    result = connection.execute(
        """
        SELECT COUNT(*)
        FROM event_records
        WHERE occurred_at >= ? AND occurred_at <= ?
        """,
        [start, end],
    ).fetchone()
    assert result is not None
    return int(result[0])


if __name__ == "__main__":
    import sys

    cloudtrail = json.loads(Path(sys.argv[1]).read_text())
    vpc_flow = json.loads(Path(sys.argv[2]).read_text())
    records = normalize_cloudtrail_events(cloudtrail) + normalize_vpc_flow_logs(vpc_flow)
    ingest_records(records, Path(".artifacts/log-basics.duckdb"), Path(".artifacts/log-basics.parquet"))
    print(f"ingested {len(records)} records")

