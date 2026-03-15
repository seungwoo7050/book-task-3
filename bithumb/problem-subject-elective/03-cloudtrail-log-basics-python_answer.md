# 03-cloudtrail-log-basics-python 답안지

이 문서는 문제지를 다시 넘기지 않고도 해답을 재구성할 수 있도록, 실제 구현 파일과 테스트만 기준으로 정리한 답안지다.

## 한 줄 해답

시작 위치의 구현을 완성해 실제 운영 규모의 대용량 적재는 다루지 않습니다와 정규화 필드는 이후 프로젝트가 쓰는 최소 공통 필드로 제한합니다를 한 흐름으로 설명하고 검증한다. 핵심은 `EventRecord`와 `normalize_cloudtrail_events`, `normalize_vpc_flow_logs` 흐름을 구현하고 테스트를 통과시키는 것이다.

## 문제를 푸는 핵심 전략

- 실제 운영 규모의 대용량 적재는 다루지 않습니다.
- 정규화 필드는 이후 프로젝트가 쓰는 최소 공통 필드로 제한합니다.
- 첫 진입점은 `../00-aws-security-foundations/03-cloudtrail-log-basics/python/src/cloudtrail_log_basics/__init__.py`이고, 여기서 `EventRecord`와 `normalize_cloudtrail_events` 흐름을 먼저 붙잡은 뒤 나머지 파일로 확장한다.
- 검증 기준은 `_problem_data`와 `test_etl_ingests_cloudtrail_and_vpc_flow_logs` 테스트가 먼저 잠근 동작부터 맞추는 것이다.

## 코드 워크스루

- `../00-aws-security-foundations/03-cloudtrail-log-basics/python/src/cloudtrail_log_basics/__init__.py`: 패키지 진입점과 공개 API 경계를 고정하는 파일이다.
- `../00-aws-security-foundations/03-cloudtrail-log-basics/python/src/cloudtrail_log_basics/etl.py`: `EventRecord`, `normalize_cloudtrail_events`, `normalize_vpc_flow_logs`, `ingest_records`가 핵심 흐름과 상태 전이를 묶는다.
- `../00-aws-security-foundations/03-cloudtrail-log-basics/python/tests/test_etl.py`: `_problem_data`, `test_etl_ingests_cloudtrail_and_vpc_flow_logs`가 통과 조건과 회귀 포인트를 잠근다.
- `../00-aws-security-foundations/03-cloudtrail-log-basics/problem/data/cloudtrail_events.json`: 입력 fixture나 계약 데이터를 고정하는 근거 파일이다.
- `../00-aws-security-foundations/03-cloudtrail-log-basics/problem/data/vpc_flow_logs.json`: 입력 fixture나 계약 데이터를 고정하는 근거 파일이다.
- `EventRecord` 구현은 `_problem_data` 등이 잠근 입력 계약과 상태 전이를 그대로 만족해야 한다.
- 회귀 게이트는 `cd /Users/woopinbell/work/book-task-3/bithumb/00-aws-security-foundations/03-cloudtrail-log-basics/python && PYTHONPATH=src python3 -m pytest`이며, 핵심 상태 전이를 바꿀 때마다 중간 검증으로 다시 실행한다.
- `../00-aws-security-foundations/03-cloudtrail-log-basics/problem/data/cloudtrail_events.json` 등을 함께 읽어 입력 fixture나 trace를 추측이 아니라 근거로 고정한다.

## 정답을 재구성하는 절차

1. `../00-aws-security-foundations/03-cloudtrail-log-basics/python/src/cloudtrail_log_basics/__init__.py`를 먼저 열어 입력과 상태 전이의 기준점을 잡는다.
2. `_problem_data` 등이 요구하는 순서대로 핵심 상태 전이와 예외 흐름을 채운다.
3. `cd /Users/woopinbell/work/book-task-3/bithumb/00-aws-security-foundations/03-cloudtrail-log-basics/python && PYTHONPATH=src python3 -m pytest`를 실행해 결과를 잠그고, 필요하면 남은 검증 명령까지 이어서 돌린다.

## 검증과 실패 포인트

```bash
cd /Users/woopinbell/work/book-task-3/bithumb/00-aws-security-foundations/03-cloudtrail-log-basics/python && PYTHONPATH=src python3 -m pytest
```

- 상위 카탈로그나 보조 문서만 보고 구현을 추측하지 않고, 지금 열어 둔 source/test를 정답 근거로 고정한다.
- `_problem_data`와 `test_etl_ingests_cloudtrail_and_vpc_flow_logs`가 잠근 상태 전이와 입력 계약을 빼먹지 않는다.
- 완성 직전에만 한 번 돌리지 말고, 상태 전이를 건드릴 때마다 `cd /Users/woopinbell/work/book-task-3/bithumb/00-aws-security-foundations/03-cloudtrail-log-basics/python && PYTHONPATH=src python3 -m pytest`로 회귀를 조기에 잡는다.

## 소스 근거

- `../00-aws-security-foundations/03-cloudtrail-log-basics/python/src/cloudtrail_log_basics/__init__.py`
- `../00-aws-security-foundations/03-cloudtrail-log-basics/python/src/cloudtrail_log_basics/etl.py`
- `../00-aws-security-foundations/03-cloudtrail-log-basics/python/tests/test_etl.py`
- `../00-aws-security-foundations/03-cloudtrail-log-basics/problem/data/cloudtrail_events.json`
- `../00-aws-security-foundations/03-cloudtrail-log-basics/problem/data/vpc_flow_logs.json`
