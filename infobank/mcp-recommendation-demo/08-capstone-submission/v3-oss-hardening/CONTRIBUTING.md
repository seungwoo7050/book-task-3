# Contributing

`v3-oss-hardening`은 study-first repository 안에 있는 self-hosted OSS candidate다. 따라서 기여의 목표는 기능을 무한 확장하는 것이 아니라, single-team self-hosted 사용성을 더 명확하고 재현 가능하게 만드는 것이다.

## Development Flow

1. `pnpm install`
2. `cp .env.example .env`
3. `pnpm db:up`
4. `pnpm migrate`
5. `pnpm seed`
6. `pnpm bootstrap:owner`
7. `pnpm dev`

## Before Opening A Change

- 먼저 `problem/README.md`와 `docs/README.md`를 읽고 현재 범위를 확인한다.
- multi-workspace SaaS, SSO, live external sync는 현재 비범위다.
- 새로운 기능이 필요하면 왜 `v2`/`v3` 범위 밖에서 굳이 추가해야 하는지 먼저 설명한다.

## Expected Checks

```bash
pnpm build
pnpm test
pnpm test:integration
pnpm e2e
pnpm eval
pnpm compare
pnpm compatibility rc-release-check-bot-1-5-0
pnpm release:gate rc-release-check-bot-1-5-0
```

## Documentation Rule

- tracked 문서는 stable index로 유지한다.
- process-heavy reasoning은 `notion/`에 둔다.
- 발표 자료는 `docs/presentation-deck.md`와 `docs/presentation-assets/`에 유지한다.
