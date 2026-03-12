# Project 10 — Shippable Backend Service 개발 타임라인

## Phase 1: Postgres 전환과 Docker Compose 환경 구축

### 1-1. Docker Compose 작성

```bash
# docker-compose.yml 생성
# postgres:16-alpine, redis:7-alpine 공식 이미지 선택

docker compose up -d postgres redis
docker compose ps    # 두 서비스 healthy 상태 확인
```

Postgres 컨테이너 설정:
```yaml
environment:
  POSTGRES_USER: backend
  POSTGRES_PASSWORD: backend
  POSTGRES_DB: shippable_backend
ports:
  - "5432:5432"
healthcheck:
  test: ["CMD-SHELL", "pg_isready -U backend"]
```

Redis 컨테이너 설정:
```yaml
ports:
  - "6379:6379"
healthcheck:
  test: ["CMD", "redis-cli", "ping"]
```

app 서비스의 `depends_on`에 `condition: service_healthy`를 넣어 DB, Redis가 준비된 후에만 앱이 시작하도록 설정.

### 1-2. 패키지 설치

```bash
cd nestjs
pnpm add pg                    # Postgres 드라이버
pnpm add redis                 # Redis 클라이언트 (node-redis v4)
pnpm add @nestjs/swagger swagger-ui-express   # Swagger UI
pnpm add dotenv                # .env 파일 로드
pnpm add -D ts-node tsconfig-paths  # 마이그레이션 스크립트 실행용
```

`better-sqlite3`와 `@types/better-sqlite3`는 제거하지 않지만, 이 프로젝트에서는 사용하지 않는다.

### 1-3. .env 파일 구성

```bash
# .env.example 생성 — Git에 커밋
cat > .env.example << 'EOF'
PORT=3000
JWT_SECRET=change-me
DATABASE_URL=postgres://backend:backend@localhost:5432/shippable_backend
REDIS_URL=redis://localhost:6379
LOGIN_THROTTLE_MAX_ATTEMPTS=5
LOGIN_THROTTLE_WINDOW_SECONDS=60
BOOKS_CACHE_TTL_SECONDS=30
EOF

# .env 생성 — .gitignore에 추가
cp .env.example .env
# JWT_SECRET 등 실제 값 수정
```

`.gitignore`에 `.env` 추가하여 시크릿이 커밋되지 않도록 한다.

---

## Phase 2: TypeORM 마이그레이션 체계 구축

### 2-1. DataSource 설정 변경

```typescript
// src/database/database-options.ts
// 기존: type: "better-sqlite3", synchronize: true
// 변경: type: "postgres", synchronize: false, migrations: [InitialSchema1710000000000]
```

`synchronize: false`로 전환하는 순간부터 엔티티를 바꿔도 테이블이 자동으로 변경되지 않는다. 모든 스키마 변경은 마이그레이션을 통해야 한다.

### 2-2. 마이그레이션 파일 작성

```bash
# src/database/migrations/1710000000000-initial-schema.ts 직접 작성
# TypeORM CLI의 generate 대신 수동 작성 선택 — 정확한 제어를 위해
```

마이그레이션 내용:
```sql
-- up
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE TABLE "users" (
  "id" uuid NOT NULL DEFAULT gen_random_uuid(),
  "username" character varying(100) NOT NULL,
  "password" character varying(200) NOT NULL,
  "role" character varying(20) NOT NULL DEFAULT 'USER',
  "createdAt" TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT "PK_users" PRIMARY KEY ("id"),
  CONSTRAINT "UQ_users_username" UNIQUE ("username")
);

CREATE TABLE "books" (
  "id" uuid NOT NULL DEFAULT gen_random_uuid(),
  "title" character varying(200) NOT NULL,
  "author" character varying(200) NOT NULL,
  "price" double precision NOT NULL,
  "createdAt" TIMESTAMPTZ NOT NULL DEFAULT now(),
  "updatedAt" TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT "PK_books" PRIMARY KEY ("id")
);

-- down
DROP TABLE "books";
DROP TABLE "users";
DROP EXTENSION IF EXISTS "pgcrypto";
```

### 2-3. 마이그레이션 실행 스크립트

```bash
# package.json에 스크립트 추가
# "db:migrate": "ts-node -r tsconfig-paths/register src/database/scripts/migrate.ts"
# "db:seed": "ts-node -r tsconfig-paths/register src/database/scripts/seed.ts"

# 마이그레이션 실행
pnpm run db:migrate
# 출력: DataSource initialized / Migrations executed / DataSource destroyed
```

`scripts/migrate.ts`는 DataSource를 초기화하고, `runMigrations()`를 호출하고, DataSource를 종료한다. 앱 프로세스와 별개로 실행되는 독립 스크립트.

### 2-4. 시드 데이터

```bash
pnpm run db:seed
# 출력: admin 유저 생성 / 샘플 책 2권 생성 (또는 이미 존재하면 건너뜀)
```

`seed-data.ts`의 `seedDatabase`는 멱등적:
```typescript
const existingAdmin = await userRepo.findOne({ where: { username: "admin" } });
if (!existingAdmin) {
  // bcrypt hash로 password 생성 후 저장
}
```

---

## Phase 3: Redis 통합

