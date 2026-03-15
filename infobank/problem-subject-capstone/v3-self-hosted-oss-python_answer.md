# v3-self-hosted-oss-python 답안지

이 문서는 문제지를 다시 넘기지 않고도 해답을 재구성할 수 있도록, 실제 구현 파일과 테스트만 기준으로 정리한 답안지다.

## 한 줄 해답

v3-self-hosted-oss의 목표는 v2를 single-team self-hosted QA Ops 도구로 끌어올리는 것이다. 데모가 아니라 설치 가능한 운영형 아카이브로 한 단계 더 확장하는 버전이다. 핵심은 `get_session`와 `get_current_admin`, `get_current_admin_optional` 흐름을 구현하고 테스트를 통과시키는 것이다.

## 문제를 푸는 핵심 전략

- single admin auth
- transcript JSONL import
- Markdown ZIP KB import
- 첫 진입점은 `../projects/02-chat-qa-ops/capstone/v3-self-hosted-oss/python/backend/src/api/__init__.py`이고, 여기서 `get_session`와 `get_current_admin` 흐름을 먼저 붙잡은 뒤 나머지 파일로 확장한다.

## 코드 워크스루

- `../projects/02-chat-qa-ops/capstone/v3-self-hosted-oss/python/backend/src/api/__init__.py`: 패키지 공개 경계와 route wiring 순서를 고정하는 진입 파일이다.
- `../projects/02-chat-qa-ops/capstone/v3-self-hosted-oss/python/backend/src/api/dependencies.py`: `get_session`, `get_current_admin`, `get_current_admin_optional`가 핵심 흐름과 상태 전이를 묶는다.
- `../projects/02-chat-qa-ops/capstone/v3-self-hosted-oss/python/backend/src/api/error_responses.py`: `dependency_unavailable_response`가 핵심 흐름과 상태 전이를 묶는다.
- `../projects/02-chat-qa-ops/capstone/v3-self-hosted-oss/python/backend/src/api/main.py`: `lifespan`, `healthz`가 핵심 흐름과 상태 전이를 묶는다.
- `../projects/02-chat-qa-ops/capstone/v3-self-hosted-oss/python/backend/src/api/routes/__init__.py`: 패키지 공개 경계와 route wiring 순서를 고정하는 진입 파일이다.
- `../projects/02-chat-qa-ops/capstone/v3-self-hosted-oss/python/tests/conftest.py`: pytest fixture와 테스트 환경 구성을 고정하는 파일이다.
- `../projects/02-chat-qa-ops/capstone/v3-self-hosted-oss/python/tests/mp1/test_auth_runtime.py`: `test_auth_bootstrap_and_session_cookie`, `test_sample_assets_are_bootstrapped_for_first_run`가 통과 조건과 회귀 포인트를 잠근다.
- `../projects/02-chat-qa-ops/capstone/v3-self-hosted-oss/python/tests/mp2/test_import_contracts.py`: `_build_kb_zip`, `test_dataset_import_contract_returns_record_count`, `test_dataset_import_validation_surfaces_line_errors`가 통과 조건과 회귀 포인트를 잠근다.

## 정답을 재구성하는 절차

1. `../projects/02-chat-qa-ops/capstone/v3-self-hosted-oss/python/backend/src/api/__init__.py`를 먼저 열어 입력과 상태 전이의 기준점을 잡는다.
2. `isolated_db` 등이 요구하는 순서대로 핵심 상태 전이와 예외 흐름을 채운다.
3. `cd /Users/woopinbell/work/book-task-3/infobank/projects/02-chat-qa-ops/capstone/v3-self-hosted-oss/python && python3 -m pytest`를 실행해 결과를 잠그고, 필요하면 남은 검증 명령까지 이어서 돌린다.

## 검증과 실패 포인트

```bash
cd /Users/woopinbell/work/book-task-3/infobank/projects/02-chat-qa-ops/capstone/v3-self-hosted-oss/python && python3 -m pytest
```

```bash
bash /Users/woopinbell/work/book-task-3/infobank/projects/02-chat-qa-ops/capstone/v3-self-hosted-oss/python/scripts/verify_mp_integrity.sh
```

- 상위 카탈로그나 보조 문서만 보고 구현을 추측하지 않고, 지금 열어 둔 source/test를 정답 근거로 고정한다.
- `isolated_db`와 `client`가 잠근 상태 전이와 입력 계약을 빼먹지 않는다.
- 완성 직전에만 한 번 돌리지 말고, 상태 전이를 건드릴 때마다 `cd /Users/woopinbell/work/book-task-3/infobank/projects/02-chat-qa-ops/capstone/v3-self-hosted-oss/python && python3 -m pytest`로 회귀를 조기에 잡는다.

## 소스 근거

- `../projects/02-chat-qa-ops/capstone/v3-self-hosted-oss/python/backend/src/api/__init__.py`
- `../projects/02-chat-qa-ops/capstone/v3-self-hosted-oss/python/backend/src/api/dependencies.py`
- `../projects/02-chat-qa-ops/capstone/v3-self-hosted-oss/python/backend/src/api/error_responses.py`
- `../projects/02-chat-qa-ops/capstone/v3-self-hosted-oss/python/backend/src/api/main.py`
- `../projects/02-chat-qa-ops/capstone/v3-self-hosted-oss/python/backend/src/api/routes/__init__.py`
- `../projects/02-chat-qa-ops/capstone/v3-self-hosted-oss/python/tests/conftest.py`
- `../projects/02-chat-qa-ops/capstone/v3-self-hosted-oss/python/tests/mp1/test_auth_runtime.py`
- `../projects/02-chat-qa-ops/capstone/v3-self-hosted-oss/python/tests/mp2/test_import_contracts.py`
- `../projects/02-chat-qa-ops/capstone/v3-self-hosted-oss/python/backend/data/fixtures/replay_sessions.yaml`
- `../projects/02-chat-qa-ops/capstone/v3-self-hosted-oss/python/backend/golden_set/phase1_seed.yaml`
