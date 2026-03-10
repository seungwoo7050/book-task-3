# 설치 안내

## 로컬 설치

```bash
pnpm install
cp .env.example .env
pnpm db:up
pnpm migrate
pnpm seed
pnpm bootstrap:owner
pnpm dev
```

접속 경로:

- Web: `http://127.0.0.1:3003`
- API: `http://127.0.0.1:3103`
- Metrics: `http://127.0.0.1:3103/metrics`
- Health: `http://127.0.0.1:3103/healthz`
- Ready: `http://127.0.0.1:3103/readyz`

## Compose 설치

```bash
docker compose up -d --build
```

Compose 구성:

- `postgres`: persistent Postgres
- `api`: Fastify API, migration on boot
- `worker`: pg-boss consumer
- `web`: Next.js dashboard

## 시드 계정

- `owner@study1.local / ChangeMe123!`
- `operator@study1.local / Operator123!`
- `viewer@study1.local / Viewer123!`

운영 전제에서는 `pnpm bootstrap:owner`로 owner를 다시 지정하고, seed 비밀번호를 즉시 바꾸는 것이 맞다.
