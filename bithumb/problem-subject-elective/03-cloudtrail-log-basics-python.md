# 03-cloudtrail-log-basics-python 문제지

## 왜 중요한가

CloudTrail과 VPC Flow Logs를 그대로 저장하는 대신, 이후 query와 detection에 재사용할 수 있는 공통 이벤트 구조로 정리해야 합니다. 핵심은 로그를 “수집”이 아니라 “분석 가능한 입력”으로 바꾸는 것입니다.

## 목표

시작 위치의 구현을 완성해 실제 운영 규모의 대용량 적재는 다루지 않습니다와 정규화 필드는 이후 프로젝트가 쓰는 최소 공통 필드로 제한합니다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../00-aws-security-foundations/03-cloudtrail-log-basics/python/src/cloudtrail_log_basics/__init__.py`
- `../00-aws-security-foundations/03-cloudtrail-log-basics/python/src/cloudtrail_log_basics/etl.py`
- `../00-aws-security-foundations/03-cloudtrail-log-basics/python/tests/test_etl.py`
- `../00-aws-security-foundations/03-cloudtrail-log-basics/problem/data/cloudtrail_events.json`
- `../00-aws-security-foundations/03-cloudtrail-log-basics/problem/data/vpc_flow_logs.json`

## starter code / 입력 계약

- `../00-aws-security-foundations/03-cloudtrail-log-basics/python/src/cloudtrail_log_basics/__init__.py`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- 실제 운영 규모의 대용량 적재는 다루지 않습니다.
- 정규화 필드는 이후 프로젝트가 쓰는 최소 공통 필드로 제한합니다.

## 제외 범위

- `../00-aws-security-foundations/03-cloudtrail-log-basics/problem/data/cloudtrail_events.json` 등 fixture나 trace를 읽지 않고 동작을 추측해서 구현하지 않는다.
- 같은 주제의 다른 runtime 구현을 섞어 읽지 않는다.

## 성공 체크리스트

- 핵심 흐름은 `EventRecord`와 `normalize_cloudtrail_events`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `_problem_data`와 `test_etl_ingests_cloudtrail_and_vpc_flow_logs`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../00-aws-security-foundations/03-cloudtrail-log-basics/problem/data/cloudtrail_events.json` 등 fixture/trace 기준으로 결과를 대조했다.
- `cd /Users/woopinbell/work/book-task-3/bithumb/00-aws-security-foundations/03-cloudtrail-log-basics/python && PYTHONPATH=src python3 -m pytest`가 통과한다.

## 검증 방법

```bash
cd /Users/woopinbell/work/book-task-3/bithumb/00-aws-security-foundations/03-cloudtrail-log-basics/python && PYTHONPATH=src python3 -m pytest
```

- 이 검증 명령을 직접 실행하려면 현재 셸에 `pytest`가 설치돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`03-cloudtrail-log-basics-python_answer.md`](03-cloudtrail-log-basics-python_answer.md)에서 확인한다.
