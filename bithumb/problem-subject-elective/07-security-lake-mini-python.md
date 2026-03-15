# 07-security-lake-mini-python 문제지

## 왜 중요한가

Security Lake 개념을 로컬로 축소 구현해, 로그를 저장하고 미리 정의한 detection query로 이상 행위를 찾아야 합니다. 핵심은 적재와 탐지가 한 흐름이라는 점을 작은 규모에서 재현하는 것입니다.

## 목표

시작 위치의 구현을 완성해 로컬 단일 테이블 흐름에 집중합니다와 분산 저장소나 대용량 최적화는 다루지 않습니다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../01-cloud-security-core/07-security-lake-mini/python/src/security_lake_mini/__init__.py`
- `../01-cloud-security-core/07-security-lake-mini/python/src/security_lake_mini/cli.py`
- `../01-cloud-security-core/07-security-lake-mini/python/src/security_lake_mini/lake.py`
- `../01-cloud-security-core/07-security-lake-mini/python/tests/test_cli.py`
- `../01-cloud-security-core/07-security-lake-mini/python/tests/test_lake.py`
- `../01-cloud-security-core/07-security-lake-mini/problem/data/cloudtrail_suspicious.json`

## starter code / 입력 계약

- `../01-cloud-security-core/07-security-lake-mini/python/src/security_lake_mini/__init__.py`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- 로컬 단일 테이블 흐름에 집중합니다.
- 분산 저장소나 대용량 최적화는 다루지 않습니다.

## 제외 범위

- `../01-cloud-security-core/07-security-lake-mini/problem/data/cloudtrail_suspicious.json` fixture나 trace를 읽지 않고 동작을 추측해서 구현하지 않는다.
- 같은 주제의 다른 runtime 구현을 섞어 읽지 않는다.

## 성공 체크리스트

- 핵심 흐름은 `ingest`와 `Alert`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `test_cli_ingest_returns_json_alerts`와 `test_security_lake_generates_expected_alerts`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../01-cloud-security-core/07-security-lake-mini/problem/data/cloudtrail_suspicious.json` fixture/trace 기준으로 결과를 대조했다.
- `cd /Users/woopinbell/work/book-task-3/bithumb/01-cloud-security-core/07-security-lake-mini/python && PYTHONPATH=src python3 -m pytest`가 통과한다.

## 검증 방법

```bash
cd /Users/woopinbell/work/book-task-3/bithumb/01-cloud-security-core/07-security-lake-mini/python && PYTHONPATH=src python3 -m pytest
```

- 이 검증 명령을 직접 실행하려면 현재 셸에 `pytest`가 설치돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`07-security-lake-mini-python_answer.md`](07-security-lake-mini-python_answer.md)에서 확인한다.
