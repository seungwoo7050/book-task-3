# 02-domain-fixtures-and-chat-harness-python 문제지

## 왜 중요한가

fixture와 replay를 어떻게 분리해야 회귀 테스트와 golden set 생성이 흔들리지 않는가?

## 목표

시작 위치의 구현을 완성해 같은 replay 입력에 대해 항상 같은 retrieved doc order가 나온다, fixture 파일과 harness 코드가 분리되어 수정 범위가 명확하다, 후속 golden set과 version compare 입력으로 이어질 수 있다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../projects/02-chat-qa-ops/stages/02-domain-fixtures-and-chat-harness/python/src/stage02/__init__.py`
- `../projects/02-chat-qa-ops/stages/02-domain-fixtures-and-chat-harness/python/src/stage02/harness.py`
- `../projects/02-chat-qa-ops/stages/02-domain-fixtures-and-chat-harness/python/tests/conftest.py`
- `../projects/02-chat-qa-ops/stages/02-domain-fixtures-and-chat-harness/python/tests/test_harness.py`
- `../projects/02-chat-qa-ops/stages/02-domain-fixtures-and-chat-harness/python/data/replay_sessions.json`
- `../projects/02-chat-qa-ops/stages/02-domain-fixtures-and-chat-harness/python/pyproject.toml`

## starter code / 입력 계약

- `../projects/02-chat-qa-ops/stages/02-domain-fixtures-and-chat-harness/python/src/stage02/__init__.py`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- 같은 replay 입력에 대해 항상 같은 retrieved doc order가 나온다.
- fixture 파일과 harness 코드가 분리되어 수정 범위가 명확하다.
- 후속 golden set과 version compare 입력으로 이어질 수 있다.

## 제외 범위

- `../projects/02-chat-qa-ops/stages/02-domain-fixtures-and-chat-harness/python/data/replay_sessions.json` fixture나 trace를 읽지 않고 동작을 추측해서 구현하지 않는다.
- 같은 주제의 다른 runtime 구현을 섞어 읽지 않는다.

## 성공 체크리스트

- 핵심 흐름은 `seed_knowledge_base`와 `retrieve`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `test_seeded_kb_reproducible`와 `test_replay_harness_reproduces_expected_docs`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../projects/02-chat-qa-ops/stages/02-domain-fixtures-and-chat-harness/python/data/replay_sessions.json` fixture/trace 기준으로 결과를 대조했다.
- `cd /Users/woopinbell/work/book-task-3/infobank/projects/02-chat-qa-ops/stages/02-domain-fixtures-and-chat-harness/python && PYTHONPATH=src python3 -m pytest`가 통과한다.

## 검증 방법

```bash
cd /Users/woopinbell/work/book-task-3/infobank/projects/02-chat-qa-ops/stages/02-domain-fixtures-and-chat-harness/python && PYTHONPATH=src python3 -m pytest
```

- 이 검증 명령을 직접 실행하려면 현재 셸에 `pytest`가 설치돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`02-domain-fixtures-and-chat-harness-python_answer.md`](02-domain-fixtures-and-chat-harness-python_answer.md)에서 확인한다.
