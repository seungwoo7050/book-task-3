# Install

## Local Install

```bash
pnpm install
cp .env.example .env
pnpm db:up
pnpm migrate
pnpm seed
pnpm bootstrap:owner
pnpm dev
```

Endpoints:

- Web: `http://127.0.0.1:3003`
- API: `http://127.0.0.1:3103`
- Metrics: `http://127.0.0.1:3103/metrics`
- Health: `http://127.0.0.1:3103/healthz`
- Ready: `http://127.0.0.1:3103/readyz`

## Compose Install

```bash
docker compose up -d --build
```

Compose topology:

- `postgres`: persistent Postgres
- `api`: Fastify API, migration on boot
- `worker`: pg-boss consumer
- `web`: Next.js dashboard

## Seed Accounts

- `owner@study1.local / ChangeMe123!`
- `operator@study1.local / Operator123!`
- `viewer@study1.local / Viewer123!`

운영 전제에서는 `pnpm bootstrap:owner`로 owner를 다시 지정하고, seed 비밀번호를 즉시 바꾸는 것이 맞다.
