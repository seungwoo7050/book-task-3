# 재현 가이드

## 무엇을 재현하나

- CloudTrail과 VPC Flow Logs가 공통 이벤트 레코드로 정규화되는지
- DuckDB와 Parquet 산출물이 동시에 생성되는지
- 집계와 시간 범위 질의가 기대한 숫자를 반환하는지

## 사전 조건

- `python3` 3.13+와 `make venv`가 필요합니다.
- 명령은 모두 레포 루트에서 실행합니다.

## 가장 짧은 재현 경로

```bash
make venv
PYTHONPATH=00-aws-security-foundations/03-cloudtrail-log-basics/python/src .venv/bin/python -m cloudtrail_log_basics.etl 00-aws-security-foundations/03-cloudtrail-log-basics/problem/data/cloudtrail_events.json 00-aws-security-foundations/03-cloudtrail-log-basics/problem/data/vpc_flow_logs.json
PYTHONPATH=00-aws-security-foundations/03-cloudtrail-log-basics/python/src .venv/bin/python -m pytest 00-aws-security-foundations/03-cloudtrail-log-basics/python/tests
```

## 기대 결과

- ETL 실행 후 stdout에 `ingested 4 records`가 출력되고, 레포 루트의 `.artifacts/log-basics.duckdb`, `.artifacts/log-basics.parquet`가 생성돼야 합니다.
- pytest는 하나의 테스트를 통과하면서 event_name 집계가 `CreateAccessKey`, `PutBucketAcl`, `flow:22`, `flow:443` 네 항목으로 정렬되는지 확인합니다.
- `within_time_range(...)=2`가 유지돼야 시간 범위 필터가 깨지지 않았다는 뜻입니다.

## 결과가 다르면 먼저 볼 파일

- 정규화 규칙을 다시 보려면: [../python/src/cloudtrail_log_basics/etl.py](../python/src/cloudtrail_log_basics/etl.py)
- 검증 기준을 다시 보려면: [../python/tests/test_etl.py](../python/tests/test_etl.py)
- CloudTrail 입력을 다시 보려면: [../problem/data/cloudtrail_events.json](../problem/data/cloudtrail_events.json)
- VPC Flow Logs 입력을 다시 보려면: [../problem/data/vpc_flow_logs.json](../problem/data/vpc_flow_logs.json)
- Python 버전 요구사항을 다시 보려면: [../../../pyproject.toml](../../../pyproject.toml)

## 이 재현이 증명하는 것

- 이 재현은 로그를 “모아 두는 것”과 “질의 가능한 구조로 만드는 것”이 다른 작업임을 보여 줍니다.
- 학습자는 ETL 성공 메시지보다, 어떤 집계 결과가 나와야 하는지를 설명할 수 있어야 합니다.
