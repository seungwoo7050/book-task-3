# 01 MCP 추천 최적화 blog

이 시리즈는 `projects/01-mcp-recommendation-demo`가 어떻게 하나의 추천 데모에서 출발해, release gate와 self-hosted 운영 표면까지 갖춘 프로젝트로 자랐는지 따라가는 기록이다. 최종 결과만 요약하는 대신, 어떤 계약을 먼저 고정했고 어떤 검증을 통과시키며 다음 단계로 넘어갔는지 차례대로 복원한다.

이번 리라이트에서는 기존 blog를 입력으로 쓰지 않았다. 예전 시리즈는 [`../../_legacy/2026-03-13-isolate-and-rewrite/projects/01-mcp-recommendation-demo/`](../../_legacy/2026-03-13-isolate-and-rewrite/projects/01-mcp-recommendation-demo/)에 보관했고, 이번 글은 현재 코드와 CLI만으로 다시 썼다.

## 어떤 근거로 썼는가

- 프로젝트 경계: `projects/01-mcp-recommendation-demo/README.md`, `problem/README.md`
- 흐름 복원 기준: `docs/stage-catalog.md`, `docs/verification-matrix.md`
- 핵심 구현: `shared/src/catalog.ts`, `shared/src/eval.ts`, `node/src/services/recommendation-service.ts`, `node/src/services/rerank-service.ts`, `node/src/services/release-gate-service.ts`, `node/src/scripts/export-artifact.ts`
- 확장 버전 핵심: `capstone/v3-oss-hardening/node/src/services/job-service.ts`, `capstone/v3-oss-hardening/react/components/mcp-dashboard.tsx`
- 실제 검증: `pnpm seed`, `pnpm test`, `pnpm eval`, `pnpm compatibility`, `pnpm release:gate`, `pnpm artifact:export`, `v3 pnpm test`

## supporting doc

1. [`_evidence-ledger.md`](_evidence-ledger.md)
2. [`_structure-outline.md`](_structure-outline.md)

## 읽는 순서

1. [`00-series-map.md`](./00-series-map.md)에서 이 프로젝트를 어떤 질문으로 읽을지 먼저 잡는다.
2. [`10-catalog-contracts-and-first-ranking-loop.md`](./10-catalog-contracts-and-first-ranking-loop.md)에서 추천 시스템의 출발점을 본다.
3. [`20-ranking-proof-and-release-gates.md`](./20-ranking-proof-and-release-gates.md)에서 compare와 release gate가 붙는 과정을 본다.
4. [`30-self-hosted-operator-surface.md`](./30-self-hosted-operator-surface.md)에서 운영자용 UI와 job 흐름으로 확장되는 단계를 본다.
