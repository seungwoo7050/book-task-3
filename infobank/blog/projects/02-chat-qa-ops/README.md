# 02 챗봇 상담 품질 관리 blog

이 시리즈는 `projects/02-chat-qa-ops`를 "챗봇이 얼마나 잘 답했는가"보다 "상담 품질 평가를 어떤 trace와 증빙으로 운영 가능한 형태까지 밀어 올렸는가"라는 질문으로 다시 읽는다. 공식 답은 `capstone/v2-submission-polish`이고, `v3-self-hosted-oss`는 그 평가 체계를 single-team self-hosted review ops로 옮긴 확장 답이다. 그래서 이 프로젝트의 중심은 answer generation보다 `Rule -> Evidence -> Judge -> Regression Proof -> Review Ops` 순서에 있다.

이번 재작성은 기존 blog를 입력으로 쓰지 않고 다음 근거만 사용했다.

- 문제와 공식 범위: `projects/02-chat-qa-ops/README.md`, `problem/README.md`
- 단계 지도: `docs/stage-catalog.md`, `docs/verification-matrix.md`
- 공식 답 문서: `capstone/v2-submission-polish/README.md`
- proof 자료: `docs/demo/demo-runbook.md`, `docs/demo/proof-artifacts/improvement-report.json`, `docs/demo/proof-artifacts/cli-compare.txt`
- 핵심 코드: `python/backend/src/evaluator/pipeline.py`, `python/backend/src/api/routes/dashboard.py`, `python/backend/src/cli/main.py`
- 확장 코드: `capstone/v3-self-hosted-oss/python/backend/src/core/auth.py`, `capstone/v3-self-hosted-oss/python/backend/src/services/jobs.py`, `capstone/v3-self-hosted-oss/react/src/App.tsx`, `capstone/v3-self-hosted-oss/react/src/pages/Jobs.tsx`
- 실제 검증: 2026-03-14에 재실행한 `make gate-all`, `make smoke-postgres`, `v3 make gate-all`, 그리고 `cli.main compare` 재실행

## supporting doc

1. [`_evidence-ledger.md`](_evidence-ledger.md)
2. [`_structure-outline.md`](_structure-outline.md)

## 읽는 순서

1. [`00-series-map.md`](./00-series-map.md)
2. [`10-first-qa-evaluation-loop.md`](./10-first-qa-evaluation-loop.md)
3. [`20-regression-hardening-and-proof.md`](./20-regression-hardening-and-proof.md)
4. [`30-self-hosted-review-ops.md`](./30-self-hosted-review-ops.md)

## 이번에 다시 확인한 현재 상태

- `v2 make gate-all`: lint 통과, mypy `42 source files`, MP1~MP5 `3/5/15/5/16 passed`, frontend `5 passed`
- `v2 make smoke-postgres`: 통과
- `v2 make compare`: 현재 Makefile은 `--baseline/--candidate` 옵션을 넘겨 CLI 시그니처와 맞지 않아 실패
- `v2 cli compare v1.0 v1.1`: 현재 snapshot에서 다시 만든 canonical local run은 `87.76 -> 87.76`, delta `0.0`
- `docs/demo/proof-artifacts`: historical proof는 archived improvement record로 `84.06 -> 87.76`, `critical 2 -> 0`를 남긴다
- `v3 make gate-all`: mypy `51 source files`, MP1~MP5 `2/4/2/1/1 passed`, frontend `6 passed`

## 지금 남기는 한계

- `v2` 문서에 남은 improvement artifact는 archived proof이고, 현재 snapshot rerun은 lineage/compare surface가 아직 살아 있는지를 보는 non-regression check에 더 가깝다.
- `make compare`는 현재 CLI 시그니처와 불일치하므로, 지금 기준 canonical compare는 direct CLI positional 호출이다.
- `v3` gate는 통과하지만 frontend 테스트 중 React Router future flag warning과 `pnpm approve-builds` 관련 경고가 출력된다.
