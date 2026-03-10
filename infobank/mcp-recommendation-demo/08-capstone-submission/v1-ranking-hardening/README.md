# v1 랭킹 강건화

v0를 바탕으로 reranker, usage logs, feedback loop, baseline/candidate compare를 더한 운영형 추천 버전이다.

## 이번 버전에서 보여 주는 것

- candidate reranking
- usage event API
- feedback API
- experiment CRUD
- compare snapshot UI

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

- 구현 및 검증 완료. baseline 대비 candidate 개선을 설명할 수 있는 첫 버전이다.
- 운영형 추천 시스템으로 넘어가는 핵심 로그와 비교 흐름이 이 버전에서 자리 잡는다.
