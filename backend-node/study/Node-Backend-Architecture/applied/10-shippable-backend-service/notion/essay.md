# 제출할 수 있는 백엔드 — 포트폴리오 수준의 서비스를 만들기까지

## 프롤로그: 학습용 코드와 제출용 서비스의 사이

프로젝트 09까지 만든 것은 학습 목적의 캡스톤이었다. 기능은 완전하지만, 실제 채용 과정에서 제출하기에는 몇 가지가 부족하다. SQLite는 로컬에서만 작동하고, 캐시가 없어서 매번 DB를 조회하며, API 문서가 코드 안에만 있고 Swagger가 없다. "동작하는 학습 프로젝트"와 "재현 가능한 포트폴리오 서비스"의 간극을 메우는 것이 이 프로젝트의 목적이다.

---

## 1. SQLite에서 Postgres로 — 왜 바꾸는가

### synchronize: true의 한계

프로젝트 06부터 09까지 TypeORM의 `synchronize: true`를 사용했다. 엔티티가 바뀌면 자동으로 스키마를 동기화했다. 편리하지만 위험했다. 컬럼을 삭제하면 데이터도 사라진다. 프로덕션에서는 절대 쓸 수 없다.

이 프로젝트에서는 `synchronize: false`로 바꾸고, 대신 마이그레이션 스크립트를 작성한다.

### 마이그레이션 — 스키마의 버전 관리

`1710000000000-initial-schema.ts` 파일이 첫 번째 마이그레이션이다. `up` 메서드에서 `CREATE TABLE "users"`와 `CREATE TABLE "books"`를 실행하고, `down` 메서드에서 `DROP TABLE`을 실행한다.

```typescript
await queryRunner.query('CREATE EXTENSION IF NOT EXISTS "pgcrypto"');
await queryRunner.query(`
  CREATE TABLE "users" (
    "id" uuid NOT NULL DEFAULT gen_random_uuid(),
    ...
  )
`);
```

`pgcrypto` 확장을 활성화하는 것은 Postgres 고유의 작업이다. `gen_random_uuid()`를 사용하기 위해서다. SQLite에서는 이런 확장이 불가능했다.

마이그레이션 파일 이름의 숫자(`1710000000000`)는 타임스탬프다. TypeORM이 이 순서대로 마이그레이션을 실행한다. 팀에서 여러 개발자가 동시에 마이그레이션을 만들더라도, 타임스탬프 순서가 실행 순서를 보장한다.

### 데이터 타입의 변화

SQLite에서는 `"text"` 타입이 대부분이었다. Postgres에서는 타입이 세분화된다:
- `uuid` — UUID 전용 타입, 인덱스 성능 최적화
- `character varying(200)` — 길이 제한 있는 문자열
- `TIMESTAMPTZ` — 타임존을 포함하는 타임스탬프
- `double precision` — 부동소수점

이 차이가 드러나는 것은 SQLite가 사실 타입에 관대한 데이터베이스였기 때문이다. Postgres는 타입을 엄격하게 검사한다.

---

## 2. Docker Compose — 로컬 인프라의 재현

### 세 개의 서비스

```yaml
services:
  postgres:   # 데이터베이스
  redis:      # 캐시 + 쓰로틀링
  app:        # NestJS 애플리케이션
```

`postgres`와 `redis`는 공식 Alpine 이미지를 사용한다. `app`은 NestJS 프로젝트의 Dockerfile로 빌드한다.

`depends_on`에 `condition: service_healthy`가 있다. Postgres의 `pg_isready`와 Redis의 `redis-cli ping`이 healthcheck다. 이것이 확인되어야 app 컨테이너가 시작한다. 이전 프로젝트의 health/ready 개념이 인프라 수준에서 적용된 것이다.

### 환경변수

`docker-compose.yml`의 `app.environment`에 모든 설정이 선언되어 있다:

