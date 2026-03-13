# 09-platform-capstone development timeline

capstone이라는 이름 때문에 거대한 새 기능이 들어갔을 것 같지만, 실제 코드가 보여 주는 중심은 다르다. 이 프로젝트는 03~08에서 따로 연습한 REST, pipeline, auth, persistence, events, 운영성 규약을 하나의 NestJS 서비스로 다시 묶어 보는 통합 검증에 가깝다. 그래서 읽는 기준도 "무엇을 더했는가"보다 "어떻게 합쳐도 안 무너졌는가"가 맞다.

## 구현 순서 요약

- AppModule에서 TypeORM, EventEmitter, Auth, Books, Events를 한 프로세스에 묶는다.
- AuthService와 BooksService는 저장/발행까지만 맡기고, listener가 후속 동작을 받는다.
- 12개 e2e 시나리오로 public/auth/admin/event/validation 경계를 한 번에 확인한다.

## Phase 1

- 당시 목표: 지금까지 따로 보던 모듈을 한 AppModule 아래로 통합한다.
- 변경 단위: `nestjs/src/app.module.ts`
- 처음 가설: capstone의 첫 번째 검증은 새로운 endpoint가 아니라 "모듈 경계가 한 서비스 안에서도 그대로 유지되는가"다.
- 실제 진행: `TypeOrmModule.forRoot()`로 SQLite 영속 계층을 붙이고, `EventEmitterModule.forRoot()`, `AuthModule`, `BooksModule`, `EventsModule`을 함께 import했다.

CLI:

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run build
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test
Tests 10 passed (10)
```

검증 신호:

- build가 통과하면서 module wiring이 먼저 닫힌다.
- unit test 10개가 auth와 books service의 기본 contract를 유지한다.

핵심 코드:

```ts
imports: [
  TypeOrmModule.forRoot({ type: "better-sqlite3", database: process.env.DB_PATH || ":memory:", entities: [Book, User], synchronize: true }),
  EventEmitterModule.forRoot(),
  AuthModule,
  BooksModule,
  EventsModule,
],
```

왜 이 코드가 중요했는가:

capstone은 결국 이 import 목록이 얼마나 자연스럽게 붙는가의 문제다. 여기서 억지스러운 의존성이 생기면 이전 단계 분리가 허상이었단 뜻이 된다.

새로 배운 것:

- 통합 설계의 품질은 거대한 클래스가 아니라, 독립적으로 만들었던 모듈이 충돌 없이 나란히 설 수 있는가로 드러난다.

## Phase 2

- 당시 목표: auth, books, events가 적절한 경계에서만 만나는지 확인한다.
- 변경 단위: `nestjs/src/books/books.service.ts`, `nestjs/src/auth/auth.service.ts`, `nestjs/src/events/app-event.listener.ts`
- 처음 가설: 통합 서비스가 커져도 service는 도메인 저장과 이벤트 발행까지만 맡고, 부수효과는 listener가 가져가야 한다.
- 실제 진행: `BooksService`는 create/update/remove 뒤 book 이벤트를 발행하고, `AuthService.register()`는 user 등록 뒤 `user.registered`를 발행한다. listener는 이 이벤트를 받아 로그를 남긴다.

CLI:

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test
✓ test/unit/books.service.test.ts (5 tests)
✓ test/unit/auth.service.test.ts (5 tests)
Tests 10 passed (10)
```

검증 신호:

- books service와 auth service가 각자 5개씩 unit test를 통과한다.
- 서비스 본문에서 listener 구현 세부를 직접 알지 않는다.

핵심 코드:

```ts
this.eventEmitter.emit(
  "book.updated",
  new BookUpdatedEvent(saved.id, changes),
);
```

왜 이 코드가 중요했는가:

통합 서비스에서도 이벤트 경계가 살아 있다는 걸 보여 준다. capstone이 서비스 본문을 거대하게 만드는 대신, 기존 event boundary를 유지한다는 신호다.

새로 배운 것:

- 모듈 통합이 잘 된다는 건 의존성이 많아져도 책임 위치가 뒤섞이지 않는다는 뜻이다.

## Phase 3

- 당시 목표: public/auth/admin/event/validation/missing resource 경계를 단일 서비스 e2e로 재검증한다.
- 변경 단위: `nestjs/test/e2e/capstone.e2e.test.ts`
- 처음 가설: capstone의 진짜 산출물은 코드보다 재검증 경로다. 이 경로가 길고 자연스러워야 통합이 성공한 것이다.
- 실제 진행: admin 사용자 생성과 로그인으로 token을 준비하고, register/login/public GET /books/protected POST PUT DELETE /books/regular user 403/invalid body 400/missing book 404를 모두 통과하게 했다.

CLI:

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test:e2e
[Event] Book updated: id=..., changes=[price]
[Event] Book deleted: id=...
[Event] User registered: regularuser ...
✓ test/e2e/capstone.e2e.test.ts (12 tests)
Tests 12 passed (12)
```

검증 신호:

- public route와 protected route가 같은 앱 안에서 공존한다.
- event log가 auth/books 흐름과 함께 실제로 출력된다.

핵심 코드:

```ts
const res = await request(app.getHttpServer())
  .post("/books")
  .set("Authorization", `Bearer ${userToken}`)
  .send(validBook);

expect(res.status).toBe(403);
```

왜 이 코드가 중요했는가:

capstone의 통합 품질은 admin happy path보다 role boundary를 잃지 않는 데서 더 잘 드러난다. 모든 걸 한 서비스로 합쳤는데도 403이 정확히 살아 있어야 한다.

새로 배운 것:

- 통합 서비스 설계는 "다 되게 만들기"보다 "되면 안 되는 것도 계속 안 되게 만들기"가 더 어렵고 중요하다.

다음:

- [`../10-shippable-backend-service/00-series-map.md`](../10-shippable-backend-service/00-series-map.md)에서 이 통합판을 Postgres, Redis, Swagger, Compose가 있는 제출용 surface로 다시 포장한다.
