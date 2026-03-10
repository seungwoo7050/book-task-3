# v2 Node 백엔드

이 디렉터리는 `v2-submission-polish`의 Fastify + Drizzle + PostgreSQL 백엔드다. `v1`의 recommendation/compare 흐름 위에 compatibility check, release gate, artifact export를 추가해 제출용 proof를 만든다.

## 현재 범위

- recommendation, rerank, compare API
- release candidate CRUD
- compatibility 검사 스크립트
- release gate 실행 스크립트
- submission artifact export 스크립트

## 자주 쓰는 명령

```bash
pnpm dev
pnpm build
pnpm test
pnpm db:push
pnpm seed
pnpm eval
pnpm compatibility
pnpm release:gate
pnpm artifact:export
```

기본 API 포트는 `3102`이다.

## 현재 상태

- 구현 상태: 완료
- 검증 경로: `pnpm test`, 상위 버전 README의 `pnpm compatibility`, `pnpm release:gate`, `pnpm artifact:export`
- 핵심 테스트: `tests/compatibility-service.test.ts`, `tests/release-gate-service.test.ts`

## 아직 없는 것

- 로그인과 권한 기반 운영
- background job worker
- audit log와 설치형 운영 기능

## 읽을 때 보면 좋은 파일

- `src/app.ts`
- `src/server.ts`
- `tests/compatibility-service.test.ts`
- `tests/release-gate-service.test.ts`
- `tests/routes.integration.test.ts`