```yaml
DATABASE_URL: postgres://backend:backend@postgres:5432/shippable_backend
REDIS_URL: redis://redis:6379
JWT_SECRET: compose-secret
LOGIN_THROTTLE_MAX_ATTEMPTS: 5
BOOKS_CACHE_TTL_SECONDS: 30
```

프로젝트 08에서 `PORT`, `READY`, `LOG_LEVEL`만 있던 config가 12개로 확장되었다. `loadRuntimeConfig`의 fail-fast 패턴은 동일하지만, `JWT_SECRET`, `DATABASE_URL`, `REDIS_URL`은 필수(없으면 시작 거부)다. 이것이 프로덕션 config의 현실이다.

---

## 3. Redis — 두 가지 역할

### 3-1. Books 캐시

`BooksService.findAll()`은 먼저 Redis에서 `books:list` 키를 조회한다. 캐시가 있으면 DB를 건너뛴다.

```typescript
async findAll(): Promise<Book[]> {
  const cached = await this.redisService.getJson<Book[]>(this.listCacheKey);
  if (cached) return cached;
  
  const books = await this.bookRepository.find(...);
  await this.redisService.setJson(this.listCacheKey, books, this.runtimeConfig.booksCacheTtlSeconds);
  return books;
}
```

`findOne`도 `books:detail:{id}` 키로 개별 책을 캐시한다.

쓰기 연산(create, update, remove) 후에는 `invalidateBookCaches`를 호출하여 해당 캐시를 삭제한다. 이것이 **캐시 무효화(cache invalidation)** 전략이다. 데이터가 변경되면 오래된 캐시를 제거하여 다음 조회 시 DB에서 최신 데이터를 가져오게 한다.

TTL(`booksCacheTtlSeconds`)도 있다. 캐시 무효화가 실패하더라도 TTL이 지나면 캐시가 자연 소멸한다. 이중 안전장치.

### 3-2. 로그인 쓰로틀링

`AuthRateLimitService`는 로그인 실패 횟수를 Redis에 기록한다.

```typescript
async ensureLoginAllowed(clientId: string): Promise<void> {
  const attempts = await this.redisService.getJson<number>(this.getKey(clientId));
  if (attempts !== null && attempts >= this.runtimeConfig.loginThrottleMaxAttempts) {
    throw new HttpException("Too many login attempts", HttpStatus.TOO_MANY_REQUESTS);
  }
}
```

키는 `auth:login:{clientId}`. 실패할 때마다 카운터가 증가하고, TTL(`loginThrottleWindowSeconds`, 기본 60초) 후 자동 리셋된다. 성공 시 카운터를 즉시 삭제한다.

프로젝트 09에서는 이 보호 장치가 없었다. 무차별 대입 공격(brute force)을 막을 방법이 없었다. Redis 기반 쓰로틀링은 이 gap을 메운다.

### RedisService의 방어적 코딩

`RedisService`의 모든 메서드는 `ensureConnected()`를 먼저 호출한다. Redis 연결이 끊어져도 앱이 죽지 않는다. 캐시가 작동하지 않을 뿐, 요청은 DB 직접 조회로 폴백한다. Redis는 "있으면 좋고, 없어도 앱은 살아남는" 보조 인프라다.

---

## 4. Health Check의 진화

프로젝트 08에서는 `/health`와 `/ready` 두 엔드포인트였다. 프로젝트 10에서는:

- `GET /health/live` — 프로세스 생존 확인. 항상 `{ status: "ok" }`.
- `GET /health/ready` — Postgres `SELECT 1` + Redis `PING` 성공 여부. 둘 다 성공하면 200, 하나라도 실패하면 503.

```typescript
const databaseReady = await this.dataSource.query("SELECT 1");
const redisReady = await this.redisService.isReady();
```

프로젝트 08의 `READY` 환경변수 기반 readiness가 실제 인프라 상태 점검으로 바뀌었다. `READY=true`라고 선언하는 것이 아니라, 실제로 DB와 Redis에 연결할 수 있는지를 확인한다.

