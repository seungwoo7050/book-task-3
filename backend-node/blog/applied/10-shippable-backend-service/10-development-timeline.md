# 10-shippable-backend-service development timeline

이 프로젝트를 따라가면 "기능을 조금 더 넣었다"는 느낌보다 "부팅 절차 자체를 과제 범위로 끌어올렸다"는 인상이 먼저 든다. `09-platform-capstone`이 단일 앱 안에서 계약을 통합하는 단계였다면, 이번에는 그 계약을 실제 서비스처럼 켜고 검증하는 절차가 코드 안으로 들어온다.

## 1. 먼저 서비스 표면을 코드로 고정한다

첫 기준선은 `configureApp()`이다. 이 함수는 `ValidationPipe`, `HttpExceptionFilter`, `StructuredLoggingInterceptor`, `TransformInterceptor`를 설치하고, Swagger를 `/docs`에 붙인다. 즉 controller를 많이 보여 주기 전에 "이 앱은 어떤 공통 표면으로 노출되는가"를 먼저 결정한다.

`AppModule`도 같은 방향으로 읽힌다. `RuntimeModule`이 env를 검증하고, `TypeOrmModule.forRootAsync`가 Postgres 연결을 만들고, `RequestIdMiddleware`가 모든 요청에 `x-request-id`를 심는다. 여기에 `HealthController`가 `GET /health/live`, `GET /health/ready`를 제공하니, 이 앱은 business feature보다 runtime contract부터 노출하는 구조가 된다.

데이터 초기화도 controller 밖으로 빠져 있다. migration은 `pgcrypto` extension과 `users`, `books` 테이블을 만들고, seed는 admin 사용자와 demo 책 2권만 조건부로 채운다. 그래서 이 프로젝트에서 "앱을 띄운다"는 말에는 `pnpm run db:migrate`, `pnpm run db:seed`가 반드시 포함된다.

## 2. Redis는 옵션이 아니라 정책을 바꾼다

두 번째 전환점은 Redis가 실제 decision path에 들어가는 순간이다. `AuthController`는 `x-forwarded-for`의 첫 값을 `clientId`로 쓰고, 없으면 `username:<username>`으로 대체한다. `AuthService.login()`은 이 `clientId`에 대해 먼저 `ensureLoginAllowed()`를 호출하고, 실패 횟수를 누적하다가 임계치부터는 `401`이 아니라 `429 Too many login attempts`를 반환한다.

이 구조가 중요한 이유는 throttle이 미들웨어 예제가 아니라 인증 정책 그 자체를 바꾸기 때문이다. 수동 재실행에서도 같은 `x-forwarded-for`로 잘못된 비밀번호를 다섯 번 보내면 `401, 401, 401, 401, 429`로 바뀌는 것을 확인했다.

책 서비스도 마찬가지다. `findAll()`은 `books:list`, `findOne()`은 `books:detail:<id>`를 Redis에서 먼저 확인하고, miss일 때만 Postgres를 조회한다. 반대로 create/update/delete는 save/remove 성공 뒤에 list/detail cache를 지운다. 실제 수동 재실행에서도 `GET /books`와 `GET /books/:id` 뒤에는 Redis key가 채워지고, 책 생성 뒤에는 `books:list`가 비워지는 것을 다시 확인했다.

## 3. 검증도 인프라를 포함한 채로 설계돼 있다

이 프로젝트의 테스트는 더 이상 앱 내부 로직만 보지 않는다. unit test는 auth와 books를 각각 6개씩 검증하고, e2e는 아예 `dist`에서 `AppModule`, `configureApp`, `createAppDataSource`, `seedDatabase`를 import한 뒤 Postgres database를 drop/migrate/seed하고 Redis를 flush한 다음에 시작한다.

```bash
$ docker compose up -d postgres redis
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run build
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test:e2e
✓ test/unit/auth.service.test.ts (6 tests)
✓ test/unit/books.service.test.ts (6 tests)
✓ test/e2e/capstone.e2e.test.ts (16 tests)
```

