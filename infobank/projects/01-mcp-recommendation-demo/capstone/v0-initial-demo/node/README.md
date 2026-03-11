# v0 Node 백엔드

이 디렉터리는 `v0-initial-demo`의 Fastify + Drizzle + PostgreSQL 백엔드다. seeded catalog, manifest validation, baseline recommendation, offline eval을 API와 스크립트로 묶는다.

## 현재 범위

- manifest validation route
- catalog 조회와 baseline recommendation API
- PostgreSQL schema push와 seed script
- offline eval 실행 스크립트

## 자주 쓰는 명령

```bash
pnpm dev
pnpm build
pnpm test
pnpm db:push
pnpm seed
pnpm eval
```

기본 API 포트는 `3100`이다.

## 현재 상태

- 구현 상태: 완료
- 검증 경로: `pnpm test`, 상위 버전 README의 `pnpm eval`, `pnpm e2e`
- 연동 패키지: `@study1-v0/shared`

## 아직 없는 것

- reranker와 baseline/candidate compare
- usage logs와 feedback loop
- release gate, artifact export, auth

## 읽을 때 보면 좋은 파일

- `src/app.ts`
- `src/server.ts`
- `src/scripts/seed.ts`
- `src/scripts/eval.ts`
- `tests/manifest-validation.test.ts`
- `tests/routes.integration.test.ts`
