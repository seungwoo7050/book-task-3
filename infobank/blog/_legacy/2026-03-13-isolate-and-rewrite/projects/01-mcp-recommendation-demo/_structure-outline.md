# 01 MCP 추천 최적화 structure outline

## 시리즈 목표

- `v0`에서 왜 manifest contract와 explanation trace를 먼저 고정했는지 보여 준다.
- `v1~v2`에서 rerank, compare, compatibility, release gate가 어떻게 하나의 제출 증빙 흐름으로 묶였는지 보여 준다.
- `v3`에서 self-hosted operator surface가 왜 auth + job queue + audit log 조합으로 바뀌는지 보여 준다.

## 글 배치

| 글 | 범위 | 중심 질문 | 꼭 넣을 코드 앵커 | 꼭 넣을 CLI |
| --- | --- | --- | --- | --- |
| `10-catalog-contracts-and-first-ranking-loop.md` | `v0` 중심, `v1` 진입 | 추천을 시작하기 전에 어떤 contract와 explanation trace를 먼저 고정해야 했는가 | `shared/src/contracts.ts`, `recommendation-service.ts`, `rerank-service.ts` | `pnpm db:up`, `pnpm migrate`, `pnpm seed`, `pnpm eval` |
| `20-ranking-proof-and-release-gates.md` | `v1 -> v2` | candidate uplift를 어떻게 compare, compatibility, release gate, artifact export로 굳혔는가 | `compare-service.ts`, `compatibility-service.ts`, `release-gate-service.ts`, `artifact-service.ts` | `pnpm test`, `pnpm compatibility`, `pnpm release:gate`, `pnpm artifact:export` |
| `30-self-hosted-operator-surface.md` | `v3` | sync demo를 self-hosted operator product로 바꿀 때 경계가 어떻게 달라졌는가 | `app.ts`, `auth-service.ts`, `job-service.ts` | `pnpm migrate`, `pnpm bootstrap:owner`, `pnpm test` |

## 서술 원칙

- Day/Session은 버전 사다리 기준으로 끊고, 나중에 알게 된 사실을 앞세우지 않는다.
- 각 글마다 코드 스니펫 2개 이상, CLI 블록 2개 이상을 넣는다.
- compare/eval/release proof는 slide caption처럼 요약하지 않고, 어떤 함수가 어떤 기준을 강제했는지까지 연결한다.
