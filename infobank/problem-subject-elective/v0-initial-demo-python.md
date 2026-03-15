# v0-initial-demo-python 문제지

## 왜 중요한가

v0-initial-demo는 Chat QA Ops 트랙에서 처음 끝까지 실행해 볼 수 있는 baseline snapshot이다. rubric, guardrail, evidence verifier, judge/score merge, golden replay, 운영 대시보드를 한 번에 연결해 "품질 관리 시스템이 실제로 어떻게 보이는지"를 보여 주는 것이 목표다.

## 목표

처음 보는 사람도 로컬에서 바로 실행해 볼 수 있는 상담 품질 QA Ops baseline을 만든다. 품질 평가 파이프라인과 운영 UI를 한 번 끝까지 연결해 보는 것이 핵심이다.

## 시작 위치

- `../projects/02-chat-qa-ops/capstone/v0-initial-demo/python/backend/src/api/__init__.py`
- `../projects/02-chat-qa-ops/capstone/v0-initial-demo/python/backend/src/api/dependencies.py`
- `../projects/02-chat-qa-ops/capstone/v0-initial-demo/python/backend/src/api/error_responses.py`
- `../projects/02-chat-qa-ops/capstone/v0-initial-demo/python/backend/src/api/main.py`
- `../projects/02-chat-qa-ops/capstone/v0-initial-demo/python/tests/conftest.py`
- `../projects/02-chat-qa-ops/capstone/v0-initial-demo/python/tests/mp1/test_chat_runtime.py`
- `../projects/02-chat-qa-ops/capstone/v0-initial-demo/python/backend/data/fixtures/replay_sessions.yaml`
- `../projects/02-chat-qa-ops/capstone/v0-initial-demo/python/backend/golden_set/phase1_seed.yaml`

## starter code / 입력 계약

- `../projects/02-chat-qa-ops/capstone/v0-initial-demo/python/backend/src/api/__init__.py`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- rubric
- rule/guardrail
- evidence verifier
- judge/score merge

## 제외 범위

- `../projects/02-chat-qa-ops/capstone/v0-initial-demo/python/backend/data/fixtures/replay_sessions.yaml` 등 fixture나 trace를 읽지 않고 동작을 추측해서 구현하지 않는다.
- 같은 주제의 다른 runtime 구현을 섞어 읽지 않는다.
- 검증 명령이 통과한다고 해서 입력 계약과 경계 조건까지 자동으로 맞는다고 가정하지 않는다.

## 성공 체크리스트

- 핵심 흐름은 `get_session`와 `dependency_unavailable_response`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `isolated_db`와 `client`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../projects/02-chat-qa-ops/capstone/v0-initial-demo/python/backend/data/fixtures/replay_sessions.yaml` 등 fixture/trace 기준으로 결과를 대조했다.
- `cd /Users/woopinbell/work/book-task-3/infobank/projects/02-chat-qa-ops/capstone/v0-initial-demo/python && python3 -m pytest`가 통과한다.

## 검증 방법

```bash
cd /Users/woopinbell/work/book-task-3/infobank/projects/02-chat-qa-ops/capstone/v0-initial-demo/python && python3 -m pytest
```

```bash
bash /Users/woopinbell/work/book-task-3/infobank/projects/02-chat-qa-ops/capstone/v0-initial-demo/python/scripts/verify_mp_integrity.sh
```

- 이 검증 명령을 직접 실행하려면 현재 셸에 `pytest`가 설치돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`v0-initial-demo-python_answer.md`](v0-initial-demo-python_answer.md)에서 확인한다.
