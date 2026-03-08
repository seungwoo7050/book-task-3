from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import duckdb


@dataclass(slots=True)
class Alert:
    control_id: str
    title: str
    event_name: str
    actor: str
    occurred_at: str


def _normalize(payload: dict[str, object]) -> list[tuple[str, str, str, str]]:
    rows: list[tuple[str, str, str, str]] = []
    for entry in payload.get("Records", []):  # type: ignore[union-attr]
        if not isinstance(entry, dict):
            continue
        identity = entry.get("userIdentity", {})
        actor = identity.get("arn", "unknown") if isinstance(identity, dict) else "unknown"
        rows.append(
            (
                str(entry["eventTime"]),
                str(entry["eventSource"]),
                str(entry["eventName"]),
                str(actor),
            )
        )
    return rows


def ingest_cloudtrail(cloudtrail_path: Path, db_path: Path, parquet_path: Path) -> None:
    payload = json.loads(cloudtrail_path.read_text())
    rows = _normalize(payload)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    parquet_path.parent.mkdir(parents=True, exist_ok=True)

    connection = duckdb.connect(str(db_path))
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS lake_events (
            occurred_at VARCHAR,
            source VARCHAR,
            event_name VARCHAR,
            actor VARCHAR
        )
        """
    )
    connection.execute("DELETE FROM lake_events")
    connection.executemany("INSERT INTO lake_events VALUES (?, ?, ?, ?)", rows)
    connection.execute(f"COPY lake_events TO '{parquet_path}' (FORMAT PARQUET)")


def run_detection_queries(db_path: Path) -> list[Alert]:
    connection = duckdb.connect(str(db_path))
    query = """
    SELECT
      CASE
        WHEN event_name = 'CreateAccessKey' THEN 'LAKE-001'
        WHEN event_name = 'PutBucketAcl' THEN 'LAKE-002'
        WHEN event_name = 'AuthorizeSecurityGroupIngress' THEN 'LAKE-003'
        WHEN event_name = 'DeleteTrail' THEN 'LAKE-004'
        WHEN event_name = 'ConsoleLogin' AND actor LIKE '%:root' THEN 'LAKE-005'
        ELSE 'INFO'
      END AS control_id,
      event_name,
      actor,
      occurred_at
    FROM lake_events
    WHERE event_name IN (
      'CreateAccessKey',
      'PutBucketAcl',
      'AuthorizeSecurityGroupIngress',
      'DeleteTrail',
      'ConsoleLogin'
    )
    ORDER BY occurred_at
    """
    alerts: list[Alert] = []
    for control_id, event_name, actor, occurred_at in connection.execute(query).fetchall():
        alerts.append(
            Alert(
                control_id=str(control_id),
                title=f"Detected suspicious event: {event_name}",
                event_name=str(event_name),
                actor=str(actor),
                occurred_at=str(occurred_at),
            )
        )
    return alerts


if __name__ == "__main__":
    import sys

    ingest_cloudtrail(Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]))
    for alert in run_detection_queries(Path(sys.argv[2])):
        print(alert)

