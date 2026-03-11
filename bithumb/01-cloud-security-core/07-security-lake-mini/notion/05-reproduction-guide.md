# 재현 가이드

## 무엇을 재현하나

- CloudTrail suspicious fixture가 lake DB와 Parquet로 적재되는지
- 다섯 개 detection rule이 기대한 control_id 순서로 alert를 만드는지
- 정규화와 detection이 같은 로컬 흐름 안에서 재현되는지

## 사전 조건

- `python3` 3.13+와 `make venv`가 필요합니다.
- 명령은 모두 레포 루트에서 실행합니다.
- 출력 파일을 보기 위해 `.artifacts/security-lake-mini` 디렉터리를 먼저 만들어 둡니다.

## 가장 짧은 재현 경로

```bash
make venv
mkdir -p .artifacts/security-lake-mini
PYTHONPATH=01-cloud-security-core/07-security-lake-mini/python/src .venv/bin/python -m security_lake_mini.cli 01-cloud-security-core/07-security-lake-mini/problem/data/cloudtrail_suspicious.json .artifacts/security-lake-mini/lake.duckdb .artifacts/security-lake-mini/events.parquet
PYTHONPATH=01-cloud-security-core/07-security-lake-mini/python/src .venv/bin/python -m pytest 01-cloud-security-core/07-security-lake-mini/python/tests
```

## 기대 결과

- CLI JSON에는 `LAKE-001`부터 `LAKE-005`까지 다섯 alert가 포함돼야 합니다.
- `.artifacts/security-lake-mini/events.parquet`가 생성돼야 합니다.
- pytest는 하나의 테스트를 통과하면서 Parquet 생성과 alert 목록 순서를 동시에 검증합니다.

## 결과가 다르면 먼저 볼 파일

- 적재와 query 흐름을 다시 보려면: [../python/src/security_lake_mini/lake.py](../python/src/security_lake_mini/lake.py)
- CLI 진입 흐름을 다시 보려면: [../python/src/security_lake_mini/cli.py](../python/src/security_lake_mini/cli.py)
- 검증 기준을 다시 보려면: [../python/tests/test_lake.py](../python/tests/test_lake.py)
- 입력 fixture를 다시 보려면: [../problem/data/cloudtrail_suspicious.json](../problem/data/cloudtrail_suspicious.json)
- 루트 공통 검증 흐름을 다시 보려면: [../../../Makefile](../../../Makefile)

## 이 재현이 증명하는 것

- 이 재현은 security lake가 거대한 플랫폼 이름이 아니라, 정규화된 로그와 repeatable query를 연결하는 학습 가능한 구조라는 점을 보여 줍니다.
- 학습자는 다섯 alert 이름을 외우기보다, 왜 정규화가 먼저여야 하는지를 설명할 수 있어야 합니다.
