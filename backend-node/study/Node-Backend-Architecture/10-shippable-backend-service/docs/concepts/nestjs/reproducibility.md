# Reproducibility

## 로컬 기준 경로

1. `docker compose up -d postgres redis`
2. `cd nestjs`
3. `pnpm install`
4. `cp .env.example .env`
5. `pnpm run db:migrate`
6. `pnpm run db:seed`
7. `pnpm run start`

## Compose 기준 경로

- 프로젝트 루트에서 `docker compose up -d app`
- app 컨테이너는 migration과 seed를 먼저 실행한 뒤 서버를 시작한다.

## CI 기준 경로

- GitHub Actions service containers로 Postgres와 Redis를 준비한다.
- `pnpm install -> build -> db:migrate -> db:seed -> test -> test:e2e` 순서를 따른다.