이 16개 e2e는 `/health/live`, `/health/ready`, `/docs`, register/login, duplicate username, throttle, public books read, cache population, admin create/update/delete, regular user `403`, invalid body `400`, missing book `404`까지 한 흐름에 묶는다. 즉 이 프로젝트에서 검증 성공은 "API가 맞다"보다 "필요한 인프라와 함께 서비스가 실제로 올라온다"에 더 가깝다. 실제로 이번 후속 점검에서도 `pnpm run test:e2e`를 compose 없이 먼저 실행하면 `connect ECONNREFUSED 127.0.0.1:5432`에서 즉시 멈췄고, `docker compose up -d postgres redis` 뒤에는 다시 16개가 모두 통과했다.

여기서 한 가지를 더 분리해 두는 편이 정확했다. compose는 reachable infra를 준비할 뿐이고, 재현 가능한 clean state는 e2e bootstrap이 직접 만든다. `capstone.e2e.test.ts`는 이미 떠 있는 Postgres에 연결한 뒤 `dropDatabase()`, `runMigrations()`, `seedDatabase()`를 실행하고, Redis도 `flushDb()`로 비운다. 그래서 이 프로젝트의 canonical proof는 "compose만 성공했다"가 아니라 "compose-backed infra 위에서 테스트가 상태를 다시 리셋하고도 통과했다"에 가깝다.

cache도 같은 식으로 두 층으로 읽는 편이 낫다. `books.service.test.ts`는 `deleteMany(["books:list", "books:detail:<id>"])` 같은 method-level invalidation 호출을 잠그고, e2e는 실제 HTTP 요청 뒤에 Redis key가 생기고 사라지는지까지 확인한다. 이번 보강에서는 이 둘을 하나의 막연한 "cache works"로 뭉개지 않았다.

## 4. 수동 실행으로 보면 README보다 먼저 드러나는 약점이 있다

수동으로 `db:migrate`, `db:seed`, `node dist/main.js`까지 실행해 보면 `/health/ready`는 `{"status":"ready","databaseReady":true,"redisReady":true}`, `/docs`는 실제 Swagger UI, `/health/live` 응답에는 `x-request-id` 헤더까지 붙는다. 겉보기에는 꽤 단단한 서비스처럼 보인다.

그런데 로그를 보면 다른 이야기가 나온다. `StructuredLoggingInterceptor`는 payload의 `level`에 실제 severity가 아니라 설정값 `LOG_LEVEL`을 그대로 넣는다. 그래서 e2e가 `LOG_LEVEL=error`로 돌 때는 성공한 `GET /health/live`조차 `"level":"error"`로 출력된다. 더 큰 문제는 error path에서도 exception filter가 최종 status를 쓰기 전에 인터셉터가 먼저 로그를 남긴다는 점이다. e2e와 수동 실행 모두에서 실패한 `POST /auth/login`, `POST /books`, `GET /books/:id`가 로그에는 `statusCode: 200` 또는 `201`로 찍혔다.

## 5. 부팅 실패 모드는 readiness보다 앞에서 막힌다

가장 중요한 마지막 발견은 Redis가 죽었을 때의 동작이다. 소스만 보면 `RedisService`의 `getJson()`, `setJson()`, `incrementWithExpiry()`는 연결 실패 시 null/0/no-op로 떨어지기 때문에, 한동안은 cache와 throttle만 비활성화되고 앱은 계속 돌 것처럼 보인다.

하지만 실제 bootstrap은 더 앞단에서 멈춘다. `RedisService.onModuleInit()`가 `await this.ensureConnected()`를 기다리는데, 내부 `client.connect()`는 reconnect strategy를 가진 채 반복 재시도한다. 수동으로 `REDIS_URL=redis://127.0.0.1:6380`으로 띄워 보니 앱은 port bind까지 가지 못하고 `Redis connection error: ECONNREFUSED` 경고만 반복했다. 즉 현재 구현에서 Redis 부재는 readiness `503` 문제가 아니라 startup hang에 가깝다.

이 지점까지 보면 이 프로젝트의 목적이 분명해진다. 단순히 "포트폴리오용으로 보기 좋게 만들었다"가 아니라, 서비스 표면과 검증 절차를 코드로 올려두되, 아직 운영적으로 거친 부분이 어디인지도 함께 드러내는 단계라는 것. 그래서 이 트랙의 마지막 장으로 적절하다.
