# v3-self-hosted-oss-python 문제지

## 왜 중요한가

v3-self-hosted-oss는 v2-submission-polish를 단일 팀용 self-hosted QA Ops OSS 스냅샷으로 확장한 버전이다. 목표는 새 평가 축을 더 붙이는 것이 아니라, 한 팀이 직접 설치하고 로그인해서 dataset import, KB import, evaluation job, dashboard review를 운영할 수 있게 만드는 것이다.

## 목표

v3-self-hosted-oss의 목표는 v2를 single-team self-hosted QA Ops 도구로 끌어올리는 것이다. 데모가 아니라 설치 가능한 운영형 아카이브로 한 단계 더 확장하는 버전이다.

## 시작 위치

- `../projects/02-chat-qa-ops/capstone/v3-self-hosted-oss/python/backend/src/api/__init__.py`
- `../projects/02-chat-qa-ops/capstone/v3-self-hosted-oss/python/backend/src/api/dependencies.py`
- `../projects/02-chat-qa-ops/capstone/v3-self-hosted-oss/python/backend/src/api/error_responses.py`
- `../projects/02-chat-qa-ops/capstone/v3-self-hosted-oss/python/backend/src/api/main.py`
- `../projects/02-chat-qa-ops/capstone/v3-self-hosted-oss/python/tests/conftest.py`
- `../projects/02-chat-qa-ops/capstone/v3-self-hosted-oss/python/tests/mp1/test_auth_runtime.py`
- `../projects/02-chat-qa-ops/capstone/v3-self-hosted-oss/python/backend/data/fixtures/replay_sessions.yaml`
- `../projects/02-chat-qa-ops/capstone/v3-self-hosted-oss/python/backend/golden_set/phase1_seed.yaml`

## starter code / 입력 계약

- `../projects/02-chat-qa-ops/capstone/v3-self-hosted-oss/python/backend/src/api/__init__.py`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- single admin auth
- transcript JSONL import
- Markdown ZIP KB import
- 비동기 evaluation job

## 제외 범위

- multi-tenant
- RBAC / SSO
- live chatbot serving

## 성공 체크리스트

- 핵심 흐름은 `get_session`와 `get_current_admin`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `isolated_db`와 `client`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../projects/02-chat-qa-ops/capstone/v3-self-hosted-oss/python/backend/data/fixtures/replay_sessions.yaml` 등 fixture/trace 기준으로 결과를 대조했다.
- `cd /Users/woopinbell/work/book-task-3/infobank/projects/02-chat-qa-ops/capstone/v3-self-hosted-oss/python && python3 -m pytest`가 통과한다.

## 검증 방법

```bash
cd /Users/woopinbell/work/book-task-3/infobank/projects/02-chat-qa-ops/capstone/v3-self-hosted-oss/python && python3 -m pytest
```

```bash
bash /Users/woopinbell/work/book-task-3/infobank/projects/02-chat-qa-ops/capstone/v3-self-hosted-oss/python/scripts/verify_mp_integrity.sh
```

- 이 검증 명령을 직접 실행하려면 현재 셸에 `pytest`가 설치돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`v3-self-hosted-oss-python_answer.md`](v3-self-hosted-oss-python_answer.md)에서 확인한다.
