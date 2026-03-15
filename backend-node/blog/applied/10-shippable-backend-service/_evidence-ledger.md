# 10-shippable-backend-service evidence ledger

이 경로의 git history 역시 `2026-03-12` 이관 커밋 한 번만 보인다. 그래서 chronology는 commit message 대신 실제 소스, 테스트, Docker/CLI 재실행, 부팅 실패 실험으로 다시 세웠다.

| 순서 | 시간 표지 | 당시 목표 | 변경 단위 | 처음 가설 | 실제 조치 | CLI | 검증 신호 | 핵심 코드 앵커 | 새로 배운 것 | 다음 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Phase 1 | `09`를 실행 가능한 서비스 표면으로 끌어올린다 | `nestjs/src/app.bootstrap.ts`, `app.module.ts`, `health.controller.ts`, `common/middleware/request-id.middleware.ts`, `database/migrations/1710000000000-initial-schema.ts`, `database/seed-data.ts` | README와 Swagger만 있으면 제출용 표면으로 충분할 것 같았다 | 전역 pipe/filter/interceptor, Swagger `/docs`, `x-request-id`, health endpoints, Postgres migration, conditional seed까지 포함해 부팅 절차를 코드로 고정했다 | `COREPACK_ENABLE_AUTO_PIN=0 pnpm run build`; `JWT_SECRET=... DATABASE_URL=... REDIS_URL=... pnpm run db:migrate`; `... pnpm run db:seed` | build 통과, migrate/seed 성공 | `SwaggerModule.setup("docs", app, swaggerDocument)`, `consumer.apply(RequestIdMiddleware).forRoutes("*")` | 제출용 서비스는 기능보다 bootstrap과 init 절차가 먼저 보여야 한다 | Redis가 실제 정책을 어떻게 바꾸는지 닫아야 한다 |
| 2 | Phase 2 | Redis를 부가 기능이 아니라 정책으로 확인한다 | `auth/auth.controller.ts`, `auth/auth.service.ts`, `auth/auth-rate-limit.service.ts`, `books/books.service.ts`, `runtime/redis.service.ts` | Redis는 붙어만 있으면 충분할 것 같았다 | `x-forwarded-for` 기반 login throttle, `books:list` / `books:detail:<id>` cache, write 후 invalidation을 코드와 수동 실행으로 재확인했다 | `curl -s -X POST /auth/login ... -H 'x-forwarded-for: 203.0.113.77'`; `curl -s /books`; `docker exec ... redis-cli GET books:list` | 동일 clientId 잘못된 로그인은 `401,401,401,401,429`, `GET /books` 뒤 list cache 생성, create 뒤 list cache 삭제 | `await this.authRateLimitService.ensureLoginAllowed(clientId)`, `await this.invalidateBookCaches(saved.id)` | Redis는 이 서비스에서 성능 장치가 아니라 응답 코드를 바꾸는 정책 엔진이다 | 테스트와 수동 실행이 이 정책을 실제로 고정하는지 봐야 한다 |
| 3 | Phase 3 | 인프라 포함 검증 루프를 다시 돌린다 | `test/unit/auth.service.test.ts`, `test/unit/books.service.test.ts`, `test/e2e/capstone.e2e.test.ts`, `docker-compose.yml` | 단위 테스트만 통과해도 문서화에는 충분할 것 같았다 | Docker로 Postgres/Redis를 올리고 unit 12개, e2e 16개를 다시 돌린 뒤 `/health/live`, `/health/ready`, `/docs`, login, cache, invalidation을 수동으로 재확인했다 | `docker compose up -d postgres redis`; `pnpm run test`; `pnpm run test:e2e`; `curl -s http://localhost:3124/health/ready`; `curl -s http://localhost:3124/docs` | unit 12개 통과, e2e 16개 통과, `/health/ready`는 `databaseReady:true`, `redisReady:true`, `/docs`는 Swagger UI 노출 | e2e의 `dropDatabase -> runMigrations -> seedDatabase -> redis flush` | shippable 검증은 앱 내부 테스트가 아니라 인프라와 함께 끝까지 부팅되는지까지 포함한다 | 운영 로그와 실패 모드를 따로 봐야 한다 |
| 4 | Phase 4 | 로그와 장애 시동 실패를 확인한다 | `runtime/structured-logging.interceptor.ts`, `runtime/redis.service.ts` | Redis 장애는 readiness `503` 정도로만 드러날 것 같았다 | e2e/stdout과 수동 실행을 비교해 성공 요청도 `LOG_LEVEL` 값 그대로 기록된다는 점, error request가 `statusCode:200/201`로 남는 점, 잘못된 `REDIS_URL`에서는 bootstrap이 끝나지 않는 점을 확인했다 | `COREPACK_ENABLE_AUTO_PIN=0 pnpm run test:e2e`; `REDIS_URL=redis://127.0.0.1:6380 node dist/main.js` | e2e 로그에 성공 요청도 `"level":"error"`, 실패 요청도 `"statusCode":200/201`; invalid Redis로는 `ECONNREFUSED` 경고 반복 후 port bind 없음 | `level: config.logLevel`, `tap({ error: ... })`, `await this.ensureConnected()` | 현재 로그는 관측 가능해 보이지만 의미가 다소 왜곡되고, Redis 부재는 fail-open보다 startup hang에 가깝다 | 트랙을 닫기 전에 이 약점을 문서에 분명히 남겨야 한다 |

