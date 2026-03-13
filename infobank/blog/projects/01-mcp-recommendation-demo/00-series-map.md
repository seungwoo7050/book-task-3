# MCP 추천 최적화 시리즈 맵

이 시리즈는 `projects/01-mcp-recommendation-demo`를 "추천 결과가 어떤가"가 아니라 "추천 시스템이 어떤 순서로 단단해졌는가"라는 질문으로 다시 읽는다. 처음에는 catalog와 manifest 계약을 고정하고, 그다음 추천과 rerank를 붙이고, 마지막에는 release 판단과 self-hosted 운영 표면으로 확장되는 흐름을 따라간다.

이번 버전은 2026-03-13에 `isolate-and-rewrite` 방식으로 다시 썼다. 예전 blog는 [`../../_legacy/2026-03-13-isolate-and-rewrite/projects/01-mcp-recommendation-demo/`](../../_legacy/2026-03-13-isolate-and-rewrite/projects/01-mcp-recommendation-demo/)에 옮겨 두었고, 이번 시리즈는 현재 소스와 실제 CLI 결과만 사용했다.

## 왜 독립 프로젝트로 보았는가

`projects/01-mcp-recommendation-demo`는 하나의 완결된 문제를 스스로 설명할 수 있다. 이 프로젝트는 "MCP 추천 시스템을 어떻게 설계하고, 그 결과를 어떻게 운영 승인 가능한 형태로 증명할 것인가"라는 질문에 답한다. 진입점도 분명하고, 검증 명령도 따로 있으며, `v0 -> v3` 버전 사다리도 다른 디렉터리와 섞이지 않는다.

반면 루트 redirect인 `mcp-recommendation-demo/`는 현재 위치를 가리키는 README만 남아 있어, 독립 프로젝트 기준에는 맞지 않았다.

## 이번에 사용한 근거

- 프로젝트 경계: `README.md`, `problem/README.md`
- 흐름 복원 기준: `docs/stage-catalog.md`, `docs/verification-matrix.md`
- 공식 답: `capstone/v2-submission-polish/README.md`
- 확장 답: `capstone/v3-oss-hardening/README.md`
- 핵심 코드:
  - `shared/src/catalog.ts`
  - `node/src/services/recommendation-service.ts`
  - `node/src/services/rerank-service.ts`
  - `node/src/services/release-gate-service.ts`
  - `node/src/scripts/export-artifact.ts`
  - `v3 node/src/services/job-service.ts`
  - `v3 react/components/mcp-dashboard.tsx`
- 실제 검증:
  - `pnpm seed`
  - `pnpm test`
  - `pnpm eval`
  - `pnpm compatibility rc-release-check-bot-1-5-0`
  - `pnpm release:gate rc-release-check-bot-1-5-0`
  - `pnpm artifact:export rc-release-check-bot-1-5-0`
  - `v3 pnpm test`

## 챕터 구성

1. [`10-catalog-contracts-and-first-ranking-loop.md`](./10-catalog-contracts-and-first-ranking-loop.md)  
   왜 추천 로직보다 먼저 catalog 계약을 세웠는지, 그리고 baseline과 rerank가 어디서 갈리는지 본다.
2. [`20-ranking-proof-and-release-gates.md`](./20-ranking-proof-and-release-gates.md)  
   점수 개선이 compare, compatibility, release gate, artifact export까지 이어지는 과정을 본다.
3. [`30-self-hosted-operator-surface.md`](./30-self-hosted-operator-surface.md)  
   이미 만든 proof pipeline이 `v3`에서 RBAC와 async job을 가진 운영 표면으로 어떻게 바뀌는지 본다.

## 이 시리즈를 읽을 때의 핵심 질문

이 프로젝트를 따라갈 때 중요한 건 "추천이 잘 되는가"만이 아니다. 더 중요한 질문은 `metadata 계약 -> 추천 trace -> compare와 gate -> 운영자 UI`가 어떤 순서로 서로 기대게 되었는가다.
