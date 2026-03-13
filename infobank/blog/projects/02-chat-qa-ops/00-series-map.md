# Chat QA Ops 시리즈 맵

이 시리즈는 `projects/02-chat-qa-ops`를 "챗봇이 얼마나 잘 답하는가"보다 "상담 품질을 어떻게 정의하고 증명 가능한 형태로 운영하는가"라는 질문으로 다시 읽는다. 처음에는 rule, evidence, judge를 묶은 평가 파이프라인이 등장하고, 그다음에는 golden regression과 compare proof가 붙고, 마지막에는 self-hosted review ops로 확장된다.

이번 버전은 2026-03-13에 `isolate-and-rewrite` 방식으로 다시 썼다. 예전 blog는 [`../../_legacy/2026-03-13-isolate-and-rewrite/projects/02-chat-qa-ops/`](../../_legacy/2026-03-13-isolate-and-rewrite/projects/02-chat-qa-ops/)에 옮겨 두었고, 이번 시리즈는 현재 소스와 실제 CLI 결과만 사용했다.

## 왜 독립 프로젝트로 보았는가

`projects/02-chat-qa-ops`는 하나의 완결된 문제를 스스로 설명할 수 있다. 이 프로젝트는 "상담 품질을 어떤 기준으로 평가하고, 그 평가를 어떻게 회귀 증빙과 운영 화면까지 연결할 것인가"라는 질문에 답한다. 진입점도 분명하고, 검증 명령도 따로 있으며, `v0 -> v3` 흐름도 다른 디렉터리와 섞이지 않는다.

반면 루트 redirect인 `chat-qa-ops/`는 현재 위치를 가리키는 README만 남아 있어 독립 프로젝트 기준을 충족하지 못했다.

## 이번에 사용한 근거

- 프로젝트 경계: `README.md`, `problem/README.md`
- 흐름 복원 기준: `docs/stage-catalog.md`, `docs/verification-matrix.md`
- 공식 답: `capstone/v2-submission-polish/README.md`
- proof 자료:
  - `docs/demo/demo-runbook.md`
  - `docs/demo/phase1-vs-phase2-diff-matrix.md`
  - `docs/demo/proof-artifacts/improvement-report.json`
  - `docs/demo/proof-artifacts/cli-report.txt`
  - `docs/demo/proof-artifacts/cli-compare.txt`
- 핵심 코드:
  - `python/backend/src/evaluator/pipeline.py`
  - `python/backend/src/api/routes/dashboard.py`
  - `python/backend/src/cli/main.py`
  - `v3 python/backend/src/core/auth.py`
  - `v3 python/backend/src/services/jobs.py`
  - `v3 react/src/App.tsx`
  - `v3 react/src/pages/Jobs.tsx`
- 실제 검증:
  - `UV_PYTHON=python3.12 make gate-all`
  - `UV_PYTHON=python3.12 make smoke-postgres`
  - `v3 UV_PYTHON=python3.12 make gate-all`

## 챕터 구성

1. [`10-first-qa-evaluation-loop.md`](./10-first-qa-evaluation-loop.md)  
   rule, evidence, judge, scoring이 어떤 순서로 묶였는지, 그리고 왜 CLI가 먼저 중요한 운영 출구가 되었는지 본다.
2. [`20-regression-hardening-and-proof.md`](./20-regression-hardening-and-proof.md)  
   golden compare, dashboard version compare, smoke-postgres, proof artifact가 어떻게 하나의 증빙 흐름을 만드는지 본다.
3. [`30-self-hosted-review-ops.md`](./30-self-hosted-review-ops.md)  
   이미 만든 proof surface가 `v3`에서 login, dataset import, evaluation job, selected-job review UI로 어떻게 확장되는지 본다.

## 이 시리즈를 읽을 때의 핵심 질문

이 트랙에서 중요한 건 점수 계산식 하나를 이해하는 것이 아니다. 더 중요한 질문은 `rule/evidence/judge -> regression proof -> operator review`가 어떤 순서로 서로 기대게 되었는가다.
