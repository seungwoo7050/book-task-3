# Python Implementation

- Scope: API server, scan worker, remediation worker, PostgreSQL/SQLite state store, DuckDB lake, Typer CLI, markdown reporting
- Build: `PYTHONPATH=src python -m cloud_security_control_plane.cli findings list`
- Test: `PYTHONPATH=src python -m pytest tests`
- Status: `verified`
- Known gaps: SQS/Kafka 같은 외부 job queue는 넣지 않고 DB polling worker로 단순화했다.