### 3-1. RedisService 구현

```bash
# src/runtime/redis.service.ts 작성
# node-redis v4의 createClient 사용
# REDIS_URL 환경변수에서 연결 정보 획득
```

OnModuleInit에서 연결, OnModuleDestroy에서 종료. 라이프사이클 훅을 통한 자원 관리.

### 3-2. 캐시 적용

```bash
# src/books/books.service.ts 수정
# findAll → books:list 키 캐시
# findOne → books:detail:{id} 키 캐시
# create/update/remove → invalidateBookCaches() 호출
```

캐시 동작 검증:
```bash
# Redis CLI로 직접 확인
docker exec -it <redis-container> redis-cli
> KEYS books:*
> GET books:list
> TTL books:list
```

### 3-3. 로그인 쓰로틀링

```bash
# src/auth/auth-rate-limit.service.ts 작성
# auth:login:{clientId} 키로 실패 횟수 추적
# loginThrottleWindowSeconds 후 자동 만료 (Redis TTL)
```

검증:
```bash
# 5회 연속 잘못된 비밀번호로 로그인 시도 → 429 Too Many Requests
# 60초 후 자동 해제 (또는 정상 로그인 시 즉시 해제)
```

---

## Phase 4: RuntimeModule과 Config 확장

### 4-1. RuntimeConfig 확장

```bash
# src/runtime/runtime-config.ts 수정
# 기존 (08): PORT, READY, LOG_LEVEL
# 추가: DATABASE_URL (필수), REDIS_URL (필수), JWT_SECRET (필수),
#       LOGIN_THROTTLE_MAX_ATTEMPTS, LOGIN_THROTTLE_WINDOW_SECONDS,
#       BOOKS_CACHE_TTL_SECONDS
```

필수 환경변수 누락 시 즉시 에러 (fail-fast):
```
Error: missing required env var JWT_SECRET
```

### 4-2. Global 모듈화

```bash
# src/runtime/runtime.module.ts 작성 — @Global() 데코레이터
# RuntimeConfigService + RedisService를 전역 공유
# 다른 모듈에서 imports 없이 주입 가능
```

---

## Phase 5: Health Check와 Swagger

### 5-1. Health 엔드포인트

```bash
# src/health.controller.ts 수정
# /health/live → 항상 200
# /health/ready → DB SELECT 1 + Redis PING, 하나라도 실패 시 503
```

검증:
```bash
# Postgres 중지 후
docker compose stop postgres
curl http://localhost:3000/health/ready
# → 503 Service Unavailable

docker compose start postgres
# 잠시 대기 후
curl http://localhost:3000/health/ready
# → 200 OK, { "status": "ok", "database": true, "redis": true }
```

### 5-2. Swagger 설정

```bash
# src/app.bootstrap.ts에 SwaggerModule 추가
# DocumentBuilder로 제목, 버전, Bearer 인증 설정
# /docs 경로에 Swagger UI 마운트
```

검증:
```bash
curl http://localhost:3000/docs     # Swagger UI HTML
curl http://localhost:3000/docs-json  # OpenAPI JSON 스펙
```

브라우저에서 `/docs`에 접속하여 모든 엔드포인트 확인 및 인증 후 API 테스트 가능.

---

## Phase 6: 전체 통합 실행 절차

### 최종 실행 흐름

```bash
# 1. 환경 변수 준비
cp .env.example .env
# JWT_SECRET 등 수정

# 2. 인프라 기동
docker compose up -d postgres redis

# 3. 마이그레이션
pnpm run db:migrate

# 4. 시드 데이터
pnpm run db:seed

# 5. 앱 실행
pnpm run start:dev

# 6. 확인
curl http://localhost:3000/health/live    # { "status": "ok" }
curl http://localhost:3000/health/ready   # { "status": "ok", "database": true, "redis": true }
# 브라우저에서 http://localhost:3000/docs → Swagger UI
```

### Docker Compose로 전체 실행

```bash
# 앱까지 포함해서 한 번에
docker compose up -d
# → postgres 헬스체크 통과 → redis 헬스체크 통과 → app 시작
```

---

## Phase 7: 테스트

### E2E 테스트 환경

```bash
pnpm test        # 유닛 테스트 (mock 기반)
pnpm test:e2e    # E2E 테스트 (실제 DB/Redis 필요)
```

E2E 테스트는 실제 Postgres와 Redis 연결이 필요. CI/CD에서는 GitHub Actions의 service containers로:
```yaml
services:
  postgres:
    image: postgres:16-alpine
    env:
      POSTGRES_USER: test
      POSTGRES_DB: test_db
  redis:
    image: redis:7-alpine
```

### 전체 서비스 중지

```bash
docker compose down           # 컨테이너 중지 + 제거
docker compose down -v        # 볼륨까지 삭제 (DB 데이터 초기화)
```

---

## Phase 8: Git 관리

```bash
# .gitignore 확인
echo ".env" >> .gitignore     # 시크릿 제외
echo "dist/" >> .gitignore    # 빌드 산출물 제외

git add .
git commit -m "feat: shippable backend with Postgres, Redis, Swagger"
```

`.env.example`은 커밋하여 다른 개발자(면접관 포함)가 필요한 환경 변수를 알 수 있게 한다.
