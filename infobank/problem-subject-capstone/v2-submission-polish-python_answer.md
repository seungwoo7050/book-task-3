# v2-submission-polish-python 답안지

이 문서는 문제지를 다시 넘기지 않고도 해답을 재구성할 수 있도록, 실제 구현 파일과 테스트만 기준으로 정리한 답안지다.

## 한 줄 해답

v1을 바탕으로 개선 실험 결과를 다시 증빙하고, 최종 runbook과 발표 자료까지 포함한 제출 마감본을 만든다. 핵심은 `get_session`와 `dependency_unavailable_response`, `lifespan` 흐름을 구현하고 테스트를 통과시키는 것이다.

## 문제를 푸는 핵심 전략

- 개선 실험 1개 이상
- baseline 대비 향상 증빙
- final runbook
- 첫 진입점은 `../projects/02-chat-qa-ops/capstone/v2-submission-polish/python/backend/src/api/__init__.py`이고, 여기서 `get_session`와 `dependency_unavailable_response` 흐름을 먼저 붙잡은 뒤 나머지 파일로 확장한다.

## 코드 워크스루

- `../projects/02-chat-qa-ops/capstone/v2-submission-polish/python/backend/src/api/__init__.py`: 패키지 공개 경계와 route wiring 순서를 고정하는 진입 파일이다.
- `../projects/02-chat-qa-ops/capstone/v2-submission-polish/python/backend/src/api/dependencies.py`: `get_session`가 핵심 흐름과 상태 전이를 묶는다.
- `../projects/02-chat-qa-ops/capstone/v2-submission-polish/python/backend/src/api/error_responses.py`: `dependency_unavailable_response`가 핵심 흐름과 상태 전이를 묶는다.
- `../projects/02-chat-qa-ops/capstone/v2-submission-polish/python/backend/src/api/main.py`: `lifespan`, `healthz`가 핵심 흐름과 상태 전이를 묶는다.
- `../projects/02-chat-qa-ops/capstone/v2-submission-polish/python/backend/src/api/routes/__init__.py`: 패키지 공개 경계와 route wiring 순서를 고정하는 진입 파일이다.
- `../projects/02-chat-qa-ops/capstone/v2-submission-polish/python/tests/conftest.py`: pytest fixture와 테스트 환경 구성을 고정하는 파일이다.
- `../projects/02-chat-qa-ops/capstone/v2-submission-polish/python/tests/mp1/test_chat_runtime.py`: `test_healthcheck`, `test_chat_creates_conversation_and_turn`, `test_chat_appends_turn_in_same_conversation`가 통과 조건과 회귀 포인트를 잠근다.
- `../projects/02-chat-qa-ops/capstone/v2-submission-polish/python/tests/mp2/test_rule_engine.py`: `test_forbidden_promise_is_critical`, `test_pii_detection_is_critical`, `test_mandatory_notice_warning`가 통과 조건과 회귀 포인트를 잠근다.

## 정답을 재구성하는 절차

1. `../projects/02-chat-qa-ops/capstone/v2-submission-polish/python/backend/src/api/__init__.py`를 먼저 열어 입력과 상태 전이의 기준점을 잡는다.
2. `isolated_db` 등이 요구하는 순서대로 핵심 상태 전이와 예외 흐름을 채운다.
3. `cd /Users/woopinbell/work/book-task-3/infobank/projects/02-chat-qa-ops/capstone/v2-submission-polish/python && python3 -m pytest`를 실행해 결과를 잠그고, 필요하면 남은 검증 명령까지 이어서 돌린다.

## 검증과 실패 포인트

```bash
cd /Users/woopinbell/work/book-task-3/infobank/projects/02-chat-qa-ops/capstone/v2-submission-polish/python && python3 -m pytest
```

```bash
bash /Users/woopinbell/work/book-task-3/infobank/projects/02-chat-qa-ops/capstone/v2-submission-polish/python/scripts/verify_mp_integrity.sh
```

- 상위 카탈로그나 보조 문서만 보고 구현을 추측하지 않고, 지금 열어 둔 source/test를 정답 근거로 고정한다.
- `isolated_db`와 `client`가 잠근 상태 전이와 입력 계약을 빼먹지 않는다.
- 완성 직전에만 한 번 돌리지 말고, 상태 전이를 건드릴 때마다 `cd /Users/woopinbell/work/book-task-3/infobank/projects/02-chat-qa-ops/capstone/v2-submission-polish/python && python3 -m pytest`로 회귀를 조기에 잡는다.

## 소스 근거

- `../projects/02-chat-qa-ops/capstone/v2-submission-polish/python/backend/src/api/__init__.py`
- `../projects/02-chat-qa-ops/capstone/v2-submission-polish/python/backend/src/api/dependencies.py`
- `../projects/02-chat-qa-ops/capstone/v2-submission-polish/python/backend/src/api/error_responses.py`
- `../projects/02-chat-qa-ops/capstone/v2-submission-polish/python/backend/src/api/main.py`
- `../projects/02-chat-qa-ops/capstone/v2-submission-polish/python/backend/src/api/routes/__init__.py`
- `../projects/02-chat-qa-ops/capstone/v2-submission-polish/python/tests/conftest.py`
- `../projects/02-chat-qa-ops/capstone/v2-submission-polish/python/tests/mp1/test_chat_runtime.py`
- `../projects/02-chat-qa-ops/capstone/v2-submission-polish/python/tests/mp2/test_rule_engine.py`
- `../projects/02-chat-qa-ops/capstone/v2-submission-polish/python/backend/data/fixtures/replay_sessions.yaml`
- `../projects/02-chat-qa-ops/capstone/v2-submission-polish/python/backend/golden_set/phase1_seed.yaml`
