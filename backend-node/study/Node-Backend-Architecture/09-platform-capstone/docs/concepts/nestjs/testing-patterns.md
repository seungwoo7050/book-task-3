# Testing Patterns — Platform Capstone

## Overview

캡스톤 프로젝트는 5개 챕터의 모든 개념이 통합되므로, 테스트 역시 **단위 테스트**와 **E2E 테스트** 양 축으로 구성됩니다.
단위 테스트는 서비스 레이어의 비즈니스 로직을 격리 검증하고, E2E 테스트는 인증 → 인가 → CRUD → 이벤트 전체 흐름을 통합 검증합니다.

---

## 1. Unit Test — Mock 전략

### 1.1 AuthService 단위 테스트

AuthService는 3가지 외부 의존성을 가집니다:

```
AuthService
  ├── Repository<User>    — 사용자 저장/조회
  ├── JwtService          — JWT 토큰 발급
  └── EventEmitter2       — user.registered 이벤트 발행
```

모든 의존성을 `vi.fn()`으로 모킹합니다:

```typescript
const mockUserRepository = {
  findOneBy: vi.fn(),
  create: vi.fn(),
  save: vi.fn(),
};

const mockJwtService = {
  sign: vi.fn().mockReturnValue('mock-jwt-token'),
};

const mockEventEmitter = {
  emit: vi.fn(),
};
```

**핵심 테스트 케이스:**

| 테스트                         | 검증 포인트                                    |
| ------------------------------ | --------------------------------------------- |
| 회원가입 성공                   | bcrypt.hash 호출, save 호출, emit 호출          |
| 중복 사용자 거부                | ConflictException 발생                         |
| 로그인 성공                    | bcrypt.compare true, sign 호출, JWT 반환        |
| 잘못된 비밀번호                 | UnauthorizedException 발생                     |
| 존재하지 않는 사용자             | UnauthorizedException 발생                     |

### 1.2 BooksService 단위 테스트

BooksService는 2가지 외부 의존성을 가집니다:

```
BooksService
  ├── Repository<Book>    — 도서 CRUD
  └── EventEmitter2       — book.* 이벤트 발행
```

```typescript
const mockBookRepository = {
  find: vi.fn(),
  findOneBy: vi.fn(),
  create: vi.fn(),
  save: vi.fn(),
  remove: vi.fn(),
};

const mockEventEmitter = {
  emit: vi.fn(),
};
```

**핵심 테스트 케이스:**

| 테스트               | 검증 포인트                                        |
| -------------------- | ------------------------------------------------- |
| 도서 생성 + 이벤트    | save 호출 → emit('book.created', event) 확인        |
| 도서 수정 + 이벤트    | save 호출 → emit('book.updated', event) 확인        |
| 도서 삭제 + 이벤트    | remove 호출 → emit('book.deleted', event) 확인      |
| 존재하지 않는 도서     | NotFoundException 발생, emit 미호출                 |
| 전체 조회            | find 호출, 배열 반환                                |

### 1.3 이벤트 발행 검증 패턴

단위 테스트에서 이벤트 발행은 **부수효과(side effect)**이므로, 핵심 로직 완료 후 호출 여부를 검증합니다:

```typescript
// 성공 시 이벤트 발행 확인
expect(mockEventEmitter.emit).toHaveBeenCalledWith(
  'book.created',
  expect.any(BookCreatedEvent),
);

// 실패 시 이벤트 미발행 확인
expect(mockEventEmitter.emit).not.toHaveBeenCalled();
```

이 패턴은 "이벤트는 성공한 작업에 대해서만 발행된다"는 설계 원칙을 테스트로 보장합니다.

---

## 2. E2E Test — 통합 인증 흐름

### 2.1 테스트 환경 구성

E2E 테스트는 실제 NestJS 애플리케이션을 부팅하여 HTTP 요청/응답 전체 파이프라인을 검증합니다:

```typescript
beforeAll(async () => {
  const moduleFixture = await Test.createTestingModule({
    imports: [AppModule],
  }).compile();

  app = moduleFixture.createNestApplication();
  // 실제 앱과 동일한 전역 설정
  app.useGlobalPipes(new ValidationPipe({ whitelist: true }));
  app.useGlobalFilters(new HttpExceptionFilter());
  app.useGlobalInterceptors(new LoggingInterceptor(), new TransformInterceptor());
  await app.init();
});
```

**중요:** 전역 파이프, 필터, 인터셉터를 `main.ts`와 동일하게 설정해야 E2E 테스트가 프로덕션 동작을 정확히 재현합니다.

