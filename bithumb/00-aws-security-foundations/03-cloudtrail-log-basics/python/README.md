# Python 구현

아래 내용은 모두 레포 루트 기준입니다.

## 구현한 답의 범위

- CloudTrail과 VPC Flow Logs fixture를 읽습니다.
- 공통 필드 중심의 이벤트 구조로 정규화합니다.
- DuckDB와 Parquet로 로컬 적재 흐름을 재현합니다.

## 핵심 엔트리포인트

- `python/src/cloudtrail_log_basics/etl.py`
- `python/tests/test_etl.py`

## 실행

```bash
make venv
PYTHONPATH=00-aws-security-foundations/03-cloudtrail-log-basics/python/src .venv/bin/python -m cloudtrail_log_basics.etl 00-aws-security-foundations/03-cloudtrail-log-basics/problem/data/cloudtrail_events.json 00-aws-security-foundations/03-cloudtrail-log-basics/problem/data/vpc_flow_logs.json
```

## 테스트

```bash
PYTHONPATH=00-aws-security-foundations/03-cloudtrail-log-basics/python/src .venv/bin/python -m pytest 00-aws-security-foundations/03-cloudtrail-log-basics/python/tests
```

## 대표 출력 예시

```text
ingested 4 records
```

## 구현 메모

ETL은 작은 fixture에서도 반복 검증이 가능하도록 단순한 입력과 출력 구조를 유지합니다.
