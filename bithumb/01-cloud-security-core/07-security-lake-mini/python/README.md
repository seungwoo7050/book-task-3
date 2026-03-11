# Python 구현

아래 내용은 모두 레포 루트 기준입니다.

## 구현한 답의 범위

- CloudTrail fixture를 DuckDB와 Parquet에 적재합니다.
- preset detection query를 실행해 alert를 생성합니다.
- 로컬에서 security lake 개념을 축소 재현합니다.

## 핵심 엔트리포인트

- `python/src/security_lake_mini/lake.py`
- `python/src/security_lake_mini/cli.py`

## 실행

```bash
make venv
mkdir -p .artifacts/security-lake-mini
PYTHONPATH=01-cloud-security-core/07-security-lake-mini/python/src .venv/bin/python -m security_lake_mini.cli 01-cloud-security-core/07-security-lake-mini/problem/data/cloudtrail_suspicious.json .artifacts/security-lake-mini/lake.duckdb .artifacts/security-lake-mini/events.parquet
```

## 테스트

```bash
PYTHONPATH=01-cloud-security-core/07-security-lake-mini/python/src .venv/bin/python -m pytest 01-cloud-security-core/07-security-lake-mini/python/tests
```

## 대표 출력 예시

```json
[
  {
    "control_id": "LAKE-001",
    "title": "Detected suspicious event: CreateAccessKey",
    "event_name": "CreateAccessKey",
    "actor": "arn:aws:iam::123456789012:user/devops",
    "occurred_at": "2026-03-07T10:00:00Z"
  }
]
```

## 구현 메모

CLI는 입력 로그와 출력 lake 경로를 명시적으로 받아 데모와 테스트에서 재사용하기 쉽습니다.
