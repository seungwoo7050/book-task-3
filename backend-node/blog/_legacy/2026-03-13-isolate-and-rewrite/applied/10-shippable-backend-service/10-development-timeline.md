# 10-shippable-backend-service development timeline

이 트랙의 마지막 프로젝트는 "capstone plus more features"로 읽으면 자꾸 길을 잃는다. 실제 코드가 보여 주는 핵심은 더 단순하다. 이전 capstone을 recruiter가 읽을 수 있는 서비스 표면으로 다시 포장하는 일이다. Postgres, Redis, Swagger, Compose, migration, cache, throttling은 기능 그 자체보다 "어떤 실행 계약이 있어야 이 앱을 믿고 다시 띄울 수 있는가"를 설명하기 위해 붙어 있다.

## 구현 순서 요약

- runtime config, bootstrap, DB options, compose surface를 먼저 정리한다.
- Redis cache와 login throttling을 Books/Auth 흐름에 연결한다.
- 인프라 없이 실패하는 e2e와 compose 뒤 성공하는 e2e를 모두 확인한다.

## Phase 1

- 당시 목표: capstone을 제출용 실행 surface로 다시 패키징한다.
- 변경 단위: `nestjs/src/app.bootstrap.ts`, `nestjs/src/runtime/runtime-config.ts`, `nestjs/src/database/database-options.ts`, `docker-compose.yml`
- 처음 가설: 포트폴리오 서비스는 코드보다 먼저 "이 앱이 어떤 env와 어떤 의존성을 요구하는가"를 읽히게 해야 한다.
- 실제 진행: `configureApp()`가 global pipe/filter/interceptor와 Swagger `/docs`를 등록하고, `loadRuntimeConfig()`는 `JWT_SECRET`, `DATABASE_URL`, `REDIS_URL`을 필수로 요구한다. DB는 `postgres` migration 기반 옵션으로 바뀌고, compose 파일은 postgres/redis/app 관계를 문서화한다.

CLI:

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run build
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test
✓ test/unit/books.service.test.ts (6 tests)
✓ test/unit/auth.service.test.ts (6 tests)
Tests 12 passed (12)
```

검증 신호:

- unit test 12개가 books/auth 기본 계약을 유지한다.
- 잘못된 비밀번호는 `UnauthorizedException`으로 계속 닫힌다.

핵심 코드:

```ts
const swaggerConfig = new DocumentBuilder()
  .setTitle("Shippable Backend Service")
  .setDescription("Portfolio-ready NestJS service for junior backend applications")
  .setVersion("1.0.0")
  .addBearerAuth()
  .build();
SwaggerModule.setup("docs", app, swaggerDocument);
```

왜 이 코드가 중요했는가:

학습용 capstone과 제출용 surface의 차이가 여기서 드러난다. 단순히 endpoint가 많은 게 아니라, 검토자가 어디서 API 표면을 볼지까지 코드가 먼저 제공한다.

새로 배운 것:

- 포트폴리오 서비스는 기능 구현보다 실행 계약과 관찰 surface를 먼저 명확히 보여 주는 편이 훨씬 설득력이 있다.

## Phase 2

- 당시 목표: Redis를 cache와 login throttling 양쪽에 연결해 운영성 surface를 실제 기능 흐름 안으로 끌어온다.
- 변경 단위: `nestjs/src/books/books.service.ts`, `nestjs/src/auth/auth.service.ts`, `nestjs/src/auth/auth-rate-limit.service.ts`, `nestjs/src/runtime/redis.service.ts`, `nestjs/src/health.controller.ts`
- 처음 가설: 제출용 backend라면 "읽기 캐시가 있다", "로그인 실패를 제한한다", "DB/Redis readiness를 본다" 같은 운영 신호가 실제 코드에 보여야 한다.
- 실제 진행: `BooksService.findAll()/findOne()`이 Redis cache를 읽고 `create/update/remove()`가 cache를 무효화한다. `AuthRateLimitService`는 `auth:login:${clientId}` key로 실패 횟수를 세고, health readiness는 Postgres와 Redis를 모두 확인한다.

CLI:

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test
Tests 12 passed (12)
```

검증 신호:

- unit test는 wrong password, cache invalidation 전제, auth service 경계를 계속 통과한다.
- e2e 준비 코드는 `books:list`, `books:detail:<id>` cache key와 login throttling env를 직접 참조한다.

핵심 코드:

```ts
const cached = await this.redisService.getJson<Book[]>(this.listCacheKey);
if (cached) {
  return cached;
}
...
await this.redisService.deleteMany([this.listCacheKey, this.getDetailCacheKey(id)]);
```

왜 이 코드가 중요했는가:

shippable surface는 단순 CRUD를 넘어서 "읽기 성능과 쓰기 후 일관성"까지 의식한다. list/detail cache와 invalidate가 함께 있어야 그 이야기를 할 수 있다.

새로 배운 것:

- 운영성 기능은 보통 별도 장으로 설명되지만, 실제 코드는 기존 use case 안에 스며들 때 가장 설득력 있게 읽힌다.

## Phase 3

- 당시 목표: 이 서비스가 코드만으로는 완성되지 않는다는 사실까지 포함해 재검증한다.
- 변경 단위: `docker-compose.yml`, `nestjs/test/e2e/capstone.e2e.test.ts`
- 처음 가설: 제출용 backend의 진짜 검증은 unit pass가 아니라 Postgres/Redis가 실제로 붙은 상태에서의 end-to-end다.
- 실제 진행: 먼저 infra 없이 `pnpm run test:e2e`를 돌려 `connect ECONNREFUSED 127.0.0.1:5432`를 확인했다. 그 다음 `docker compose up -d postgres redis`로 의존성을 띄우고 health가 `healthy`가 된 뒤 e2e를 다시 실행했다.

CLI:

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test:e2e
Error: connect ECONNREFUSED 127.0.0.1:5432

$ docker compose up -d postgres redis
Container 10-shippable-backend-service-postgres-1  Started
Container 10-shippable-backend-service-redis-1     Started

$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test:e2e
✓ test/e2e/capstone.e2e.test.ts (16 tests)
Tests 16 passed (16)
```

검증 신호:

- infra 없이 돌리면 16개 e2e가 모두 skip되고 suite가 실패한다.
- compose 뒤에는 `/health/live`, `/health/ready`, `/docs`, register/login, throttling, cache, admin CRUD, 403, 404까지 모두 통과한다.

핵심 코드:

```ts
process.env.DATABASE_URL =
  process.env.DATABASE_URL || "postgres://backend:backend@127.0.0.1:5432/shippable_backend";
process.env.REDIS_URL = process.env.REDIS_URL || "redis://127.0.0.1:6379";
```

왜 이 코드가 중요했는가:

이 e2e는 처음부터 "로컬 infra가 있어야 완성되는 서비스"를 전제로 한다. 실패와 성공 둘 다 남겨야 이 프로젝트의 실행 계약이 정말 읽힌다.

새로 배운 것:

- shippable backend의 완성도는 코드 품질만으로는 설명되지 않는다. 재현 가능한 infra 전제까지 검증 경로 안에 들어와야 한다.

다음:

- 이 트랙의 blog 시리즈는 여기서 끝난다. 이후 확장은 배포, worker, 외부 연동 같은 별도 프로젝트 축으로 분리하는 편이 자연스럽다.
