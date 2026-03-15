# 10-shippable-backend-service series map

이 프로젝트는 `09-platform-capstone`을 그대로 복사해 둔 버전이 아니다. 여기서는 Postgres migration, Redis cache/throttling, Swagger, `docker-compose.yml`, request-id, structured logging까지 포함해 "코드를 읽는 과제"를 "실행 절차까지 보여 주는 서비스 표면"으로 바꾸려 한다. 그래서 이 capstone에서 말하는 shippable은 zero-dependency local run이 아니라, 필요한 infra를 함께 올렸을 때 bootstrap부터 e2e까지 재현되는 상태에 더 가깝다.

처음 읽을 때는 `app.bootstrap.ts`와 `app.module.ts`로 서비스가 어떤 전역 계약으로 올라오는지 보고, `AuthRateLimitService`와 `BooksService`에서 Redis가 실제 정책으로 들어가는 장면을 확인한 뒤, `capstone.e2e.test.ts`와 수동 실행 결과로 그 표면이 정말 재현되는지 닫는 순서가 가장 좋다. 이 순서로 보면 README의 주장보다 실제 부팅 조건과 실패 모드가 먼저 보인다.

## 이 글에서 볼 것

- `Swagger + health + migration + seed + compose`가 부가 문서가 아니라 서비스의 일부라는 점
- compose는 "붙을 수 있는 Postgres/Redis가 있다"를 준비할 뿐이고, canonical e2e는 그 위에서 `dropDatabase -> runMigrations -> seedDatabase -> flushDb`까지 다시 수행해 clean baseline을 직접 만든다는 점
- Redis가 단순 부속품이 아니라 `429 login throttle`, `books:list`, `books:detail:<id>` 정책을 바꾸는 핵심 제약이라는 점
- cache 관련 보장도 한 덩어리가 아니라, unit test는 service method의 invalidation 호출을, e2e는 실제 Redis key 생성/삭제를 나눠서 잠근다는 점
- Redis가 없을 때 readiness만 나빠지는 수준이 아니라, 현재 구현에서는 bootstrap 자체가 끝나지 못한다는 운영 리스크

## source of truth

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

## 구현 흐름 한눈에 보기

1. `loadRuntimeConfig`가 `JWT_SECRET`, `DATABASE_URL`, `REDIS_URL`과 throttle/cache TTL을 강제한다.
2. `AppModule`이 Postgres TypeORM, Redis runtime, auth, books, events를 묶고 `RequestIdMiddleware`를 전역에 건다.
3. `configureApp`가 `ValidationPipe`, `HttpExceptionFilter`, `StructuredLoggingInterceptor`, `TransformInterceptor`, Swagger `/docs`를 올린다.
4. `AuthService.login()`은 Redis 기반 실패 횟수 누적으로 `401`에서 `429`로 분기한다.
5. `BooksService`는 public read를 캐시하고, create/update/delete 성공 뒤 list/detail cache를 무효화한다.
6. e2e와 수동 실행으로 `/health/live`, `/health/ready`, `/docs`, login throttle, cache population/invalidation을 다시 확인한다.

## 대표 검증

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test:e2e
FAIL  test/e2e/capstone.e2e.test.ts > Shippable Backend Service E2E
Error: connect ECONNREFUSED 127.0.0.1:5432
```

```bash
$ docker compose up -d postgres redis
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run build
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test:e2e
✓ test/unit/auth.service.test.ts (6 tests)
✓ test/unit/books.service.test.ts (6 tests)
✓ test/e2e/capstone.e2e.test.ts (16 tests)
```

```bash
$ JWT_SECRET=manual-secret DATABASE_URL=postgres://backend:backend@127.0.0.1:5432/shippable_backend \
  REDIS_URL=redis://127.0.0.1:6379 COREPACK_ENABLE_AUTO_PIN=0 pnpm run db:migrate
$ JWT_SECRET=manual-secret DATABASE_URL=postgres://backend:backend@127.0.0.1:5432/shippable_backend \
  REDIS_URL=redis://127.0.0.1:6379 COREPACK_ENABLE_AUTO_PIN=0 pnpm run db:seed
$ curl -s http://localhost:3124/health/ready
{"success":true,"data":{"status":"ready","databaseReady":true,"redisReady":true}}
```

## 지금 시점의 한계

- `StructuredLoggingInterceptor`는 `level`에 실제 severity가 아니라 설정값 `LOG_LEVEL`을 그대로 넣는다. 그래서 e2e처럼 `LOG_LEVEL=error`이면 성공 요청도 `"level":"error"`로 찍힌다.
- 같은 인터셉터는 error path에서 final status code가 확정되기 전에 로그를 남겨, 실제 e2e와 수동 실행 기준 `409`, `401`, `429`, `400` 실패도 로그에는 `statusCode: 200` 또는 `201`로 남는다.
- bare `pnpm run test:e2e`는 Postgres가 없으면 곧바로 `ECONNREFUSED 127.0.0.1:5432`로 실패한다. 즉 canonical verification 자체가 compose-backed bootstrap을 전제로 한다.
- `RedisService.onModuleInit()`는 `client.connect()`를 기다리므로 Redis가 부팅 시점에 죽어 있으면 readiness `503`로 내려가기 전에 앱 bootstrap 자체가 끝나지 못한다.
- seed는 데이터 리셋이 아니라 "admin이 없으면 추가, 책이 0권이면 demo 2권 추가" 방식이라, 이미 데이터가 있는 DB에서는 완전히 같은 초기 상태를 보장하지 않는다.

## 트랙의 끝에서

이 프로젝트는 `backend-node` 트랙의 마지막 장면이다. 여기서 끝나는 건 기능이 아니라 범위다. 다음 확장은 배포, worker, 외부 연동, 장애 복구처럼 별도 운영 축으로 넘어간다.
