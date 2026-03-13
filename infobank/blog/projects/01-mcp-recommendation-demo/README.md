# 01 MCP 추천 최적화 blog

이 디렉터리는 `01-mcp-recommendation-demo`를 `source-first` 방식으로 다시 읽는 project-level blog 시리즈다. chronology는 `projects/01-mcp-recommendation-demo` 아래의 현재 capstone 버전, 서비스 코드, 테스트, runbook, 검증 명령만으로 복원했다.

## source set

- [`../../../projects/01-mcp-recommendation-demo/README.md`](../../../projects/01-mcp-recommendation-demo/README.md)
- [`../../../projects/01-mcp-recommendation-demo/capstone/README.md`](../../../projects/01-mcp-recommendation-demo/capstone/README.md)
- [`../../../projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/README.md`](../../../projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/README.md)
- [`../../../projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/README.md`](../../../projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/README.md)
- [`../../../projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/README.md`](../../../projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/README.md)
- [`../../../projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/docs/runbook.md`](../../../projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/docs/runbook.md)
- [`../../../projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/node/src/services/recommendation-service.ts`](../../../projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/node/src/services/recommendation-service.ts)
- [`../../../projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/node/src/services/release-gate-service.ts`](../../../projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/node/src/services/release-gate-service.ts)
- [`../../../projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/node/tests/routes.integration.test.ts`](../../../projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/node/tests/routes.integration.test.ts)
- [`../../../projects/01-mcp-recommendation-demo/capstone/v3-oss-hardening/node/src/services/auth-service.ts`](../../../projects/01-mcp-recommendation-demo/capstone/v3-oss-hardening/node/src/services/auth-service.ts)
- [`../../../projects/01-mcp-recommendation-demo/capstone/v3-oss-hardening/node/src/services/job-service.ts`](../../../projects/01-mcp-recommendation-demo/capstone/v3-oss-hardening/node/src/services/job-service.ts)

## 읽는 순서

1. [`00-series-map.md`](00-series-map.md)
2. [`10-development-timeline.md`](10-development-timeline.md)
3. [`../../../projects/01-mcp-recommendation-demo/README.md`](../../../projects/01-mcp-recommendation-demo/README.md)

## 검증 진입점

- `cd projects/01-mcp-recommendation-demo/capstone/v2-submission-polish`
- `pnpm db:up`
- `pnpm migrate`
- `pnpm seed`
- `pnpm test`
- `pnpm eval`
- `pnpm compatibility rc-release-check-bot-1-5-0`
- `pnpm release:gate rc-release-check-bot-1-5-0`

## chronology 메모

- 현재 git 기록은 버전 재배치와 문서 정리 커밋이 중심이라 세밀한 날짜 복원이 어렵다.
- 그래서 이 시리즈는 `Day / Session` 형식을 쓰고, 각 세션은 `v0 -> v1 -> v2 -> v3` 버전 사다리로 고정한다.
- 실제로 `pnpm test`는 prepared DB 없이 실행하면 `routes.integration.test.ts`에서 `/api/catalog`가 `500`을 반환했다. 따라서 이 프로젝트의 canonical verify는 항상 `db:up -> migrate -> seed`를 먼저 밟는 흐름으로 적는다.
