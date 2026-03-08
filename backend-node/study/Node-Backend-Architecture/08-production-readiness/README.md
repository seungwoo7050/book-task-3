# 08-production-readiness

- 상태: `verified`
- 구현 레인: `nestjs/`
- 신규 설계 여부: 신규 프로젝트

## 목표

애플리케이션 코드만으로 끝나지 않고,
Docker, config, health check, logging, CI, cache, queue, rate limiting까지
실무형 운영 관점을 붙인다.

## 현재 상태

NestJS starter app, config loader, health/readiness endpoint, structured logging, Dockerfile,
CI 초안, 테스트를 추가했고 새 경로에서 다시 검증했다.

## 실행 명령

- 구현 경로: `nestjs/`
- install: `pnpm install`
- build: `pnpm run build`
- test: `pnpm run test`
- test:e2e: `pnpm run test:e2e`
- run: `pnpm start`

## 검증 상태

- `nestjs/`: `pnpm run build && pnpm run test && pnpm run test:e2e`

## 실패 시 복구 루트

- 앱이 기동 직후 종료되면 `PORT`, `READY`, `LOG_LEVEL` 값이 허용 범위를 벗어났는지 먼저 확인한다.
- readiness 테스트가 실패하면 `process.env.READY`를 읽는 config loader와 `ServiceUnavailableException` 경로를 먼저 본다.
