# 01 MCP 추천 최적화 blog

이 디렉터리는 `01-mcp-recommendation-demo`를 project-level source-first 시리즈로 다시 읽는 입구다. chronology는 `v0-initial-demo -> v1-ranking-hardening -> v2-submission-polish -> v3-oss-hardening` 사다리와 실제 재검증 명령을 함께 사용해 복원했다.

## source set

- [`../../../projects/01-mcp-recommendation-demo/README.md`](../../../projects/01-mcp-recommendation-demo/README.md)
- [`../../../projects/01-mcp-recommendation-demo/problem/README.md`](../../../projects/01-mcp-recommendation-demo/problem/README.md)
- [`../../../projects/01-mcp-recommendation-demo/docs/stage-catalog.md`](../../../projects/01-mcp-recommendation-demo/docs/stage-catalog.md)
- [`../../../projects/01-mcp-recommendation-demo/docs/verification-matrix.md`](../../../projects/01-mcp-recommendation-demo/docs/verification-matrix.md)
- [`../../../projects/01-mcp-recommendation-demo/capstone/README.md`](../../../projects/01-mcp-recommendation-demo/capstone/README.md)
- [`../../../projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/shared/src/contracts.ts`](../../../projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/shared/src/contracts.ts)
- [`../../../projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/node/src/services/recommendation-service.ts`](../../../projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/node/src/services/recommendation-service.ts)
- [`../../../projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/node/src/services/rerank-service.ts`](../../../projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/node/src/services/rerank-service.ts)
- [`../../../projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/node/src/services/compare-service.ts`](../../../projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/node/src/services/compare-service.ts)
- [`../../../projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/node/src/services/compatibility-service.ts`](../../../projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/node/src/services/compatibility-service.ts)
- [`../../../projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/node/src/services/release-gate-service.ts`](../../../projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/node/src/services/release-gate-service.ts)
- [`../../../projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/node/src/services/artifact-service.ts`](../../../projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/node/src/services/artifact-service.ts)
- [`../../../projects/01-mcp-recommendation-demo/capstone/v3-oss-hardening/node/src/app.ts`](../../../projects/01-mcp-recommendation-demo/capstone/v3-oss-hardening/node/src/app.ts)
- [`../../../projects/01-mcp-recommendation-demo/capstone/v3-oss-hardening/node/src/services/auth-service.ts`](../../../projects/01-mcp-recommendation-demo/capstone/v3-oss-hardening/node/src/services/auth-service.ts)
- [`../../../projects/01-mcp-recommendation-demo/capstone/v3-oss-hardening/node/src/services/job-service.ts`](../../../projects/01-mcp-recommendation-demo/capstone/v3-oss-hardening/node/src/services/job-service.ts)
- [`../../../projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/node/tests`](../../../projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/node/tests)
- [`../../../projects/01-mcp-recommendation-demo/capstone/v3-oss-hardening/react/components/mcp-dashboard.test.tsx`](../../../projects/01-mcp-recommendation-demo/capstone/v3-oss-hardening/react/components/mcp-dashboard.test.tsx)

## 읽는 순서

1. [`00-series-map.md`](00-series-map.md)
2. [`10-catalog-contracts-and-first-ranking-loop.md`](10-catalog-contracts-and-first-ranking-loop.md)
3. [`20-ranking-proof-and-release-gates.md`](20-ranking-proof-and-release-gates.md)
4. [`30-self-hosted-operator-surface.md`](30-self-hosted-operator-surface.md)
5. [`../../../projects/01-mcp-recommendation-demo/README.md`](../../../projects/01-mcp-recommendation-demo/README.md)

Supporting doc:

- [`_evidence-ledger.md`](_evidence-ledger.md)
- [`_structure-outline.md`](_structure-outline.md)

## 검증 진입점

- 공식 제출 답: `cd ../../../projects/01-mcp-recommendation-demo/capstone/v2-submission-polish && pnpm db:up && pnpm migrate && pnpm seed && pnpm test && pnpm eval && pnpm compatibility rc-release-check-bot-1-5-0 && pnpm release:gate rc-release-check-bot-1-5-0`
- 확장 답: `cd ../../../projects/01-mcp-recommendation-demo/capstone/v3-oss-hardening && pnpm install --no-frozen-lockfile && pnpm db:up && pnpm migrate && pnpm bootstrap:owner && pnpm test`

## chronology 메모

- project-level git history는 migration commit 하나뿐이라, 실제 chronology는 버전 README와 파일 diff를 기준으로 다시 세웠다.
- 기존 blog는 [`../../_legacy/projects/01-mcp-recommendation-demo`](../../_legacy/projects/01-mcp-recommendation-demo)로 격리했고 입력 근거로 사용하지 않았다.
- 현재 revalidation에서 `v2` 공식 답과 `v3` 확장 답의 핵심 명령을 다시 실행해 CLI 신호를 확보했다.
