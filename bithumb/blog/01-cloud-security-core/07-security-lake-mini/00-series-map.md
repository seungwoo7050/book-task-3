# 07 Security Lake Mini - Series Map

이 시리즈는 `notion/` 없이 `README.md`, `problem/README.md`, `python/README.md`, `lake.py`, `cli.py`, `test_lake.py`, `test_cli.py`, 실제 재검증 명령만으로 다시 읽은 학습 로그입니다.

## 이 시리즈가 답하는 질문

- Security Lake 개념을 local 단일 테이블 수준으로 줄였을 때도 어떤 detection query를 반복 실행할 수 있을까
- 로그 적재와 alert 생성이 한 흐름이라는 점을 가장 작은 코드로 어떻게 설명할까

## 실제 구현 표면

- CloudTrail fixture를 DuckDB `lake_events`와 Parquet 파일로 적재합니다.
- `CreateAccessKey`, `PutBucketAcl`, `AuthorizeSecurityGroupIngress`, `DeleteTrail`, root `ConsoleLogin`을 `LAKE-001`부터 `LAKE-005`로 변환합니다.
- CLI는 적재 후 바로 detection query 결과 JSON을 출력합니다.

## 대표 검증 엔트리

- `mkdir -p .artifacts/security-lake-mini && PYTHONPATH=01-cloud-security-core/07-security-lake-mini/python/src .venv/bin/python -m security_lake_mini.cli 01-cloud-security-core/07-security-lake-mini/problem/data/cloudtrail_suspicious.json .artifacts/security-lake-mini/lake.duckdb .artifacts/security-lake-mini/events.parquet`
- `PYTHONPATH=01-cloud-security-core/07-security-lake-mini/python/src .venv/bin/python -m pytest 01-cloud-security-core/07-security-lake-mini/python/tests`

## 읽는 순서

1. [프로젝트 README](../../../01-cloud-security-core/07-security-lake-mini/README.md)
2. [문제 정의](../../../01-cloud-security-core/07-security-lake-mini/problem/README.md)
3. [실행 진입점](../../../01-cloud-security-core/07-security-lake-mini/python/README.md)
4. [대표 테스트](../../../01-cloud-security-core/07-security-lake-mini/python/tests/test_lake.py)
5. [CLI 테스트](../../../01-cloud-security-core/07-security-lake-mini/python/tests/test_cli.py)
6. [핵심 구현](../../../01-cloud-security-core/07-security-lake-mini/python/src/security_lake_mini/lake.py)
7. [개발 타임라인](10-development-timeline.md)

## 근거 파일

- [README.md](../../../01-cloud-security-core/07-security-lake-mini/README.md)
- [problem/README.md](../../../01-cloud-security-core/07-security-lake-mini/problem/README.md)
- [python/README.md](../../../01-cloud-security-core/07-security-lake-mini/python/README.md)
- [lake.py](../../../01-cloud-security-core/07-security-lake-mini/python/src/security_lake_mini/lake.py)
- [cli.py](../../../01-cloud-security-core/07-security-lake-mini/python/src/security_lake_mini/cli.py)
- [test_lake.py](../../../01-cloud-security-core/07-security-lake-mini/python/tests/test_lake.py)
- [test_cli.py](../../../01-cloud-security-core/07-security-lake-mini/python/tests/test_cli.py)

## Git Anchor

- `2026-03-10 a4b4aae docs: enhance bithumb`
- `2026-03-11 a9c65b3 Track 2에 대한 전반적인 개선 완료 (infobank, bithumb, game-server)`
