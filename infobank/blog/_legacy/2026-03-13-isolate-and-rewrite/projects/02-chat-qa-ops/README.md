# 02 챗봇 상담 품질 관리 blog

이 디렉터리는 `02-chat-qa-ops`를 project-level source-first 시리즈로 다시 읽는 입구다. chronology는 `v0-initial-demo -> v1-regression-hardening -> v2-submission-polish -> v3-self-hosted-oss` 사다리와 실제 재검증 명령을 함께 사용해 복원했다.

## source set

- [`../../../projects/02-chat-qa-ops/README.md`](../../../projects/02-chat-qa-ops/README.md)
- [`../../../projects/02-chat-qa-ops/problem/README.md`](../../../projects/02-chat-qa-ops/problem/README.md)
- [`../../../projects/02-chat-qa-ops/docs/stage-catalog.md`](../../../projects/02-chat-qa-ops/docs/stage-catalog.md)
- [`../../../projects/02-chat-qa-ops/docs/verification-matrix.md`](../../../projects/02-chat-qa-ops/docs/verification-matrix.md)
- [`../../../projects/02-chat-qa-ops/capstone/README.md`](../../../projects/02-chat-qa-ops/capstone/README.md)
- [`../../../projects/02-chat-qa-ops/capstone/v0-initial-demo/python/backend/src/evaluator/pipeline.py`](../../../projects/02-chat-qa-ops/capstone/v0-initial-demo/python/backend/src/evaluator/pipeline.py)
- [`../../../projects/02-chat-qa-ops/capstone/v2-submission-polish/python/backend/src/cli/main.py`](../../../projects/02-chat-qa-ops/capstone/v2-submission-polish/python/backend/src/cli/main.py)
- [`../../../projects/02-chat-qa-ops/capstone/v1-regression-hardening/python/backend/src/core/provider_chain.py`](../../../projects/02-chat-qa-ops/capstone/v1-regression-hardening/python/backend/src/core/provider_chain.py)
- [`../../../projects/02-chat-qa-ops/capstone/v2-submission-polish/python/backend/src/chatbot/retriever.py`](../../../projects/02-chat-qa-ops/capstone/v2-submission-polish/python/backend/src/chatbot/retriever.py)
- [`../../../projects/02-chat-qa-ops/capstone/v2-submission-polish/python/backend/src/chatbot/bot.py`](../../../projects/02-chat-qa-ops/capstone/v2-submission-polish/python/backend/src/chatbot/bot.py)
- [`../../../projects/02-chat-qa-ops/capstone/v2-submission-polish/python/Makefile`](../../../projects/02-chat-qa-ops/capstone/v2-submission-polish/python/Makefile)
- [`../../../projects/02-chat-qa-ops/capstone/v2-submission-polish/docs/demo/proof-artifacts/improvement-report.json`](../../../projects/02-chat-qa-ops/capstone/v2-submission-polish/docs/demo/proof-artifacts/improvement-report.json)
- [`../../../projects/02-chat-qa-ops/capstone/v2-submission-polish/docs/demo/proof-artifacts/api-version-compare.json`](../../../projects/02-chat-qa-ops/capstone/v2-submission-polish/docs/demo/proof-artifacts/api-version-compare.json)
- [`../../../projects/02-chat-qa-ops/capstone/v3-self-hosted-oss/python/backend/src/api/routes/evaluation.py`](../../../projects/02-chat-qa-ops/capstone/v3-self-hosted-oss/python/backend/src/api/routes/evaluation.py)
- [`../../../projects/02-chat-qa-ops/capstone/v3-self-hosted-oss/python/backend/src/api/routes/jobs.py`](../../../projects/02-chat-qa-ops/capstone/v3-self-hosted-oss/python/backend/src/api/routes/jobs.py)
- [`../../../projects/02-chat-qa-ops/capstone/v3-self-hosted-oss/python/backend/src/services/jobs.py`](../../../projects/02-chat-qa-ops/capstone/v3-self-hosted-oss/python/backend/src/services/jobs.py)
- [`../../../projects/02-chat-qa-ops/capstone/v3-self-hosted-oss/python/Makefile`](../../../projects/02-chat-qa-ops/capstone/v3-self-hosted-oss/python/Makefile)
- [`../../../projects/02-chat-qa-ops/capstone/v2-submission-polish/python/tests`](../../../projects/02-chat-qa-ops/capstone/v2-submission-polish/python/tests)
- [`../../../projects/02-chat-qa-ops/capstone/v3-self-hosted-oss/python/tests`](../../../projects/02-chat-qa-ops/capstone/v3-self-hosted-oss/python/tests)
- [`../../../projects/02-chat-qa-ops/capstone/v3-self-hosted-oss/react/src/pages/Jobs.test.tsx`](../../../projects/02-chat-qa-ops/capstone/v3-self-hosted-oss/react/src/pages/Jobs.test.tsx)

## 읽는 순서

1. [`00-series-map.md`](00-series-map.md)
2. [`10-first-qa-evaluation-loop.md`](10-first-qa-evaluation-loop.md)
3. [`20-regression-hardening-and-proof.md`](20-regression-hardening-and-proof.md)
4. [`30-self-hosted-review-ops.md`](30-self-hosted-review-ops.md)
5. [`../../../projects/02-chat-qa-ops/README.md`](../../../projects/02-chat-qa-ops/README.md)

Supporting doc:

- [`_evidence-ledger.md`](_evidence-ledger.md)
- [`_structure-outline.md`](_structure-outline.md)

## 검증 진입점

- 공식 제출 답: `cd ../../../projects/02-chat-qa-ops/capstone/v2-submission-polish/python && UV_PYTHON=python3.12 uv sync --extra dev && UV_PYTHON=python3.12 make init-db && UV_PYTHON=python3.12 make seed-demo && UV_PYTHON=python3.12 make gate-all && UV_PYTHON=python3.12 make smoke-postgres`
- 공식 compare proof: `cd ../../../projects/02-chat-qa-ops/capstone/v2-submission-polish && sed -n '1,120p' docs/demo/proof-artifacts/improvement-report.json && sed -n '1,120p' docs/demo/proof-artifacts/api-version-compare.json`
- 확장 답: `cd ../../../projects/02-chat-qa-ops/capstone/v3-self-hosted-oss/python && UV_PYTHON=python3.12 uv sync --extra dev && UV_PYTHON=python3.12 make gate-all`

## chronology 메모

- project-level git history는 migration commit 하나뿐이라, 실제 chronology는 버전 README와 파일 diff를 기준으로 다시 세웠다.
- 기존 blog는 [`../../_legacy/projects/02-chat-qa-ops`](../../_legacy/projects/02-chat-qa-ops)로 격리했고 입력 근거로 사용하지 않았다.
- `compare`는 현재 CLI가 positional 인자(`compare(baseline, candidate)`)를 기대하는데 Makefile은 여전히 `--baseline/--candidate` 플래그를 써서 drift가 있다. 그래서 개선 수치는 source-level CLI 시그니처와 committed proof artifact JSON을 함께 근거로 잡았다.
