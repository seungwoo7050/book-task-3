# Python Implementation

- Scope: CloudTrail/VPC Flow Logs fixture를 정규화해 DuckDB와 Parquet로 적재한다.
- Build: `PYTHONPATH=src python -m cloudtrail_log_basics.etl <cloudtrail.json> <vpcflow.json>`
- Test: `PYTHONPATH=src python -m pytest tests`
- Status: `verified`
- Known gaps: 실제 CloudTrail 스키마의 모든 필드를 보존하지는 않는다.

