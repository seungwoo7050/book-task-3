# 02 챗봇 상담 품질 관리 blog

이 시리즈는 `projects/02-chat-qa-ops`가 어떻게 하나의 평가 파이프라인에서 출발해, regression proof와 self-hosted review ops까지 갖춘 프로젝트로 자랐는지 따라가는 기록이다. 최종 결과를 짧게 소개하는 대신, 어떤 품질 기준을 먼저 세웠고 어떤 검증과 운영 화면이 그 뒤에 붙었는지 차례대로 복원한다.

이번 리라이트에서는 기존 blog를 입력으로 쓰지 않았다. 예전 시리즈는 [`../../_legacy/2026-03-13-isolate-and-rewrite/projects/02-chat-qa-ops/`](../../_legacy/2026-03-13-isolate-and-rewrite/projects/02-chat-qa-ops/)에 보관했고, 이번 글은 현재 코드와 CLI, proof artifact만으로 다시 썼다.

## 어떤 근거로 썼는가

- 프로젝트 경계: `projects/02-chat-qa-ops/README.md`, `problem/README.md`
- 흐름 복원 기준: `docs/stage-catalog.md`, `docs/verification-matrix.md`
- 핵심 구현: `python/backend/src/evaluator/pipeline.py`, `python/backend/src/api/routes/dashboard.py`, `python/backend/src/cli/main.py`
- proof 자료: `docs/demo/demo-runbook.md`, `docs/demo/phase1-vs-phase2-diff-matrix.md`, `docs/demo/proof-artifacts/improvement-report.json`, `docs/demo/proof-artifacts/cli-report.txt`, `docs/demo/proof-artifacts/cli-compare.txt`
- 확장 버전 핵심: `v3 python/backend/src/core/auth.py`, `v3 python/backend/src/api/routes/jobs.py`, `v3 python/backend/src/services/jobs.py`, `v3 react/src/App.tsx`, `v3 react/src/pages/Jobs.tsx`
- 실제 검증: `UV_PYTHON=python3.12 make gate-all`, `UV_PYTHON=python3.12 make smoke-postgres`, `v3 UV_PYTHON=python3.12 make gate-all`

## supporting doc

1. [`_evidence-ledger.md`](_evidence-ledger.md)
2. [`_structure-outline.md`](_structure-outline.md)

## 읽는 순서

1. [`00-series-map.md`](./00-series-map.md)에서 이 프로젝트를 어떤 질문으로 읽을지 먼저 잡는다.
2. [`10-first-qa-evaluation-loop.md`](./10-first-qa-evaluation-loop.md)에서 평가 파이프라인의 출발점을 본다.
3. [`20-regression-hardening-and-proof.md`](./20-regression-hardening-and-proof.md)에서 golden regression과 proof artifact를 본다.
4. [`30-self-hosted-review-ops.md`](./30-self-hosted-review-ops.md)에서 self-hosted review ops로 확장되는 단계를 본다.