### 2.2 인증 흐름 패턴

E2E 테스트의 핵심은 **인증 토큰 획득 → 인가된 요청** 흐름입니다:

```
┌─────────────────────┐
│  1. POST /auth/register  │  ← ADMIN 사용자 생성
├─────────────────────┤
│  2. POST /auth/login     │  ← JWT 토큰 획득
├─────────────────────┤
│  3. GET/POST/PUT/DELETE  │  ← Authorization: Bearer <token>
└─────────────────────┘
```

```typescript
// beforeAll에서 ADMIN 등록 + 로그인
const registerRes = await request(app.getHttpServer())
  .post('/auth/register')
  .send({ username: 'admin', password: 'password123', role: 'ADMIN' });

const loginRes = await request(app.getHttpServer())
  .post('/auth/login')
  .send({ username: 'admin', password: 'password123' });

adminToken = loginRes.body.data.token;
```
근거: [테스트] `06-platform-capstone/solve/solution/test/e2e/capstone.e2e.test.ts` (`loginRes.body.data.token`)

### 2.3 RBAC 테스트 전략

Role-Based Access Control의 핵심 경계를 테스트합니다:

| 시나리오                          | 예상 결과 | 검증 포인트                      |
| -------------------------------- | -------- | ------------------------------- |
| 인증 없이 GET /books              | 200      | 공개 엔드포인트 접근 가능          |
| 인증 없이 POST /books             | 401      | 보호된 엔드포인트 접근 차단        |
| ADMIN 토큰으로 POST /books        | 201      | ADMIN 역할 권한 확인              |
| USER 토큰으로 POST /books         | 403      | USER 역할 권한 제한 확인          |
| ADMIN 토큰으로 PUT /books/:id     | 200      | 수정 권한 확인                   |
| ADMIN 토큰으로 DELETE /books/:id  | 204      | 삭제 권한 확인                   |

이 매트릭스는 Guard 체인의 정확한 동작을 보장합니다:

```
요청 → JwtAuthGuard (401) → RolesGuard (403) → Controller
```

### 2.4 Validation 검증

E2E 테스트에서 `ValidationPipe`의 동작을 확인합니다:

```typescript
// 필수 필드 누락 시 400 Bad Request
await request(app.getHttpServer())
  .post('/books')
  .set('Authorization', `Bearer ${adminToken}`)
  .send({ title: '' })  // author, isbn 누락
  .expect(400);
```

### 2.5 에러 응답 일관성

`HttpExceptionFilter`가 모든 에러를 일관된 형식으로 응답하는지 검증합니다:

```typescript
// 404 Not Found — 존재하지 않는 리소스
await request(app.getHttpServer())
  .get('/books/99999')
  .expect(404);
```

---

## 3. 테스트 아키텍처 요약

```
test/
├── unit/
│   ├── auth.service.test.ts     ← AuthService 격리 테스트
│   └── books.service.test.ts    ← BooksService 격리 테스트
└── e2e/
    └── capstone.e2e.test.ts     ← 전체 통합 E2E 테스트
```

### 테스트 피라미드

```
         ┌─────┐
         │ E2E │   ← 1개 파일, 12개 테스트
         │     │      인증 흐름 + RBAC + CRUD
         ├─────┤
         │Unit │   ← 2개 파일, 10개 테스트
         │     │      Service 비즈니스 로직
         └─────┘
```

| 계층       | 파일 수 | 테스트 수 | 커버리지                        |
| ---------- | ------- | -------- | ------------------------------ |
| Unit       | 2       | 10       | AuthService + BooksService     |
| E2E        | 1       | 12       | 전체 HTTP 파이프라인             |
| **합계**   | **3**   | **22**   | 서비스 로직 + 통합 흐름           |

---

## 4. Chapter별 테스트 통합 비교

| Chapter | 테스트 범위            | 캡스톤 통합                                   |
| ------- | --------------------- | -------------------------------------------- |
| 01      | CRUD 단위 테스트       | BooksService 단위 테스트로 계승                 |
| 02      | Auth 미들웨어/Guard    | E2E에서 JwtAuthGuard + RolesGuard 통합 검증     |
| 03      | Pipe/Filter/Interceptor| E2E에서 전역 설정 포함하여 검증                 |
| 04      | Repository 패턴        | 단위 테스트에서 mock Repository 사용            |
| 05      | Event 발행/수신        | 단위 테스트에서 emit 호출 검증                  |

각 챕터에서 개별적으로 테스트하던 개념이 캡스톤에서는 **하나의 E2E 흐름** 안에서 자연스럽게 통합 검증됩니다.
