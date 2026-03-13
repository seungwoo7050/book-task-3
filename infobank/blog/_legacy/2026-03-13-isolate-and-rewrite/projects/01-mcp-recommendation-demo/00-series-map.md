# MCP 추천 최적화 시리즈 지도

## 이 프로젝트를 한 줄로

catalog metadata를 안정적인 계약으로 먼저 고정한 뒤, baseline recommendation을 rerank/compare/release gate/self-hosted operator surface까지 밀어 올리는 프로젝트다. 시작점은 "어떤 MCP를 추천할까"였지만, 끝에 가면 질문이 "이 추천 candidate를 어떤 근거로 release할까"로 바뀐다.

## 문제 구조

- 원 프로젝트: [`../../../projects/01-mcp-recommendation-demo/README.md`](../../../projects/01-mcp-recommendation-demo/README.md)
- 문제 정의: [`../../../projects/01-mcp-recommendation-demo/problem/README.md`](../../../projects/01-mcp-recommendation-demo/problem/README.md)
- 공식 답: [`../../../projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/README.md`](../../../projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/README.md)
- 확장 답: [`../../../projects/01-mcp-recommendation-demo/capstone/v3-oss-hardening/README.md`](../../../projects/01-mcp-recommendation-demo/capstone/v3-oss-hardening/README.md)
- canonical verify:
  - `pnpm db:up`
  - `pnpm migrate`
  - `pnpm seed`
  - `pnpm test`
  - `pnpm eval`
  - `pnpm compatibility rc-release-check-bot-1-5-0`
  - `pnpm release:gate rc-release-check-bot-1-5-0`

## 버전 사다리

| 버전 | 무엇을 처음 고정했는가 | 대표 코드/문서 | 대표 검증 신호 |
| --- | --- | --- | --- |
| `v0-initial-demo` | manifest contract, baseline selector, Korean explanation, offline eval | `shared/src/contracts.ts`, `node/src/services/recommendation-service.ts` | `pnpm seed`, `pnpm eval` |
| `v1-ranking-hardening` | usage/feedback rerank, baseline/candidate compare, operator dashboard | `node/src/services/rerank-service.ts`, `node/src/services/compare-service.ts` | `pnpm test`, compare snapshot docs |
| `v2-submission-polish` | compatibility gate, release gate, submission artifact export | `compatibility-service.ts`, `release-gate-service.ts`, `artifact-service.ts` | `compatibility passed`, `release gate passed`, artifact markdown export |
| `v3-oss-hardening` | auth, RBAC, queued jobs, worker, self-hosted packaging | `app.ts`, `auth-service.ts`, `job-service.ts`, `worker.ts` | `pnpm bootstrap:owner`, `pnpm test`, Compose quickstart |

## 이 시리즈에서 따라갈 질문

1. 추천 점수 함수보다 먼저 고정해야 했던 contract는 무엇이었는가.
2. baseline recommendation이 언제 "설명 가능한 추천"으로 바뀌었는가.
3. usage log와 feedback가 왜 analytics가 아니라 rerank signal이 되었는가.
4. compare uplift가 왜 release gate와 artifact export까지 이어져야 했는가.
5. self-hosted operator surface를 만들면서 왜 auth와 job queue가 중심이 되었는가.

## 글 목록

| 번호 | 파일 | 범위 |
| --- | --- | --- |
| `10` | [`10-catalog-contracts-and-first-ranking-loop.md`](10-catalog-contracts-and-first-ranking-loop.md) | `v0`의 contract, baseline scoring, explanation trace, `v1` rerank 질문의 시작 |
| `20` | [`20-ranking-proof-and-release-gates.md`](20-ranking-proof-and-release-gates.md) | `v1` compare에서 `v2` compatibility/release/artifact flow로 넘어가는 구간 |
| `30` | [`30-self-hosted-operator-surface.md`](30-self-hosted-operator-surface.md) | `v3`에서 auth, RBAC, queue worker, self-hosted 운영 표면을 붙이는 구간 |
