# 07 Security Lake Mini

## Status

`verified`

## Problem Scope

- CloudTrail fixture를 Parquet + DuckDB로 적재
- detection query preset 실행
- alert snapshot 생성

## Build

```bash
cd python
PYTHONPATH=src python -m security_lake_mini.cli ../problem/data/cloudtrail_suspicious.json .artifacts/lake.duckdb .artifacts/events.parquet
```

## Test

```bash
cd study2
PYTHONPATH=01-cloud-security-core/07-security-lake-mini/python/src .venv/bin/python -m pytest 01-cloud-security-core/07-security-lake-mini/python/tests
```
