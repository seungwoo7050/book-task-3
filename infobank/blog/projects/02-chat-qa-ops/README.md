# 02 챗봇 상담 품질 관리 blog

이 디렉터리는 `02-chat-qa-ops`를 `source-first` 방식으로 다시 읽는 project-level blog 시리즈다. chronology는 현재 `projects/02-chat-qa-ops` 아래의 capstone 버전, FastAPI/CLI 코드, React 페이지, demo 문서, 테스트, 실제 검증 명령만으로 복원했다.

## source set

- [`../../../projects/02-chat-qa-ops/README.md`](../../../projects/02-chat-qa-ops/README.md)
- [`../../../projects/02-chat-qa-ops/capstone/README.md`](../../../projects/02-chat-qa-ops/capstone/README.md)
- [`../../../projects/02-chat-qa-ops/capstone/v0-initial-demo/README.md`](../../../projects/02-chat-qa-ops/capstone/v0-initial-demo/README.md)
- [`../../../projects/02-chat-qa-ops/capstone/v1-regression-hardening/README.md`](../../../projects/02-chat-qa-ops/capstone/v1-regression-hardening/README.md)
- [`../../../projects/02-chat-qa-ops/capstone/v2-submission-polish/README.md`](../../../projects/02-chat-qa-ops/capstone/v2-submission-polish/README.md)
- [`../../../projects/02-chat-qa-ops/capstone/v2-submission-polish/python/Makefile`](../../../projects/02-chat-qa-ops/capstone/v2-submission-polish/python/Makefile)
- [`../../../projects/02-chat-qa-ops/capstone/v2-submission-polish/python/backend/src/evaluator/pipeline.py`](../../../projects/02-chat-qa-ops/capstone/v2-submission-polish/python/backend/src/evaluator/pipeline.py)
- [`../../../projects/02-chat-qa-ops/capstone/v2-submission-polish/python/tests/mp3/test_retrieval_v2.py`](../../../projects/02-chat-qa-ops/capstone/v2-submission-polish/python/tests/mp3/test_retrieval_v2.py)
- [`../../../projects/02-chat-qa-ops/capstone/v2-submission-polish/react/src/pages/Overview.tsx`](../../../projects/02-chat-qa-ops/capstone/v2-submission-polish/react/src/pages/Overview.tsx)
- [`../../../projects/02-chat-qa-ops/capstone/v3-self-hosted-oss/python/backend/src/api/routes/auth.py`](../../../projects/02-chat-qa-ops/capstone/v3-self-hosted-oss/python/backend/src/api/routes/auth.py)
- [`../../../projects/02-chat-qa-ops/capstone/v3-self-hosted-oss/python/backend/src/api/routes/datasets.py`](../../../projects/02-chat-qa-ops/capstone/v3-self-hosted-oss/python/backend/src/api/routes/datasets.py)
- [`../../../projects/02-chat-qa-ops/capstone/v3-self-hosted-oss/python/backend/src/services/jobs.py`](../../../projects/02-chat-qa-ops/capstone/v3-self-hosted-oss/python/backend/src/services/jobs.py)

## 읽는 순서

1. [`00-series-map.md`](00-series-map.md)
2. [`10-development-timeline.md`](10-development-timeline.md)
3. [`../../../projects/02-chat-qa-ops/README.md`](../../../projects/02-chat-qa-ops/README.md)

## 검증 진입점

- `cd projects/02-chat-qa-ops/capstone/v2-submission-polish/python`
- `UV_PYTHON=python3.12 uv sync --extra dev`
- `UV_PYTHON=python3.12 make gate-all`
- `UV_PYTHON=python3.12 make smoke-postgres`

## chronology 메모

- 이 프로젝트도 git history가 stage/capstone 재배치 중심이라 실제 세션 시각을 복원하기 어렵다.
- 그래서 `Day / Session` 형식을 쓰고, 각 세션은 `v0 -> v1 -> v2 -> v3` 버전 사다리로 고정한다.
- 실제 검증 기준은 `make gate-all`이다. 현재 환경에서 `ruff`, `mypy`, MP1~MP5 backend tests, frontend tests가 모두 통과했고, optional `make smoke-postgres`도 `PostgreSQL smoke verification passed`를 반환했다.
