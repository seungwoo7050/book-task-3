# Python 구현

아래 내용은 모두 레포 루트 기준입니다.

## 다루는 범위

- CloudTrail fixture를 DuckDB와 Parquet에 적재합니다.
- preset detection query를 실행해 alert를 생성합니다.
- 로컬에서 security lake 개념을 축소 재현합니다.

## 실행 예시

```bash
make venv
mkdir -p .artifacts/security-lake-mini
PYTHONPATH=01-cloud-security-core/07-security-lake-mini/python/src .venv/bin/python -m security_lake_mini.cli 01-cloud-security-core/07-security-lake-mini/problem/data/cloudtrail_suspicious.json .artifacts/security-lake-mini/lake.duckdb .artifacts/security-lake-mini/events.parquet
```

## 테스트

```bash
PYTHONPATH=01-cloud-security-core/07-security-lake-mini/python/src .venv/bin/python -m pytest 01-cloud-security-core/07-security-lake-mini/python/tests
```

## 상태

`verified`

## 구현 메모

CLI는 입력 로그와 출력 lake 경로를 명시적으로 받아 데모와 테스트에서 재사용하기 쉽습니다.
