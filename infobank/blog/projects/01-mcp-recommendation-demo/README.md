# 01 MCP 추천 최적화 blog

이 시리즈는 `projects/01-mcp-recommendation-demo`를 "추천 결과가 괜찮은가"보다 "추천 계약이 어떻게 release proof와 operator surface까지 버텼는가"라는 질문으로 다시 읽는다. 실제 공식 답은 `capstone/v2-submission-polish`이고, `v3-oss-hardening`은 그 proof pipeline을 self-hosted 운영 표면으로 옮긴 확장 답이다. 그래서 이 프로젝트를 제대로 읽으려면 ranking 자체보다 `metadata schema -> explanation trace -> deterministic gate -> async operator job` 순서가 더 중요하다.

이번 재작성은 기존 blog를 입력으로 쓰지 않고 아래 근거만 사용했다.

- 문제와 공식 범위: `projects/01-mcp-recommendation-demo/README.md`, `problem/README.md`
- 단계 복원 기준: `docs/stage-catalog.md`, `docs/verification-matrix.md`
- 공식 답 핵심: `capstone/v2-submission-polish/README.md`
- 핵심 코드: `shared/src/catalog.ts`, `node/src/services/recommendation-service.ts`, `node/src/services/rerank-service.ts`, `node/src/services/release-gate-service.ts`, `node/src/services/compare-service.ts`, `node/src/scripts/export-artifact.ts`
- 확장 답 핵심: `capstone/v3-oss-hardening/node/src/services/job-service.ts`, `capstone/v3-oss-hardening/react/components/mcp-dashboard.tsx`
- 실제 검증: 2026-03-14에 재실행한 `pnpm db:up`, `pnpm migrate`, `pnpm seed`, `pnpm test`, `pnpm eval`, `pnpm compatibility rc-release-check-bot-1-5-0`, `pnpm release:gate rc-release-check-bot-1-5-0`, `pnpm artifact:export rc-release-check-bot-1-5-0`, `v3 pnpm test`

## supporting doc

1. [`_evidence-ledger.md`](_evidence-ledger.md)
2. [`_structure-outline.md`](_structure-outline.md)

## 읽는 순서

1. [`00-series-map.md`](./00-series-map.md)
2. [`10-catalog-contracts-and-first-ranking-loop.md`](./10-catalog-contracts-and-first-ranking-loop.md)
3. [`20-ranking-proof-and-release-gates.md`](./20-ranking-proof-and-release-gates.md)
4. [`30-self-hosted-operator-surface.md`](./30-self-hosted-operator-surface.md)

## 이번에 다시 확인한 현재 상태

- `pnpm migrate`: `No changes detected`
- `pnpm seed`: catalog 12개, eval case 12개, usage signal, feedback, experiment, release candidate 재적재
- `pnpm test`: v2 node 9 passed, react 1 passed
- `pnpm eval`: `top3Recall 0.9583333333333334`, `explanationCompleteness 1`, `forbiddenHitRate 0`
- `pnpm compatibility rc-release-check-bot-1-5-0`: 5개 check 모두 pass
- `pnpm release:gate rc-release-check-bot-1-5-0`: `baselineNdcg3 == candidateNdcg3 == 0.9758684958518087`인데도 `uplift 0.11464081369730995`로 pass
- `pnpm artifact:export rc-release-check-bot-1-5-0`: submission markdown 출력
- `v3 pnpm test`: node 8 passed | 2 skipped, react 2 passed, owner job flow는 살아 있지만 route integration 2개는 아직 skip

## 지금 남기는 한계

- 공식 답 `v2`는 submission proof 중심이라 long-running production SaaS를 목표로 하지 않는다.
- release gate는 "랭킹이 더 좋아졌는가"보다 "랭킹이 뒤로 가지 않았고, score uplift까지 포함한 candidate signal이 충분한가"를 본다. 그래서 현재 rerun처럼 nDCG가 동률이어도 gate는 통과할 수 있다.
- `v3`는 운영 표면을 보여 주지만, 지금 살아 있는 증거는 owner/operator job flow와 dashboard 중심이고 node route integration 2개는 아직 skipped다.
