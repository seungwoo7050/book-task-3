# 01 MCP 추천 최적화 시리즈 지도

이 시리즈는 `MCP 추천 시스템`을 단순 검색 데모가 아니라, `catalog contract -> rerank/compare -> release gate -> self-hosted 운영 흐름`으로 읽어야 한다는 점을 실제 소스 기준으로 다시 고정한다.

## 이 시리즈가 보는 문제

- catalog와 manifest를 어떤 계약으로 고정해야 추천 결과를 검증 가능한 제품 설명으로 바꿀 수 있는가
- baseline recommendation을 어떤 신호까지 포함해야 `candidate` 개선과 `compare`가 의미를 갖는가
- compatibility gate, release gate, artifact export를 어디까지 묶어야 제출 가능한 답이 되는가
- `v3`에서 auth, job worker, audit log, Compose packaging을 더하면 어디서부터 productization으로 넘어가는가

## 실제 구현 표면

- `shared/src/contracts.ts`, `shared/src/catalog.ts`, `shared/src/eval.ts`가 manifest와 eval fixture 계약을 고정한다.
- `node/src/services/recommendation-service.ts`, `rerank-service.ts`, `compare-service.ts`, `compatibility-service.ts`, `release-gate-service.ts`, `artifact-service.ts`가 추천에서 제출 증빙까지의 핵심 로직을 이룬다.
- `node/tests/routes.integration.test.ts`는 catalog, recommendation, eval, compare, compatibility, release gate, artifact export가 한 DB 준비 경로에서 연결되는지 확인한다.
- `react/components/mcp-dashboard.tsx`와 각 버전의 presentation assets는 추천 UI와 compare/release surface를 보여 준다.
- `v3-oss-hardening`의 `auth-service.ts`, `job-service.ts`, `audit-service.ts`, `worker.ts`는 로그인, background job, audit trail, worker 분리를 추가한다.

## 대표 검증 엔트리

- `pnpm db:up`
- `pnpm migrate`
- `pnpm seed`
- `pnpm test`
- `pnpm eval`
- `pnpm compatibility rc-release-check-bot-1-5-0`
- `pnpm release:gate rc-release-check-bot-1-5-0`
- `pnpm artifact:export rc-release-check-bot-1-5-0`

## 읽는 순서

1. [원 프로젝트 README](../../../projects/01-mcp-recommendation-demo/README.md)
2. [capstone 개요](../../../projects/01-mcp-recommendation-demo/capstone/README.md)
3. [v2 제출 버전 README](../../../projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/README.md)
4. [runbook](../../../projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/docs/runbook.md)
5. [route integration test](../../../projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/node/tests/routes.integration.test.ts)
6. [개발 타임라인](10-development-timeline.md)

## 근거 파일

- [recommendation-service.ts](../../../projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/node/src/services/recommendation-service.ts)
- [manifest-validation.test.ts](../../../projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/node/tests/manifest-validation.test.ts)
- [rerank-service.ts](../../../projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/node/src/services/rerank-service.ts)
- [compare-service.ts](../../../projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/node/src/services/compare-service.ts)
- [release-gate-service.ts](../../../projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/node/src/services/release-gate-service.ts)
- [routes.integration.test.ts](../../../projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/node/tests/routes.integration.test.ts)
- [auth-service.ts](../../../projects/01-mcp-recommendation-demo/capstone/v3-oss-hardening/node/src/services/auth-service.ts)
- [job-service.ts](../../../projects/01-mcp-recommendation-demo/capstone/v3-oss-hardening/node/src/services/job-service.ts)
