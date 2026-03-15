# 02-domain-fixtures-and-chat-harness-python 답안지

이 문서는 문제지를 다시 넘기지 않고도 해답을 재구성할 수 있도록, 실제 구현 파일과 테스트만 기준으로 정리한 답안지다.

## 한 줄 해답

시작 위치의 구현을 완성해 같은 replay 입력에 대해 항상 같은 retrieved doc order가 나온다, fixture 파일과 harness 코드가 분리되어 수정 범위가 명확하다, 후속 golden set과 version compare 입력으로 이어질 수 있다를 한 흐름으로 설명하고 검증한다. 핵심은 `seed_knowledge_base`와 `retrieve`, `run_replay` 흐름을 구현하고 테스트를 통과시키는 것이다.

## 문제를 푸는 핵심 전략

- 같은 replay 입력에 대해 항상 같은 retrieved doc order가 나온다.
- fixture 파일과 harness 코드가 분리되어 수정 범위가 명확하다.
- 후속 golden set과 version compare 입력으로 이어질 수 있다.
- 첫 진입점은 `../projects/02-chat-qa-ops/stages/02-domain-fixtures-and-chat-harness/python/src/stage02/__init__.py`이고, 여기서 `seed_knowledge_base`와 `retrieve` 흐름을 먼저 붙잡은 뒤 나머지 파일로 확장한다.

## 코드 워크스루

- `../projects/02-chat-qa-ops/stages/02-domain-fixtures-and-chat-harness/python/src/stage02/__init__.py`: 패키지 진입점과 공개 API 경계를 고정하는 파일이다.
- `../projects/02-chat-qa-ops/stages/02-domain-fixtures-and-chat-harness/python/src/stage02/harness.py`: `seed_knowledge_base`, `retrieve`, `run_replay`가 핵심 흐름과 상태 전이를 묶는다.
- `../projects/02-chat-qa-ops/stages/02-domain-fixtures-and-chat-harness/python/tests/conftest.py`: pytest fixture와 테스트 환경 구성을 고정하는 파일이다.
- `../projects/02-chat-qa-ops/stages/02-domain-fixtures-and-chat-harness/python/tests/test_harness.py`: `test_seeded_kb_reproducible`, `test_replay_harness_reproduces_expected_docs`가 통과 조건과 회귀 포인트를 잠근다.
- `../projects/02-chat-qa-ops/stages/02-domain-fixtures-and-chat-harness/python/data/replay_sessions.json`: 입력 fixture나 계약 데이터를 고정하는 근거 파일이다.
- `../projects/02-chat-qa-ops/stages/02-domain-fixtures-and-chat-harness/python/pyproject.toml`: 실행 명령과 검증 경로를 고정하는 설정 파일이다.
- `seed_knowledge_base` 구현은 `test_seeded_kb_reproducible` 등이 잠근 입력 계약과 상태 전이를 그대로 만족해야 한다.
- 회귀 게이트는 `cd /Users/woopinbell/work/book-task-3/infobank/projects/02-chat-qa-ops/stages/02-domain-fixtures-and-chat-harness/python && PYTHONPATH=src python3 -m pytest`이며, 핵심 상태 전이를 바꿀 때마다 중간 검증으로 다시 실행한다.

## 정답을 재구성하는 절차

1. `../projects/02-chat-qa-ops/stages/02-domain-fixtures-and-chat-harness/python/src/stage02/__init__.py`를 먼저 열어 입력과 상태 전이의 기준점을 잡는다.
2. `test_seeded_kb_reproducible` 등이 요구하는 순서대로 핵심 상태 전이와 예외 흐름을 채운다.
3. `cd /Users/woopinbell/work/book-task-3/infobank/projects/02-chat-qa-ops/stages/02-domain-fixtures-and-chat-harness/python && PYTHONPATH=src python3 -m pytest`를 실행해 결과를 잠그고, 필요하면 남은 검증 명령까지 이어서 돌린다.

## 검증과 실패 포인트

```bash
cd /Users/woopinbell/work/book-task-3/infobank/projects/02-chat-qa-ops/stages/02-domain-fixtures-and-chat-harness/python && PYTHONPATH=src python3 -m pytest
```

- 상위 카탈로그나 보조 문서만 보고 구현을 추측하지 않고, 지금 열어 둔 source/test를 정답 근거로 고정한다.
- `test_seeded_kb_reproducible`와 `test_replay_harness_reproduces_expected_docs`가 잠근 상태 전이와 입력 계약을 빼먹지 않는다.
- 완성 직전에만 한 번 돌리지 말고, 상태 전이를 건드릴 때마다 `cd /Users/woopinbell/work/book-task-3/infobank/projects/02-chat-qa-ops/stages/02-domain-fixtures-and-chat-harness/python && PYTHONPATH=src python3 -m pytest`로 회귀를 조기에 잡는다.

## 소스 근거

- `../projects/02-chat-qa-ops/stages/02-domain-fixtures-and-chat-harness/python/src/stage02/__init__.py`
- `../projects/02-chat-qa-ops/stages/02-domain-fixtures-and-chat-harness/python/src/stage02/harness.py`
- `../projects/02-chat-qa-ops/stages/02-domain-fixtures-and-chat-harness/python/tests/conftest.py`
- `../projects/02-chat-qa-ops/stages/02-domain-fixtures-and-chat-harness/python/tests/test_harness.py`
- `../projects/02-chat-qa-ops/stages/02-domain-fixtures-and-chat-harness/python/data/replay_sessions.json`
- `../projects/02-chat-qa-ops/stages/02-domain-fixtures-and-chat-harness/python/pyproject.toml`