---

## 5. Swagger — 코드에서 자동 생성되는 API 문서

`app.bootstrap.ts`에서 `SwaggerModule`을 설정한다:

```typescript
const swaggerConfig = new DocumentBuilder()
  .setTitle("Shippable Backend Service")
  .addBearerAuth()
  .build();
SwaggerModule.setup("docs", app, swaggerDocument);
```

`GET /docs`에서 Swagger UI를 확인할 수 있다. Controller의 데코레이터와 DTO의 class-validator 데코레이터에서 API 스펙을 자동 추출한다.

`.addBearerAuth()`로 JWT 인증 헤더를 Swagger UI에서 직접 입력하고 테스트할 수 있다.

---

## 6. RuntimeModule — Global 모듈

```typescript
@Global()
@Module({
  providers: [RUNTIME_CONFIG, RuntimeConfigService, RedisService],
  exports: [RuntimeConfigService, RedisService],
})
export class RuntimeModule {}
```

`@Global()` 데코레이터로 선언된 이 모듈은 다른 모듈에서 별도 import 없이 `RuntimeConfigService`와 `RedisService`를 주입받을 수 있다. Books가 Redis 캐시를 쓰고, Auth가 Redis 쓰로틀링을 쓰고, Health가 Redis 상태를 확인하는 — 모든 곳에서 같은 Redis 인스턴스를 공유한다.

---

## 7. Seed 스크립트 — 초기 데이터

마이그레이션이 스키마를 만들고, seed 스크립트가 초기 데이터를 넣는다.

- admin 유저 (username: "admin", password: bcrypt hash of "admin123", role: ADMIN)
- 샘플 책 2권

seed는 멱등적이다. 이미 admin이 있으면 건너뛴다. 이미 책이 있으면 건너뛴다. 여러 번 실행해도 안전하다.

---

## 8. 09와 10의 대조

| 관점 | 09-platform-capstone | 10-shippable-backend-service |
|------|---------------------|------------------------------|
| DB | SQLite (better-sqlite3) | Postgres (pg) |
| 스키마 관리 | `synchronize: true` | Migration 스크립트 |
| 캐시 | 없음 | Redis (`books:list`, `books:detail:*`) |
| 로그인 보호 | 없음 | Redis 기반 쓰로틀링 |
| Health Check | 없음 | `/health/live`, `/health/ready` (DB+Redis 상태) |
| API 문서 | 없음 | Swagger (`/docs`) |
| 인프라 | 없음 (단일 프로세스) | Docker Compose (3 서비스) |
| 초기 데이터 | 테스트에서만 | Seed 스크립트 (`pnpm run db:seed`) |
| Config 필수값 | `DB_PATH` (선택) | `JWT_SECRET`, `DATABASE_URL`, `REDIS_URL` (필수) |
| 설정 관리 | `process.env` 직접 | `.env` 파일 + `dotenv` |
| 목적 | 학습용 통합 | 채용 제출용 포트폴리오 |

---

## 에필로그: 재현 가능성이라는 가치

이 프로젝트의 최종 목표는 "누구나 `docker compose up -d`와 `.env.example`만으로 전체 서비스를 재현할 수 있는 상태"다. 클라우드 배포는 다음 단계로 남겨두었다.

README의 "빠른 실행 방법" 7줄을 따라 하면 Postgres에 테이블이 생기고, Redis가 연결되고, Swagger에서 API를 테스트할 수 있다. 이 7줄이 프로젝트 00부터 10까지 쌓아온 모든 지식의 집약이다. TypeScript의 타입 시스템, Node.js의 런타임, HTTP의 원리, Express와 NestJS의 패턴, 인증, 영속, 이벤트, 운영 인프라 — 그 모든 것이 이 한 서비스 안에 녹아 있다.
