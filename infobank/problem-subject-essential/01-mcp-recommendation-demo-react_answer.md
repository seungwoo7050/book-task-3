# 01-mcp-recommendation-demo-react 답안지

이 문서는 문제지를 다시 넘기지 않고도 해답을 재구성할 수 있도록, 실제 구현 파일과 테스트만 기준으로 정리한 답안지다.

## 한 줄 해답

시작 위치의 구현을 완성해 reranker와 compare runner, usage/feedback/experiment API, 운영 콘솔의 compare 화면을 한 흐름으로 설명하고 검증한다. 핵심은 `metadata`와 `apiBaseUrl`, `apiFetch` 흐름을 구현하고 테스트를 통과시키는 것이다.

## 문제를 푸는 핵심 전략

- reranker와 compare runner
- usage/feedback/experiment API
- 운영 콘솔의 compare 화면
- 첫 진입점은 `../projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/react/app/layout.tsx`이고, 여기서 `metadata`와 `apiBaseUrl` 흐름을 먼저 붙잡은 뒤 나머지 파일로 확장한다.

## 코드 워크스루

- `../projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/react/app/layout.tsx`: 앱 레이아웃과 메타데이터 경계를 고정하는 파일이다.
- `../projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/react/app/page.tsx`: 화면 진입점에서 최상위 composition과 초기 시연 흐름을 고정하는 파일이다.
- `../projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/react/components/mcp-dashboard.tsx`: `apiBaseUrl`, `apiFetch`, `buildSampleCatalogEntry`, `MpcDashboard`가 핵심 흐름과 상태 전이를 묶는다.
- `../projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/react/next.config.ts`: `root`, `nextConfig`가 핵심 흐름과 상태 전이를 묶는다.
- `../projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/react/vitest.setup.ts`: 핵심 구현을 담는 파일이다.
- `../projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/react/components/mcp-dashboard.test.tsx`: `fetchMock`, `MpcDashboard v1`, `renders compare workflow and candidate recommendation`가 통과 조건과 회귀 포인트를 잠근다.
- `../projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/react/tsconfig.json`: 입력 fixture나 계약 데이터를 고정하는 근거 파일이다.
- `../projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/react/package.json`: 실행 명령과 검증 경로를 고정하는 설정 파일이다.

## 정답을 재구성하는 절차

1. `../projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/react/app/layout.tsx`를 먼저 열어 입력과 상태 전이의 기준점을 잡는다.
2. `fetchMock` 등이 요구하는 순서대로 핵심 상태 전이와 예외 흐름을 채운다.
3. `pnpm install && cp .env.example .env && pnpm db:up && pnpm migrate && pnpm seed && pnpm dev && pnpm test && pnpm eval && pnpm capture:presentation && pnpm e2e`를 실행해 결과를 잠그고, 필요하면 남은 검증 명령까지 이어서 돌린다.

## 검증과 실패 포인트

```bash
pnpm install && cp .env.example .env && pnpm db:up && pnpm migrate && pnpm seed && pnpm dev && pnpm test && pnpm eval && pnpm capture:presentation && pnpm e2e
```

```bash
cd /Users/woopinbell/work/book-task-3/infobank/projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/react && npm run test
```

- 상위 카탈로그나 보조 문서만 보고 구현을 추측하지 않고, 지금 열어 둔 source/test를 정답 근거로 고정한다.
- `fetchMock`와 `MpcDashboard v1`가 잠근 상태 전이와 입력 계약을 빼먹지 않는다.
- 완성 직전에만 한 번 돌리지 말고, 상태 전이를 건드릴 때마다 `pnpm install && cp .env.example .env && pnpm db:up && pnpm migrate && pnpm seed && pnpm dev && pnpm test && pnpm eval && pnpm capture:presentation && pnpm e2e`로 회귀를 조기에 잡는다.

## 소스 근거

- `../projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/react/app/layout.tsx`
- `../projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/react/app/page.tsx`
- `../projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/react/components/mcp-dashboard.tsx`
- `../projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/react/next.config.ts`
- `../projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/react/vitest.setup.ts`
- `../projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/react/components/mcp-dashboard.test.tsx`
- `../projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/react/tsconfig.json`
- `../projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/react/package.json`
- `../projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/react/vitest.config.ts`
