# v3 Node 백엔드와 워커

이 디렉터리는 `v3-oss-hardening`의 Fastify API와 worker를 담는다. `v2`의 recommendation, compare, gate, artifact export에 auth/session, role 구분, background jobs, audit log를 더해 self-hosted 운영 코어를 만든다.

## 현재 범위

- 로그인 세션과 role-aware API
- recommendation, compare, compatibility, release gate, artifact export
- owner bootstrap 스크립트
- pg-boss 기반 background job worker
- audit log와 운영 이벤트 추적

## 자주 쓰는 명령

```bash
pnpm dev
pnpm worker
pnpm build
pnpm test
pnpm test:integration
pnpm db:push
pnpm seed
pnpm bootstrap:owner
pnpm eval
pnpm compare
pnpm compatibility
pnpm release:gate
pnpm artifact:export
```

기본 API 포트는 `3103`이다.

## 현재 상태

- 구현 상태: 완료
- 검증 경로: `pnpm test`, `pnpm test:integration`, 상위 버전 README의 `pnpm compare`, `pnpm e2e`
- 실행 모드: API와 worker를 분리해 운영할 수 있다.

## 범위 밖

- multi-workspace SaaS
- 외부 registry 실시간 sync
- SSO/OAuth

## 읽을 때 보면 좋은 파일

- `src/server.ts`
- `src/worker.ts`
- `src/app.ts`
- `tests/routes.integration.test.ts`
- `tests/release-gate-service.test.ts`
