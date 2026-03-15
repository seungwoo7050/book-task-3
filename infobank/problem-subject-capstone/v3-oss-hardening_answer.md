# v3-oss-hardening 답안지

이 문서는 문제지를 다시 넘기지 않고도 해답을 재구성할 수 있도록, 실제 구현 파일과 테스트만 기준으로 정리한 답안지다.

## 한 줄 해답

anonymous request가 protected route에서 401을 반환한다. viewer mutation이 403을 반환한다. owner는 user/settings를 관리할 수 있다. operator는 catalog/experiment/release candidate CRUD와 job 실행이 가능하다. 핵심은 `sessionCookieOptions`와 `ensureSettings`, `buildApp` 흐름을 구현하고 테스트를 통과시키는 것이다.

## 문제를 푸는 핵심 전략

- anonymous request가 protected route에서 401을 반환한다.
- viewer mutation이 403을 반환한다.
- owner는 user/settings를 관리할 수 있다.
- 첫 진입점은 `../projects/01-mcp-recommendation-demo/capstone/v3-oss-hardening/node/src/app.ts`이고, 여기서 `sessionCookieOptions`와 `ensureSettings` 흐름을 먼저 붙잡은 뒤 나머지 파일로 확장한다.

## 코드 워크스루

- `../projects/01-mcp-recommendation-demo/capstone/v3-oss-hardening/node/src/app.ts`: `sessionCookieOptions`, `ensureSettings`, `buildApp`가 핵심 흐름과 상태 전이를 묶는다.
- `../projects/01-mcp-recommendation-demo/capstone/v3-oss-hardening/node/src/config.ts`: `config`가 핵심 흐름과 상태 전이를 묶는다.
- `../projects/01-mcp-recommendation-demo/capstone/v3-oss-hardening/node/src/db/client.ts`: `pool`, `db`가 핵심 흐름과 상태 전이를 묶는다.
- `../projects/01-mcp-recommendation-demo/capstone/v3-oss-hardening/node/src/db/schema.ts`: `catalogEntries`, `evalCases`, `recommendationRuns`, `evalRuns`가 핵심 흐름과 상태 전이를 묶는다.
- `../projects/01-mcp-recommendation-demo/capstone/v3-oss-hardening/node/src/repositories/catalog-repository.ts`: `toPublicUser`, `listCatalogEntries`, `getCatalogEntryById`, `createCatalogEntry`가 핵심 흐름과 상태 전이를 묶는다.
- `../projects/01-mcp-recommendation-demo/capstone/v3-oss-hardening/react/components/mcp-dashboard.test.tsx`: `fetchMock`, `now`, `ownerSession`가 통과 조건과 회귀 포인트를 잠근다.
- `../projects/01-mcp-recommendation-demo/capstone/v3-oss-hardening/node/tests/compatibility-service.test.ts`: `releaseCheckBot`, `runCompatibilityGate`, `passes for the seeded release candidate shape`가 통과 조건과 회귀 포인트를 잠근다.
- `../projects/01-mcp-recommendation-demo/capstone/v3-oss-hardening/node/tests/manifest-validation.test.ts`: `manifest validation`, `rejects incomplete manifests`가 통과 조건과 회귀 포인트를 잠근다.

## 정답을 재구성하는 절차

1. `../projects/01-mcp-recommendation-demo/capstone/v3-oss-hardening/node/src/app.ts`를 먼저 열어 입력과 상태 전이의 기준점을 잡는다.
2. `fetchMock` 등이 요구하는 순서대로 핵심 상태 전이와 예외 흐름을 채운다.
3. `pnpm install && cp .env.example .env && pnpm db:up && pnpm migrate && pnpm seed && pnpm bootstrap:owner && pnpm build && pnpm test && pnpm test:integration && pnpm e2e && pnpm eval && pnpm compare && pnpm compatibility rc-release-check-bot-1-5-0 && pnpm release:gate rc-release-check-bot-1-5-0 && pnpm artifact:export rc-release-check-bot-1-5-0 && pnpm capture:presentation`를 실행해 결과를 잠그고, 필요하면 남은 검증 명령까지 이어서 돌린다.

## 검증과 실패 포인트

```bash
pnpm install && cp .env.example .env && pnpm db:up && pnpm migrate && pnpm seed && pnpm bootstrap:owner && pnpm build && pnpm test && pnpm test:integration && pnpm e2e && pnpm eval && pnpm compare && pnpm compatibility rc-release-check-bot-1-5-0 && pnpm release:gate rc-release-check-bot-1-5-0 && pnpm artifact:export rc-release-check-bot-1-5-0 && pnpm capture:presentation
```

```bash
cd /Users/woopinbell/work/book-task-3/infobank/projects/01-mcp-recommendation-demo/capstone/v3-oss-hardening/node && npm test -- tests/compatibility-service.test.ts tests/manifest-validation.test.ts tests/recommendation-service.test.ts tests/release-gate-service.test.ts tests/rerank-service.test.ts
```

```bash
cd /Users/woopinbell/work/book-task-3/infobank/projects/01-mcp-recommendation-demo/capstone/v3-oss-hardening && npm run test
```

- 상위 카탈로그나 보조 문서만 보고 구현을 추측하지 않고, 지금 열어 둔 source/test를 정답 근거로 고정한다.
- `fetchMock`와 `now`가 잠근 상태 전이와 입력 계약을 빼먹지 않는다.
- 완성 직전에만 한 번 돌리지 말고, 상태 전이를 건드릴 때마다 `pnpm install && cp .env.example .env && pnpm db:up && pnpm migrate && pnpm seed && pnpm bootstrap:owner && pnpm build && pnpm test && pnpm test:integration && pnpm e2e && pnpm eval && pnpm compare && pnpm compatibility rc-release-check-bot-1-5-0 && pnpm release:gate rc-release-check-bot-1-5-0 && pnpm artifact:export rc-release-check-bot-1-5-0 && pnpm capture:presentation`로 회귀를 조기에 잡는다.

## 소스 근거

- `../projects/01-mcp-recommendation-demo/capstone/v3-oss-hardening/node/src/app.ts`
- `../projects/01-mcp-recommendation-demo/capstone/v3-oss-hardening/node/src/config.ts`
- `../projects/01-mcp-recommendation-demo/capstone/v3-oss-hardening/node/src/db/client.ts`
- `../projects/01-mcp-recommendation-demo/capstone/v3-oss-hardening/node/src/db/schema.ts`
- `../projects/01-mcp-recommendation-demo/capstone/v3-oss-hardening/node/src/repositories/catalog-repository.ts`
- `../projects/01-mcp-recommendation-demo/capstone/v3-oss-hardening/react/components/mcp-dashboard.test.tsx`
- `../projects/01-mcp-recommendation-demo/capstone/v3-oss-hardening/node/tests/compatibility-service.test.ts`
- `../projects/01-mcp-recommendation-demo/capstone/v3-oss-hardening/node/tests/manifest-validation.test.ts`
- `../projects/01-mcp-recommendation-demo/capstone/v3-oss-hardening/.env.example`
- `../projects/01-mcp-recommendation-demo/capstone/v3-oss-hardening/docker-compose.yml`
