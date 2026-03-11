# v0 초기 실행 데모 문제 정의

## 이번 버전의 목표

registry seed, manifest validation, baseline selector, 한국어 추천 근거, offline eval까지 동작하는 최초 runnable 데모다.

## 최소 범위

- registry seed와 manifest validation
- baseline selector와 한국어 추천 근거
- offline eval과 기본 운영 화면

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
- offline eval 결과
