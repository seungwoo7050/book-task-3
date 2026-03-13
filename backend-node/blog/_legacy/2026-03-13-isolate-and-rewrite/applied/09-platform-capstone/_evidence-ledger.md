# 09-platform-capstone evidence ledger

근거는 [`README.md`](../../../study/Node-Backend-Architecture/applied/09-platform-capstone/README.md), [`nestjs/src/app.module.ts`](../../../study/Node-Backend-Architecture/applied/09-platform-capstone/nestjs/src/app.module.ts), [`nestjs/src/books/books.service.ts`](../../../study/Node-Backend-Architecture/applied/09-platform-capstone/nestjs/src/books/books.service.ts), [`nestjs/src/auth/auth.service.ts`](../../../study/Node-Backend-Architecture/applied/09-platform-capstone/nestjs/src/auth/auth.service.ts), [`nestjs/src/events/app-event.listener.ts`](../../../study/Node-Backend-Architecture/applied/09-platform-capstone/nestjs/src/events/app-event.listener.ts), [`nestjs/test/e2e/capstone.e2e.test.ts`](../../../study/Node-Backend-Architecture/applied/09-platform-capstone/nestjs/test/e2e/capstone.e2e.test.ts), 실제 검증 출력이다.

## Phase 1

- 순서: 1
- 시간 표지: Phase 1
- 당시 목표: 03~08에서 따로 보던 규약을 단일 AppModule 아래로 통합한다.
- 변경 단위: `nestjs/src/app.module.ts`
- 처음 가설: capstone은 새 개념을 더 넣기보다 지금까지 만든 모듈 경계가 같이 살아남는지 보는 프로젝트여야 한다.
- 실제 조치: `TypeOrmModule.forRoot`, `EventEmitterModule.forRoot`, `AuthModule`, `BooksModule`, `EventsModule`을 한 module에 묶었다.
- CLI: `COREPACK_ENABLE_AUTO_PIN=0 pnpm run build`
- 검증 신호: `nest build` 통과
- 핵심 코드 앵커: `AppModule.imports`
- 새로 배운 것: capstone 통합의 핵심은 기능 추가가 아니라 "기존 규약을 억지로 바꾸지 않고 한 프로세스에 넣을 수 있는가"였다.
- 다음: auth/books/events 서비스가 실제로 연결되는지 본다.

## Phase 2

- 순서: 2
- 시간 표지: Phase 2
- 당시 목표: auth, books, events가 서로 알맞은 경계에서만 만나는지 확인한다.
- 변경 단위: `nestjs/src/auth/auth.service.ts`, `nestjs/src/books/books.service.ts`, `nestjs/src/events/app-event.listener.ts`
- 처음 가설: capstone이 비대해지지 않으려면 service는 저장과 이벤트 발행까지만 하고, 후속 동작은 listener가 가져가야 한다.
- 실제 조치: `AuthService.register()`는 `user.registered`, `BooksService.create()/update()/remove()`는 book 이벤트를 발행하고, listener가 로그를 남긴다.
- CLI: `COREPACK_ENABLE_AUTO_PIN=0 pnpm run test`
- 검증 신호: unit `Tests 10 passed (10)`
- 핵심 코드 앵커: `BooksService.create()`, `AuthService.register()`, `AppEventListener`
- 새로 배운 것: 통합 서비스가 견디는지 보려면 "모듈이 많다"보다 "모듈이 서로 어디서만 만나는가"를 봐야 했다.
- 다음: 12개 e2e 시나리오로 public/auth/admin/event 경계를 모두 검증한다.

## Phase 3

- 순서: 3
- 시간 표지: Phase 3
- 당시 목표: auth, public books, admin books, role boundary, validation, missing resource를 단일 서비스로 재검증한다.
- 변경 단위: `nestjs/test/e2e/capstone.e2e.test.ts`
- 처음 가설: capstone의 품질은 기능 수보다 e2e coverage로 더 잘 드러난다.
- 실제 조치: register, duplicate register, login, invalid credential, public GET /books, protected POST/PUT/DELETE /books, regular user 403, invalid body 400, missing book 404를 모두 한 테스트 파일에 넣었다.
- CLI: `COREPACK_ENABLE_AUTO_PIN=0 pnpm run test:e2e`
- 검증 신호: `✓ test/e2e/capstone.e2e.test.ts (12 tests)`, event logs for `book.updated`, `book.deleted`, `user.registered`
- 핵심 코드 앵커: `capstone.e2e.test.ts`
- 새로 배운 것: capstone은 새 기능을 보여 주는 장르가 아니라 "지금까지 만든 규약이 한 서비스 안에서도 일관적인가"를 증명하는 장르다.
- 다음: `10-shippable-backend-service`에서 같은 통합판을 채용 제출용 surface로 다시 포장한다.
