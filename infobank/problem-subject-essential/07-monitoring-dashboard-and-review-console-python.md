# 07-monitoring-dashboard-and-review-console-python 문제지

## 왜 중요한가

평가 결과와 trace를 운영 콘솔에서 어떻게 읽히는 형태로 보여줄 것인가?

## 목표

시작 위치의 구현을 완성해 운영자가 평균 점수, failure top, 세션 trace, compare delta를 한 곳에서 읽을 수 있다, backend contract와 frontend mocked tests가 같은 payload shape를 공유한다, run label과 retrieval version 같은 lineage 정보가 session review에 노출된다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../projects/02-chat-qa-ops/stages/07-monitoring-dashboard-and-review-console/python/src/stage07/__init__.py`
- `../projects/02-chat-qa-ops/stages/07-monitoring-dashboard-and-review-console/python/src/stage07/app.py`
- `../projects/02-chat-qa-ops/stages/07-monitoring-dashboard-and-review-console/python/tests/conftest.py`
- `../projects/02-chat-qa-ops/stages/07-monitoring-dashboard-and-review-console/python/tests/test_api.py`
- `../projects/02-chat-qa-ops/stages/07-monitoring-dashboard-and-review-console/python/pyproject.toml`

## starter code / 입력 계약

- `../projects/02-chat-qa-ops/stages/07-monitoring-dashboard-and-review-console/python/src/stage07/__init__.py`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- 운영자가 평균 점수, failure top, 세션 trace, compare delta를 한 곳에서 읽을 수 있다.
- backend contract와 frontend mocked tests가 같은 payload shape를 공유한다.
- run label과 retrieval version 같은 lineage 정보가 session review에 노출된다.

## 제외 범위

- 같은 주제의 다른 runtime 구현을 섞어 읽지 않는다.

## 성공 체크리스트

- 핵심 흐름은 `overview`와 `failures`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `test_dashboard_snapshot_endpoints`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `cd /Users/woopinbell/work/book-task-3/infobank/projects/02-chat-qa-ops/stages/07-monitoring-dashboard-and-review-console/python && PYTHONPATH=src python3 -m pytest`가 통과한다.

## 검증 방법

```bash
cd /Users/woopinbell/work/book-task-3/infobank/projects/02-chat-qa-ops/stages/07-monitoring-dashboard-and-review-console/python && PYTHONPATH=src python3 -m pytest
```

- 이 검증 명령을 직접 실행하려면 현재 셸에 `pytest`가 설치돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`07-monitoring-dashboard-and-review-console-python_answer.md`](07-monitoring-dashboard-and-review-console-python_answer.md)에서 확인한다.
