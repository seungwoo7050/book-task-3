# v1 랭킹 강건화 문제 정의

## 이번 버전의 목표

v0를 바탕으로 reranker, usage logs, feedback loop, baseline/candidate compare를 더한 운영형 추천 버전이다.

## 최소 범위

- reranker와 compare runner
- usage/feedback/experiment API
- 운영 콘솔의 compare 화면

## 검증 명령

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

## 증빙 산출물

- presentation deck
- presentation capture assets
- compare proof와 usage 흐름 설명
