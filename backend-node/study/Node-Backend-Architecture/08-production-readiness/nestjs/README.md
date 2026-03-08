# NestJS Implementation

## 범위

운영 준비 기능을 모아 놓은 실무 지향 NestJS starter app을 제공한다.

## 현재 상태

- 상태: `verified`
- build: `pnpm run build`
- test: `pnpm run test`
- test:e2e: `pnpm run test:e2e`
- run: `pnpm start`

## 포함된 것

- `src/runtime/runtime-config.ts`: env 로더와 검증
- `src/runtime/structured-logging.interceptor.ts`: 요청 단위 JSON 로그
- `src/health.controller.ts`: health/readiness endpoint
- `Dockerfile`: 로컬/CI 빌드 기준점
- `ci/github-actions.yml`: 샘플 CI 워크플로

## 알려진 제약

- rate limiting, cache, queue는 문서와 체크리스트 수준으로만 포함한다.
