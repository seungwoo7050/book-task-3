# 09-platform-capstone — 개발 타임라인

> 소스 코드에 남지 않는 개발 과정을 시간순으로 기록한다.

---

## Phase 1: 프로젝트 초기화와 의존성 통합

### 1-1. NestJS 프로젝트 설정

```bash
cd 09-platform-capstone/nestjs
pnpm init
```

이전 프로젝트들의 의존성을 하나로 합친다:

```bash
# 프레임워크 코어
pnpm add @nestjs/common @nestjs/core @nestjs/platform-express reflect-metadata rxjs

# TypeORM + SQLite (from 06)
pnpm add @nestjs/typeorm typeorm better-sqlite3

# Auth (from 05)
pnpm add @nestjs/jwt @nestjs/passport passport passport-jwt bcryptjs

# Events (from 07)
pnpm add @nestjs/event-emitter

# Validation (from 04)
pnpm add class-validator class-transformer @nestjs/mapped-types

# Dev
pnpm add -D @nestjs/cli @nestjs/testing typescript @types/node @types/express @types/supertest @types/bcryptjs @types/passport-jwt supertest vitest
```

### 1-2. better-sqlite3 native 빌드

```bash
pnpm install
pnpm approve-builds
pnpm rebuild better-sqlite3
```

---

## Phase 2: 디렉토리 구조 설계

```bash
src/
├── auth/               # 05에서 가져온 인증·인가
│   ├── decorators/     # @Roles, @CurrentUser
│   ├── dto/            # RegisterDto, LoginDto
│   ├── entities/       # User entity
│   ├── guards/         # JwtAuthGuard, RolesGuard
│   ├── strategies/     # JwtStrategy
│   ├── auth.controller.ts
│   ├── auth.module.ts
│   └── auth.service.ts
├── books/              # 03+04에서 가져온 CRUD
│   ├── dto/
│   ├── entities/
│   ├── books.controller.ts
│   ├── books.module.ts
│   └── books.service.ts
├── common/             # 04에서 가져온 파이프라인
│   ├── filters/
│   └── interceptors/
├── events/             # 07에서 가져온 이벤트
│   ├── app-event.listener.ts
│   ├── events.module.ts
│   └── events.ts
├── app.module.ts
└── main.ts
```

---

## Phase 3: 모듈별 통합 과정

### 3-1. Auth 모듈 통합

05-auth-and-authorization에서 가져온 파일들:

- `entities/user.entity.ts` — `Role` enum 추가 (`USER`, `ADMIN`)
- `auth.service.ts` — register, login 로직
- `guards/jwt-auth.guard.ts`, `guards/roles.guard.ts`
- `strategies/jwt.strategy.ts`
- `decorators/roles.decorator.ts`, `decorators/current-user.decorator.ts`
- `dto/register.dto.ts`, `dto/login.dto.ts`
- `auth.controller.ts`, `auth.module.ts`

`AuthModule`에서 `JwtModule.register()`와 `PassportModule` 설정:

```typescript
JwtModule.register({
  secret: process.env.JWT_SECRET || "super-secret",
  signOptions: { expiresIn: "1h" },
})
```

### 3-2. Books 모듈 통합

06-persistence에서 Book 엔티티와 CRUD 로직을 가져오고, 05의 Guard를 연결:

- `@UseGuards(JwtAuthGuard, RolesGuard)` + `@Roles(Role.ADMIN)` — POST, PUT, DELETE에 적용
- GET은 Guard 없음 — 공개 API

### 3-3. Events 모듈 확장

07-domain-events에서 가져온 이벤트에 `UserRegisteredEvent` 추가:

```
events.ts → BookCreatedEvent, BookUpdatedEvent, BookDeletedEvent, UserRegisteredEvent
```

`BookEventListener` → `AppEventListener`로 이름 변경:
- Book 이벤트 3개 + User 이벤트 1개 수신

`AuthService.register()`에 이벤트 발행 추가:

```typescript
this.eventEmitter.emit("user.registered", new UserRegisteredEvent(...));
```

### 3-4. Common 모듈 (Pipeline)

04-request-pipeline에서 가져온 공통 인프라:

- `HttpExceptionFilter` — 전역 예외 필터
- `TransformInterceptor` — 응답 래핑 (`{ success, data }`)
- `LoggingInterceptor` — 요청 로깅

### 3-5. AppModule 조립

```typescript
imports: [
  TypeOrmModule.forRoot({ entities: [Book, User], synchronize: true }),
  EventEmitterModule.forRoot(),
  AuthModule,
  BooksModule,
  EventsModule,
]
```

`entities` 배열에 `Book`과 `User` 모두 등록. 하나의 SQLite 파일에 두 테이블.

