# 10-shippable-backend-service evidence ledger

근거는 [`README.md`](../../../study/Node-Backend-Architecture/applied/10-shippable-backend-service/README.md), [`docker-compose.yml`](../../../study/Node-Backend-Architecture/applied/10-shippable-backend-service/docker-compose.yml), [`nestjs/src/app.bootstrap.ts`](../../../study/Node-Backend-Architecture/applied/10-shippable-backend-service/nestjs/src/app.bootstrap.ts), [`nestjs/src/runtime/runtime-config.ts`](../../../study/Node-Backend-Architecture/applied/10-shippable-backend-service/nestjs/src/runtime/runtime-config.ts), [`nestjs/src/database/database-options.ts`](../../../study/Node-Backend-Architecture/applied/10-shippable-backend-service/nestjs/src/database/database-options.ts), [`nestjs/src/books/books.service.ts`](../../../study/Node-Backend-Architecture/applied/10-shippable-backend-service/nestjs/src/books/books.service.ts), [`nestjs/src/auth/auth-rate-limit.service.ts`](../../../study/Node-Backend-Architecture/applied/10-shippable-backend-service/nestjs/src/auth/auth-rate-limit.service.ts), [`nestjs/src/runtime/redis.service.ts`](../../../study/Node-Backend-Architecture/applied/10-shippable-backend-service/nestjs/src/runtime/redis.service.ts), [`nestjs/test/e2e/capstone.e2e.test.ts`](../../../study/Node-Backend-Architecture/applied/10-shippable-backend-service/nestjs/test/e2e/capstone.e2e.test.ts), 실제 CLI와 compose 출력이다.

## Phase 1

- 순서: 1
- 시간 표지: Phase 1
- 당시 목표: 학습용 capstone을 제출용 서비스 표면으로 다시 포장한다.
- 변경 단위: `nestjs/src/app.bootstrap.ts`, `nestjs/src/runtime/runtime-config.ts`, `nestjs/src/database/database-options.ts`, `docker-compose.yml`
- 처음 가설: 포트폴리오 표면의 핵심은 기능 추가보다 "어떤 infra와 env가 있어야 이 앱이 뜨는가"를 README와 bootstrap이 함께 설명하는 것이다.
- 실제 조치: Swagger를 `/docs`에 올리고, runtime config에서 `JWT_SECRET`, `DATABASE_URL`, `REDIS_URL`을 필수로 요구하며, DB는 Postgres migration 기반으로 바꿨다.
- CLI: `COREPACK_ENABLE_AUTO_PIN=0 pnpm run build`, `COREPACK_ENABLE_AUTO_PIN=0 pnpm run test`
- 검증 신호: unit `Tests 12 passed (12)`
- 핵심 코드 앵커: `configureApp()`, `loadRuntimeConfig()`, `createDatabaseOptions()`
- 새로 배운 것: 포트폴리오 서비스는 코드보다 실행 계약이 먼저 읽혀야 한다.
- 다음: Redis cache와 login throttling 같은 운영 기능을 Books/Auth 서비스에 묶는다.

## Phase 2

- 순서: 2
- 시간 표지: Phase 2
- 당시 목표: Redis를 cache와 login throttling 양쪽에 연결해 서비스 표면을 더 운영 친화적으로 만든다.
- 변경 단위: `nestjs/src/books/books.service.ts`, `nestjs/src/auth/auth.service.ts`, `nestjs/src/auth/auth-rate-limit.service.ts`, `nestjs/src/runtime/redis.service.ts`, `nestjs/src/health.controller.ts`
- 처음 가설: 제출용 surface는 "책 CRUD가 된다"보다 "list cache, detail cache, login throttling, readiness check를 왜 붙였는가"를 보여 줘야 한다.
- 실제 조치: `BooksService`가 list/detail cache를 읽고 무효화하며, `AuthRateLimitService`가 Redis key로 로그인 실패 횟수를 제한한다. health readiness는 Postgres와 Redis를 같이 확인한다.
- CLI: `COREPACK_ENABLE_AUTO_PIN=0 pnpm run test`
- 검증 신호: unit test 12개 통과, auth wrong password 케이스 포함
- 핵심 코드 앵커: `BooksService.findAll()/invalidateBookCaches()`, `AuthRateLimitService.ensureLoginAllowed()`, `HealthController.getReadiness()`
- 새로 배운 것: 운영성은 별도 마이크로서비스가 아니라도 cache/throttle/health를 통해 충분히 surface에 드러낼 수 있다.
- 다음: e2e가 실제 infra 없이는 왜 실패하는지, 그리고 compose를 올리면 어떻게 통과하는지 확인한다.

## Phase 3

- 순서: 3
- 시간 표지: Phase 3
- 당시 목표: compose-backed infra 위에서 제출용 surface 전체를 재검증한다.
- 변경 단위: `docker-compose.yml`, `nestjs/test/e2e/capstone.e2e.test.ts`
- 처음 가설: 이 프로젝트의 핵심 검증은 pure unit test가 아니라 Postgres/Redis가 실제로 붙은 상태에서만 완성된다.
- 실제 조치: 먼저 `pnpm run test:e2e`를 단독 실행해 `connect ECONNREFUSED 127.0.0.1:5432`를 확인했고, 이어 `docker compose up -d postgres redis`로 의존성을 띄운 뒤 e2e를 다시 실행했다.
- CLI: `docker compose up -d postgres redis`, `COREPACK_ENABLE_AUTO_PIN=0 pnpm run test:e2e`
- 검증 신호: 초기 실패 `16 skipped`, infra 기동 후 `✓ test/e2e/capstone.e2e.test.ts (16 tests)`, `Tests 16 passed (16)`
- 핵심 코드 앵커: `capstone.e2e.test.ts`, `docker-compose.yml`
- 새로 배운 것: recruiter-facing 서비스는 코드만 맞아서는 안 되고, "실행 전제 조건"까지 검증 경로 안에 들어와야 한다.
- 다음: 이 트랙의 끝 단계다. 이후 확장은 배포, worker, 외부 연동처럼 별도 축으로 나뉜다.
