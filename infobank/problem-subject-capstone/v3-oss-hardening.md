# v3-oss-hardening 문제지

## 왜 중요한가

v3-oss-hardening은 v2-submission-polish를 self-hosted OSS 후보로 끌어올린 제품화 확장 버전이다. 목표는 새 추천 기능을 더 넣는 것이 아니라, 한 팀이 직접 설치해서 로그인된 권한 아래 catalog, experiment, release candidate, release gate를 운영할 수 있게 만드는 것이다.

## 목표

anonymous request가 protected route에서 401을 반환한다. viewer mutation이 403을 반환한다. owner는 user/settings를 관리할 수 있다. operator는 catalog/experiment/release candidate CRUD와 job 실행이 가능하다.

## 시작 위치

- `../projects/01-mcp-recommendation-demo/capstone/v3-oss-hardening/node/src/app.ts`
- `../projects/01-mcp-recommendation-demo/capstone/v3-oss-hardening/node/src/config.ts`
- `../projects/01-mcp-recommendation-demo/capstone/v3-oss-hardening/node/src/db/client.ts`
- `../projects/01-mcp-recommendation-demo/capstone/v3-oss-hardening/node/src/db/schema.ts`
- `../projects/01-mcp-recommendation-demo/capstone/v3-oss-hardening/react/components/mcp-dashboard.test.tsx`
- `../projects/01-mcp-recommendation-demo/capstone/v3-oss-hardening/node/tests/compatibility-service.test.ts`
- `../projects/01-mcp-recommendation-demo/capstone/v3-oss-hardening/.env.example`
- `../projects/01-mcp-recommendation-demo/capstone/v3-oss-hardening/docker-compose.yml`

## starter code / 입력 계약

- `../projects/01-mcp-recommendation-demo/capstone/v3-oss-hardening/node/src/app.ts`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- anonymous request가 protected route에서 401을 반환한다.
- viewer mutation이 403을 반환한다.
- owner는 user/settings를 관리할 수 있다.
- operator는 catalog/experiment/release candidate CRUD와 job 실행이 가능하다.
- eval, compare, compatibility, release gate, artifact export가 job으로 완료된다.
- docker compose up -d --build로 postgres + api + worker + web가 함께 기동된다.
- pnpm bootstrap:owner가 idempotent하게 동작한다.

## 제외 범위

- `../projects/01-mcp-recommendation-demo/capstone/v3-oss-hardening/.env.example` 등 fixture나 trace를 읽지 않고 동작을 추측해서 구현하지 않는다.
- 상위 카탈로그 요약만 보고 세부 산출물 계약을 생략하지 않는다.

## 성공 체크리스트

- 핵심 흐름은 `sessionCookieOptions`와 `ensureSettings`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `fetchMock`와 `now`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../projects/01-mcp-recommendation-demo/capstone/v3-oss-hardening/.env.example` 등 fixture/trace 기준으로 결과를 대조했다.
- `pnpm install && cp .env.example .env && pnpm db:up && pnpm migrate && pnpm seed && pnpm bootstrap:owner && pnpm build && pnpm test && pnpm test:integration && pnpm e2e && pnpm eval && pnpm compare && pnpm compatibility rc-release-check-bot-1-5-0 && pnpm release:gate rc-release-check-bot-1-5-0 && pnpm artifact:export rc-release-check-bot-1-5-0 && pnpm capture:presentation`가 통과한다.

## 검증 방법

```bash
pnpm install && cp .env.example .env && pnpm db:up && pnpm migrate && pnpm seed && pnpm bootstrap:owner && pnpm build && pnpm test && pnpm test:integration && pnpm e2e && pnpm eval && pnpm compare && pnpm compatibility rc-release-check-bot-1-5-0 && pnpm release:gate rc-release-check-bot-1-5-0 && pnpm artifact:export rc-release-check-bot-1-5-0 && pnpm capture:presentation
```

```bash
cd /Users/woopinbell/work/book-task-3/infobank/projects/01-mcp-recommendation-demo/capstone/v3-oss-hardening/node && npm test -- tests/compatibility-service.test.ts tests/manifest-validation.test.ts tests/recommendation-service.test.ts tests/release-gate-service.test.ts tests/rerank-service.test.ts
```

```bash
cd /Users/woopinbell/work/book-task-3/infobank/projects/01-mcp-recommendation-demo/capstone/v3-oss-hardening && npm run test
```

- Node 계열 lab는 의존성 설치(`npm install` 등)가 끝난 뒤 검증 명령을 실행한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`v3-oss-hardening_answer.md`](v3-oss-hardening_answer.md)에서 확인한다.