---

## Phase 4: 교차 기능 검증

### 4-1. RBAC + CRUD 통합 테스트

```bash
# 서버 실행
pnpm run start

# 1. Admin 등록
curl -X POST http://localhost:3000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123","role":"ADMIN"}'

# 2. Admin 로그인 → JWT 토큰 획득
curl -X POST http://localhost:3000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
# 응답에서 token 복사

# 3. 토큰으로 책 생성
curl -X POST http://localhost:3000/books \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"title":"Clean Code","author":"Robert C. Martin","publishedYear":2008,"genre":"Programming","price":33.99}'

# 4. 토큰 없이 책 생성 → 401
curl -X POST http://localhost:3000/books \
  -H "Content-Type: application/json" \
  -d '{"title":"Fail","author":"None","publishedYear":2024,"genre":"Test","price":9.99}'

# 5. 일반 유저로 책 생성 → 403
# (일반 유저 등록 + 로그인 후 토큰으로 시도)
```

### 4-2. 이벤트 발행 확인

서버 콘솔에서 다음 로그가 출력되는지 확인:

```
[Event] User registered: admin (role=ADMIN, id=xxx)
[Event] Book created: "Clean Code" by Robert C. Martin (id=xxx)
```

---

## Phase 5: 테스트 작성

### 5-1. 단위 테스트

`test/unit/auth.service.test.ts`:
```bash
pnpm run test
```
- AuthService의 register/login 로직 검증
- bcrypt 해싱 동작 확인
- 중복 username 거부 검증

`test/unit/books.service.test.ts`:
- BooksService CRUD 동작 검증

### 5-2. 캡스톤 E2E 테스트

`test/e2e/capstone.e2e.test.ts`:

```bash
pnpm run test:e2e
```

**`beforeAll` 사용** — `beforeEach`가 아닌 `beforeAll`로 앱을 한 번만 초기화. 데이터가 테스트 간에 누적되는 것을 허용하여 통합 시나리오를 현실적으로 검증.

테스트 시나리오:
1. Admin 계정 등록 → 로그인 → JWT 토큰 획득
2. 일반 유저 등록 성공
3. 중복 username 등록 거부 (409)
4. 로그인 성공/실패
5. `GET /books` 공개 접근
6. `POST /books` 무인증 시 401
7. Admin으로 책 생성/수정/삭제
8. 일반 유저로 책 생성 시 403
9. 잘못된 body 시 400
10. 존재하지 않는 책 조회 시 404

---

## Phase 6: 빌드 및 최종 검증

```bash
cd nestjs/
pnpm install
pnpm approve-builds
pnpm rebuild better-sqlite3
pnpm run build
pnpm run test
pnpm run test:e2e
```

---

## 도구 및 커맨드 요약

| 도구/커맨드 | 용도 |
|-------------|------|
| `pnpm install` | 통합 의존성 설치 |
| `pnpm approve-builds` | better-sqlite3 native 빌드 승인 |
| `pnpm rebuild better-sqlite3` | C++ 바인딩 컴파일 |
| `pnpm run build` | nest build |
| `pnpm run test` | 단위 테스트 (Vitest) |
| `pnpm run test:e2e` | 캡스톤 E2E 테스트 |
| `curl` | 수동 API 통합 검증 |
| `JWT_SECRET` 환경변수 | JWT 서명 키 (기본: "super-secret") |
| `DB_PATH` 환경변수 | SQLite 파일 경로 (기본: ":memory:") |

## 핵심 파일 생성 순서

```
auth/entities/user.entity.ts → auth/dto/ → auth/strategies/ → auth/guards/ → auth/decorators/
→ auth/auth.service.ts → auth/auth.controller.ts → auth/auth.module.ts
→ books/ (06에서 이관, Controller에 Guard 추가)
→ events/events.ts (UserRegisteredEvent 추가) → events/app-event.listener.ts → events/events.module.ts
→ common/filters/ + common/interceptors/ (04에서 이관)
→ app.module.ts → main.ts
→ test/unit/ → test/e2e/capstone.e2e.test.ts
```

## 통합 시 주의한 점

1. **Guard import 경로**: `BooksController`에서 `../auth/guards/`로 Auth 모듈의 Guard를 직접 import
2. **Entity 배열**: `TypeOrmModule.forRoot()`의 `entities`에 `Book`과 `User` 모두 포함
3. **EventsModule export**: `AppEventListener`를 export하여 다른 모듈에서 접근 가능
4. **환경변수 기본값**: `JWT_SECRET`과 `DB_PATH` 모두 기본값 제공 → 개발 환경에서 설정 없이 시작 가능
