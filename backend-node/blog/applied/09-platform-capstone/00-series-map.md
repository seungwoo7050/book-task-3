# 09-platform-capstone series map

이 capstone은 새 장난감을 많이 추가하는 프로젝트가 아니다. `AppModule` 안에 auth, books, events, TypeORM, JWT, 공통 filter/interceptor를 한 번에 올려 두고, 이전 장에서 따로 검증하던 계약이 단일 NestJS 서비스 안에서도 유지되는지 확인하는 통합 실험에 가깝다.

처음 읽을 때는 `main.ts`와 `app.module.ts`로 앱 껍질을 잡고, `AuthService`와 `BooksService`에서 실제 책임이 어떻게 이어지는지 본 뒤, `capstone.e2e.test.ts`와 수동 HTTP 재실행으로 통합 결과를 닫는 순서가 가장 자연스럽다. 이렇게 읽으면 "기능 목록"보다 "계약을 어디까지 다시 고정했는가"가 먼저 보인다.

## 이 글에서 볼 것

- 단일 NestJS 앱이 `ValidationPipe -> Guards -> Controller -> Service -> Repository -> EventEmitter2` 흐름을 어떻게 한 줄로 묶는지
- `GET /books`는 공개, `POST/PUT/DELETE /books`는 `ADMIN`만 허용하는 단순 RBAC가 실제 코드와 응답 표면에서 어떻게 드러나는지
- 성공 응답은 `TransformInterceptor`, 실패 응답은 `HttpExceptionFilter`가 감싸지만, request 로그는 성공 요청 위주로만 남는 현재 한계가 무엇인지
- canonical problem에 들어 있는 native SQLite recovery와 기본 e2e가 실제로 잠그는 범위가 어디서 갈라지는지
- e2e가 single app + shared `:memory:` DB 위에서 순차적으로 시나리오를 쌓는 통합 검증이라는 점까지 포함해 읽어야 한다

## source of truth

- `applied/09-platform-capstone/README.md`
- `applied/09-platform-capstone/problem/README.md`
- `applied/09-platform-capstone/nestjs/src/app.module.ts`
- `applied/09-platform-capstone/nestjs/src/main.ts`
- `applied/09-platform-capstone/nestjs/src/auth/auth.controller.ts`
- `applied/09-platform-capstone/nestjs/src/auth/auth.service.ts`
- `applied/09-platform-capstone/nestjs/src/auth/guards/jwt-auth.guard.ts`
- `applied/09-platform-capstone/nestjs/src/auth/guards/roles.guard.ts`
- `applied/09-platform-capstone/nestjs/src/auth/strategies/jwt.strategy.ts`
- `applied/09-platform-capstone/nestjs/src/books/books.controller.ts`
- `applied/09-platform-capstone/nestjs/src/books/books.service.ts`
- `applied/09-platform-capstone/nestjs/src/common/filters/http-exception.filter.ts`
- `applied/09-platform-capstone/nestjs/src/common/interceptors/logging.interceptor.ts`
- `applied/09-platform-capstone/nestjs/src/common/interceptors/transform.interceptor.ts`
- `applied/09-platform-capstone/nestjs/src/events/app-event.listener.ts`
- `applied/09-platform-capstone/nestjs/src/events/events.ts`
- `applied/09-platform-capstone/nestjs/test/unit/auth.service.test.ts`
- `applied/09-platform-capstone/nestjs/test/unit/books.service.test.ts`
- `applied/09-platform-capstone/nestjs/test/e2e/capstone.e2e.test.ts`

## 구현 흐름 한눈에 보기

1. `AppModule`이 `better-sqlite3` 기반 TypeORM, `EventEmitterModule`, `AuthModule`, `BooksModule`, `EventsModule`을 한 앱으로 조합한다.
2. `main.ts`가 전역 `ValidationPipe`, `HttpExceptionFilter`, `LoggingInterceptor`, `TransformInterceptor`를 설치해 공통 HTTP 표면을 고정한다.
3. `AuthService`는 `register -> bcrypt.hash -> save -> user.registered emit`, `login -> bcrypt.compare -> jwt.sign` 흐름을 맡는다.
4. `BooksService`는 공개 read와 관리자 write를 나누고, save/remove 성공 뒤에만 `book.created/updated/deleted` 이벤트를 발행한다.
5. e2e와 수동 `curl` 재실행으로 `401/403/400/404`와 성공 응답 envelope를 다시 확인한다.

## 대표 검증

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run build
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test:e2e
✓ test/unit/auth.service.test.ts (5 tests)
✓ test/unit/books.service.test.ts (5 tests)
✓ test/e2e/capstone.e2e.test.ts (12 tests)
```

```bash
$ curl -s http://localhost:3123/books
{"success":true,"data":[]}

$ curl -s -o - -w '\n%{http_code}\n' -X POST http://localhost:3123/books \
  -H 'Content-Type: application/json' \
  -d '{"title":"Clean Code","author":"Robert C. Martin","publishedYear":2008,"genre":"Programming","price":33.99}'
{"success":false,"error":{"status":401,"message":"Unauthorized"}}
401
```

## 지금 시점의 한계

- 토큰은 `accessToken`이 아니라 `token` 필드 하나만 반환한다.
- 책 리소스에는 소유권, pagination, soft delete, audit trail이 없다.
- `LoggingInterceptor`는 `tap(() => ...)`만 써서 성공 요청은 로그에 남지만, 수동 재실행 기준 `401/403/400/404`는 같은 형식의 request 로그가 남지 않는다.
- e2e는 `TransformInterceptor`와 `HttpExceptionFilter`는 재설치하지만 `LoggingInterceptor`는 포함하지 않아 로그 계약을 검증하지 않는다.
- canonical problem statement는 native SQLite recovery를 범위에 넣지만, e2e는 `DB_PATH=:memory:`를 강제하므로 file-backed recovery 절차 자체를 자동으로 검증하지는 않는다.
- e2e는 `beforeAll`에서 한 번 띄운 앱과 shared in-memory DB를 계속 재사용하므로, 각 케이스는 완전히 독립적인 hermetic test라기보다 누적 통합 시나리오에 더 가깝다.

## 다음 프로젝트와의 연결

다음 장 `10-shippable-backend-service`는 이 단일 서비스 통합본을 실제 배포 표면에 더 가깝게 다시 포장하는 단계다. 여기서 확인한 인증, RBAC, 응답 envelope, 이벤트 seam이 다음 장의 기반선이 된다.
