# NestJS Implementation

## 문제 범위

학습용 capstone을 recruiter가 바로 읽을 수 있는 Postgres + Redis 기반 서비스 패키지로 강화한다.

## 실행

- install: `pnpm install`
- build: `pnpm run build`
- migrate: `pnpm run db:migrate`
- seed: `pnpm run db:seed`
- start: `pnpm run start`
- test: `pnpm run test`
- test-e2e: `env $(cat .env.example | xargs) pnpm run test:e2e`

## 현재 상태

- 상태: `verified`
- 기준 프로젝트: `study/Node-Backend-Architecture/09-platform-capstone`
- 새 경로 검증: `pnpm run build && pnpm run test && pnpm run test:e2e`

## 환경 제약

- 지원 환경: macOS, Ubuntu
- 런타임: Node.js 22+
- 패키지 매니저: pnpm 9+
- e2e와 readiness 검증에는 Postgres, Redis가 필요하다.
- 로컬 표준 실행 경로는 [docker-compose.yml](../docker-compose.yml) 기준이다.

## 실패 시 복구 루트

- `pnpm run db:migrate`가 실패하면 `.env`의 `DATABASE_URL`과 컨테이너 상태를 먼저 확인한다.
- `pnpm run test:e2e`가 실패하면 `docker compose up -d postgres redis` 이후 다시 실행한다.
- Docker build가 실패하면 `tsconfig.base.json`이 프로젝트 내부에서 독립적으로 해석되는지 먼저 본다.
