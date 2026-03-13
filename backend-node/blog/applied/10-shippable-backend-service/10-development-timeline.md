# 10-shippable-backend-service development timeline

이 프로젝트는 09번 capstone을 그대로 공개하는 대신, 채용 검토자가 실제 서비스처럼 읽고 검증할 수 있는 표면으로 다시 정리한 버전이다. 그래서 처음 눈에 들어오는 것도 controller 코드보다 bootstrap, migration, Redis policy, infra-backed e2e 쪽이다.

## 흐름 먼저 보기

1. `configureApp`와 migration으로 제출용 표면을 세운다.
2. Redis cache와 login throttling을 service flow 안으로 넣는다.
3. infra 없는 실패와 compose 이후 성공을 한 검증 루프로 묶는다.

## 제출용 표면을 세운 장면

capstone에 README만 덧붙인다고 제출용 서비스처럼 보이지는 않는다. 이 프로젝트가 따로 서는 이유는 bootstrap과 schema, docs 표면이 먼저 정리돼 있기 때문이다.

```ts
app.useGlobalPipes(
  new ValidationPipe({
    whitelist: true,
    forbidNonWhitelisted: true,
    transform: true,
  }),
);
app.useGlobalFilters(new HttpExceptionFilter());
app.useGlobalInterceptors(app.get(StructuredLoggingInterceptor), new TransformInterceptor());
```

이 bootstrap은 "앱이 어떤 공통 규약으로 올라오는가"를 한곳에 모아 둔다. 제출용 서비스가 controller 개수보다 먼저 읽히는 지점이 바로 여기다.

Swagger도 같은 역할을 한다.

```ts
const swaggerDocument = SwaggerModule.createDocument(app, swaggerConfig);
SwaggerModule.setup("docs", app, swaggerDocument);
```

즉 이 프로젝트는 기능을 많이 늘린 게 아니라, 검토자가 `/docs`와 bootstrap만 봐도 서비스 표면을 이해할 수 있게 만든 셈이다. migration도 같은 맥락이다.

```ts
await queryRunner.query(`
  CREATE TABLE "users" (
    "id" uuid NOT NULL DEFAULT gen_random_uuid(),
    "username" character varying(30) NOT NULL,
    ...
  )
`);
```

schema가 코드 밖의 별도 단계로 분리돼 있어야 "서비스를 띄운다"는 말에 실제 데이터 초기화 절차가 붙는다.

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run build && pnpm run test
Tests       12 passed (12)
Duration    1.98s
```

## 인프라 제약을 서비스 경로에 넣은 장면

다음 전환점은 Redis를 단순한 부가 기능이 아니라 실제 policy로 다루는 부분에서 나온다. 먼저 로그인 시도 제한이 그렇다.

```ts
await this.authRateLimitService.ensureLoginAllowed(clientId);

const user = await this.userRepository.findOneBy({ username });
if (!user) {
  const attempts = await this.authRateLimitService.recordFailedAttempt(clientId);
  if (this.authRateLimitService.isBlockedAttemptCount(attempts)) {
    throw new HttpException("Too many login attempts", HttpStatus.TOO_MANY_REQUESTS);
  }
  throw new UnauthorizedException("Invalid credentials");
}
```

이 코드가 중요한 이유는 rate limit이 controller 바깥 미들웨어 예제가 아니라, 인증 정책 그 자체를 바꾸는 decision path 안으로 들어왔기 때문이다. 이제 잘못된 비밀번호를 반복하면 결과가 단순 `401`이 아니라 실제 `429`로 바뀐다.

books 서비스도 같은 결이다.

```ts
const cached = await this.redisService.getJson<Book[]>(this.listCacheKey);
if (cached) {
  return cached;
}

const books = await this.bookRepository.find({ order: { createdAt: "DESC" } });
await this.redisService.setJson(this.listCacheKey, books, this.runtimeConfig.booksCacheTtlSeconds);
```

읽기 path는 캐시를 채우고,

```ts
await this.invalidateBookCaches(saved.id);
```

쓰기 path는 캐시를 비운다. 둘이 같이 있어야 cache가 실제 정책이 된다. `RedisService`가 `ensureConnected()`와 `ping()`를 들고 있는 것도 같은 이유다. 인프라 의존성을 숨기지 않고 드러낸다.

## 실패 후 성공까지 검증한 장면

이 프로젝트에서 가장 사람 손을 많이 타는 장면은 e2e다. unit test가 아무리 통과해도, Postgres와 Redis가 없는 상태라면 제출용 검증은 완성되지 않는다.

처음 신호는 실패였다.

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test:e2e
FAIL  test/e2e/capstone.e2e.test.ts > Shippable Backend Service E2E
Error: connect ECONNREFUSED 127.0.0.1:5432
Tests  16 skipped (16)
```

이 실패가 중요한 이유는, 이 서비스의 검증이 더 이상 앱 코드만으로 끝나지 않는다는 사실을 아주 정직하게 보여 주기 때문이다. e2e 파일도 실제로 migrations, seed, Redis flush부터 시작한다.

```ts
dataSource = createAppDataSource(process.env);
await dataSource.initialize();
await dataSource.dropDatabase();
await dataSource.runMigrations();
await seedDatabase(dataSource);

redisClient = createClient({ url: process.env.REDIS_URL });
await redisClient.connect();
await redisClient.flushDb();
```

즉 이 테스트는 애플리케이션 기능 테스트가 아니라, "이 서비스가 인프라와 함께 실제로 올라와 있는가"를 보는 작은 연동 검증에 더 가깝다.

그다음 compose로 의존성을 올리고 다시 같은 검증을 돌린다.

```bash
$ docker compose up -d postgres redis
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test:e2e
Test Files  1 passed (1)
Tests       16 passed (16)
Duration    2.34s
```

재실행에서는 `/health/live`, `/health/ready`, `/docs`, register/login, login throttling, books cache population, cache invalidation, admin write, regular user `403`, invalid payload, missing book까지 모두 통과했다. 이 흐름이 중요한 이유는 단순히 "통과했다"가 아니라, 이 프로젝트의 검증이 어디까지를 서비스의 일부로 보는지 보여 주기 때문이다.

여기까지 오면 이 트랙의 마지막 문장이 자연스럽게 나온다. shippable service의 완성도는 테스트 코드 개수보다, 필요한 인프라가 준비된 상태에서 그 테스트가 끝까지 도는지로 더 정확하게 판단할 수 있다는 것. 이 프로젝트는 바로 그 기준을 한 번 실제로 끝까지 밀어 본 결과다.
