# v1 Node 백엔드

이 디렉터리는 `v1-ranking-hardening`의 Fastify + Drizzle + PostgreSQL 백엔드다. `v0`의 baseline API 위에 reranker, usage logs, feedback loop, experiment CRUD, compare snapshot을 추가한다.

## 현재 범위

- baseline/candidate recommendation API
- rerank service와 compare 계산
- usage event 저장
- feedback 저장
- experiment CRUD와 catalog 확장 API

## 자주 쓰는 명령

```bash
pnpm dev
pnpm build
pnpm test
pnpm db:push
pnpm seed
pnpm eval
```

기본 API 포트는 `3101`이다.

## 현재 상태

- 구현 상태: 완료
- 검증 경로: `pnpm test`, 상위 버전 README의 `pnpm e2e`
- 핵심 테스트: `tests/rerank-service.test.ts`, `tests/routes.integration.test.ts`

## 아직 없는 것

- compatibility gate와 release gate
- artifact export
- auth, worker, audit log

## 읽을 때 보면 좋은 파일

- `src/app.ts`
- `src/server.ts`
- `tests/rerank-service.test.ts`
- `tests/routes.integration.test.ts`
