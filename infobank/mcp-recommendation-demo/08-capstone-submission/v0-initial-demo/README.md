# v0 초기 실행 데모

registry seed, manifest validation, baseline selector, 한국어 추천 근거, offline eval까지 동작하는 최초 runnable 데모다.

## 이번 버전에서 보여 주는 것

- catalog list/detail
- manifest validate
- baseline recommendation
- offline eval
- Next.js dashboard

## 실행 명령

```bash
pnpm install
cp .env.example .env
pnpm db:up
pnpm migrate
pnpm seed
pnpm dev
pnpm test
pnpm eval
pnpm capture:presentation
pnpm e2e
```

## 먼저 확인할 문서

- `docs/README.md`
- `docs/presentation-deck.md`
- `docs/presentation-assets/`
- `problem/README.md`

## 현재 상태

- 구현 및 검증 완료 상태의 baseline snapshot이다.
- 학생이 처음 실행해 보기 가장 좋은 capstone 버전이다.
