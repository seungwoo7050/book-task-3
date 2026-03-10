# 기여 안내

`v3-oss-hardening`은 학습 우선 레포 안에 있는 self-hosted OSS 후보 버전이다. 따라서 기여의 목표는 기능을 무한 확장하는 것이 아니라, 한 팀이 직접 설치해 재현 가능한 운영 경로를 더 분명하게 만드는 것이다.

## 개발 흐름

1. `pnpm install`
2. `cp .env.example .env`
3. `pnpm db:up`
4. `pnpm migrate`
5. `pnpm seed`
6. `pnpm bootstrap:owner`
7. `pnpm dev`

## 변경 전 확인 사항

- 먼저 `problem/README.md`와 `docs/README.md`를 읽고 현재 범위를 확인한다.
- multi-workspace SaaS, SSO, live external sync는 현재 범위 밖이다.
- 새로운 기능이 필요하면 왜 `v2`/`v3` 범위 밖에서 굳이 추가해야 하는지 먼저 설명한다.

## 기대 검증 항목

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

## 문서 작성 원칙

- tracked 문서는 안정적인 인덱스로 유지한다.
- process-heavy reasoning은 `notion/`에 둔다.
- 발표 자료는 `docs/presentation-deck.md`와 `docs/presentation-assets/`에 유지한다.