## 후속 재검증 메모

- `2026-03-14` 후속 점검에서 compose 없이 `COREPACK_ENABLE_AUTO_PIN=0 pnpm run test:e2e`를 먼저 실행하면 `connect ECONNREFUSED 127.0.0.1:5432`로 즉시 실패했다.
- 같은 턴에 `docker compose up -d postgres redis` 후 `COREPACK_ENABLE_AUTO_PIN=0 pnpm run test`와 `COREPACK_ENABLE_AUTO_PIN=0 pnpm run test:e2e`를 다시 실행하자 unit 12개, e2e 16개가 모두 통과했다.
- `books.service.test.ts`는 cache invalidation 메서드 호출을 직접 잠그고, e2e는 실제 Redis key materialization/invalidation을 확인한다.
- 그래서 이 프로젝트의 canonical verification은 "로컬에서 그냥 test:e2e"가 아니라, compose로 infra를 먼저 올린 뒤 테스트 bootstrap이 DB/Redis 상태를 다시 비우는 절차까지 포함해 확인하는 루프라고 적는 편이 정확하다.

## 근거 파일

- `applied/10-shippable-backend-service/README.md`
- `applied/10-shippable-backend-service/problem/README.md`
- `applied/10-shippable-backend-service/docker-compose.yml`
- `applied/10-shippable-backend-service/nestjs/.env.example`
- `applied/10-shippable-backend-service/nestjs/src/app.bootstrap.ts`
- `applied/10-shippable-backend-service/nestjs/src/app.module.ts`
- `applied/10-shippable-backend-service/nestjs/src/health.controller.ts`
- `applied/10-shippable-backend-service/nestjs/src/common/middleware/request-id.middleware.ts`
- `applied/10-shippable-backend-service/nestjs/src/auth/auth.controller.ts`
- `applied/10-shippable-backend-service/nestjs/src/auth/auth.service.ts`
- `applied/10-shippable-backend-service/nestjs/src/auth/auth-rate-limit.service.ts`
- `applied/10-shippable-backend-service/nestjs/src/books/books.service.ts`
- `applied/10-shippable-backend-service/nestjs/src/runtime/redis.service.ts`
- `applied/10-shippable-backend-service/nestjs/src/runtime/runtime-config.ts`
- `applied/10-shippable-backend-service/nestjs/src/runtime/structured-logging.interceptor.ts`
- `applied/10-shippable-backend-service/nestjs/src/database/database-options.ts`
- `applied/10-shippable-backend-service/nestjs/src/database/migrations/1710000000000-initial-schema.ts`
- `applied/10-shippable-backend-service/nestjs/src/database/scripts/migrate.ts`
- `applied/10-shippable-backend-service/nestjs/src/database/scripts/seed.ts`
- `applied/10-shippable-backend-service/nestjs/src/database/seed-data.ts`
- `applied/10-shippable-backend-service/nestjs/test/unit/auth.service.test.ts`
- `applied/10-shippable-backend-service/nestjs/test/unit/books.service.test.ts`
- `applied/10-shippable-backend-service/nestjs/test/e2e/capstone.e2e.test.ts`
