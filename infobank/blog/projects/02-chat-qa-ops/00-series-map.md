# 02 챗봇 상담 품질 관리 시리즈 지도

이 시리즈는 `상담 챗봇 품질 관리`를 단순 챗봇 데모가 아니라, `rubric -> rule/evidence/judge pipeline -> regression compare -> self-hosted evaluation job`으로 읽기 위한 지도다.

## 이 시리즈가 보는 문제

- 상담 품질을 어떤 rubric과 failure taxonomy로 정의해야 rule, evidence, judge가 같은 점수 체계 안에서 동작하는가
- critical short-circuit, evidence verification, provider fallback을 어떤 순서로 합성해야 비용과 안전성을 같이 다룰 수 있는가
- golden set과 version compare를 어디까지 구현해야 "개선됐다"는 주장을 artifact로 남길 수 있는가
- `v3`에서 login, dataset upload, KB bundle upload, evaluation job worker를 더하면 어느 지점부터 self-hosted QA Ops가 되는가

## 실제 구현 표면

- `python/backend/src/chatbot/*`, `evaluator/*`, `api/routes/*`, `core/*`가 품질 평가 파이프라인의 중심이다.
- `python/tests/mp1~mp5/*`는 chat runtime, rule engine, retrieval/evidence, scoring, lineage/runtime contract를 각각 고정한다.
- `react/src/pages/Overview.tsx`, `Failures.tsx`, `SessionReview.tsx`, `EvalRunner.tsx`가 데모 콘솔 표면을 이룬다.
- `docs/demo/`는 실제 시연 흐름과 proof artifact 위치를 정리한다.
- `v3-self-hosted-oss`의 `api/routes/auth.py`, `datasets.py`, `kb_bundles.py`, `jobs.py`, `services/importers.py`, `services/jobs.py`는 로그인, 업로드, job worker 경로를 더한다.

## 대표 검증 엔트리

- `UV_PYTHON=python3.12 uv sync --extra dev`
- `UV_PYTHON=python3.12 make gate-all`
- `UV_PYTHON=python3.12 make smoke-postgres`
- `cd ../react && pnpm test --run`

## 읽는 순서

1. [원 프로젝트 README](../../../projects/02-chat-qa-ops/README.md)
2. [capstone 개요](../../../projects/02-chat-qa-ops/capstone/README.md)
3. [v2 제출 버전 README](../../../projects/02-chat-qa-ops/capstone/v2-submission-polish/README.md)
4. [v2 demo runbook](../../../projects/02-chat-qa-ops/capstone/v2-submission-polish/docs/demo/demo-runbook.md)
5. [v2 Makefile](../../../projects/02-chat-qa-ops/capstone/v2-submission-polish/python/Makefile)
6. [개발 타임라인](10-development-timeline.md)

## 근거 파일

- [bot.py](../../../projects/02-chat-qa-ops/capstone/v0-initial-demo/python/backend/src/chatbot/bot.py)
- [pipeline.py](../../../projects/02-chat-qa-ops/capstone/v0-initial-demo/python/backend/src/evaluator/pipeline.py)
- [provider_chain.py](../../../projects/02-chat-qa-ops/capstone/v1-regression-hardening/python/backend/src/core/provider_chain.py)
- [test_lineage_and_trace.py](../../../projects/02-chat-qa-ops/capstone/v1-regression-hardening/python/tests/mp5/test_lineage_and_trace.py)
- [test_retrieval_v2.py](../../../projects/02-chat-qa-ops/capstone/v2-submission-polish/python/tests/mp3/test_retrieval_v2.py)
- [Overview.tsx](../../../projects/02-chat-qa-ops/capstone/v2-submission-polish/react/src/pages/Overview.tsx)
- [auth.py](../../../projects/02-chat-qa-ops/capstone/v3-self-hosted-oss/python/backend/src/api/routes/auth.py)
- [datasets.py](../../../projects/02-chat-qa-ops/capstone/v3-self-hosted-oss/python/backend/src/api/routes/datasets.py)
- [jobs.py](../../../projects/02-chat-qa-ops/capstone/v3-self-hosted-oss/python/backend/src/services/jobs.py)
