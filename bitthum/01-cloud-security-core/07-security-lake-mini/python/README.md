# Python Implementation

- Scope: CloudTrail fixture를 DuckDB/Parquet로 적재하고 preset detection query를 수행한다.
- Build: `PYTHONPATH=src python -m security_lake_mini.cli <cloudtrail.json> <lake.duckdb> <events.parquet>`
- Test: `PYTHONPATH=src python -m pytest tests`
- Status: `verified`
- Known gaps: VPC Flow Logs와 multi-table join은 capstone에서 확장한다.

