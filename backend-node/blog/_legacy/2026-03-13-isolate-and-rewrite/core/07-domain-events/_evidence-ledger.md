# 07-domain-events evidence ledger

근거는 [`README.md`](../../../study/Node-Backend-Architecture/core/07-domain-events/README.md), [`express/src/events/event-bus.ts`](../../../study/Node-Backend-Architecture/core/07-domain-events/express/src/events/event-bus.ts), [`express/test/e2e/events.e2e.test.ts`](../../../study/Node-Backend-Architecture/core/07-domain-events/express/test/e2e/events.e2e.test.ts), [`nestjs/src/events/book-event.listener.ts`](../../../study/Node-Backend-Architecture/core/07-domain-events/nestjs/src/events/book-event.listener.ts), [`nestjs/test/unit/book-event.listener.test.ts`](../../../study/Node-Backend-Architecture/core/07-domain-events/nestjs/test/unit/book-event.listener.test.ts), 실제 검증 출력이다.

## Phase 1

- 순서: 1
- 시간 표지: Phase 1
- 당시 목표: Express 레인에서 persistence 이후 side effect를 `EventBus`로 분리한다.
- 변경 단위: `express/src/events/event-bus.ts`, `express/src/services/*`, `express/test/e2e/events.e2e.test.ts`
- 처음 가설: DB 저장과 후속 로그/알림 성격의 동작을 같은 service 본문에 두면 실패 경계를 설명하기 어렵다.
- 실제 조치: `EventBus`를 `EventEmitter` 위에 감싸고, create/update/delete 성공 후에만 `book.created`, `book.updated`, `book.deleted`를 발행하게 했다.
- CLI: `COREPACK_ENABLE_AUTO_PIN=0 pnpm run test`, `COREPACK_ENABLE_AUTO_PIN=0 pnpm run test:e2e`
- 검증 신호: unit `Tests 5 passed (5)`, e2e `Tests 5 passed (5)`와 함께 `[Event] Book created ...` 로그가 출력된다.
- 핵심 코드 앵커: `EventBus.emit()`, `events.e2e.test.ts`
- 새로 배운 것: 이벤트 설계의 핵심은 이벤트를 많이 만드는 게 아니라 "실패한 연산에서는 발행하지 않는다"를 분명히 하는 데 있었다.
- 다음: NestJS listener로 같은 경계를 다시 세운다.

## Phase 2

- 순서: 2
- 시간 표지: Phase 2
- 당시 목표: NestJS에서 event-emitter와 listener 클래스로 side effect를 분리한다.
- 변경 단위: `nestjs/src/events/book-event.listener.ts`, `nestjs/src/events/events.module.ts`, `nestjs/src/books/books.service.ts`
- 처음 가설: NestJS에서는 이벤트 발행보다 listener 등록 방식이 구조 차이를 더 크게 보여 줄 것이다.
- 실제 조치: `@OnEvent("book.created")` 등으로 listener 메서드를 등록하고, service는 저장 성공 뒤에만 `eventEmitter.emit()`을 호출하게 했다.
- CLI: `COREPACK_ENABLE_AUTO_PIN=0 pnpm run test`, `COREPACK_ENABLE_AUTO_PIN=0 pnpm run test:e2e`
- 검증 신호: unit `Tests 8 passed (8)`, e2e `Tests 4 passed (4)`와 함께 `[Event] Book updated ...`, `[Event] Book deleted ...` 로그가 남는다.
- 핵심 코드 앵커: `BookEventListener`, `BooksService.create()/update()/remove()`
- 새로 배운 것: listener는 부수효과의 위치를 옮기는 도구이면서 동시에 "서비스 본문이 책임져야 할 것과 아닌 것"을 나누는 문법이었다.
- 다음: 성공/실패 경계를 테스트가 어떻게 설명하는지 본다.

## Phase 3

- 순서: 3
- 시간 표지: Phase 3
- 당시 목표: 이벤트가 성공 경로에서만 나오고 실패 경로에서는 나오지 않는다는 사실을 증명한다.
- 변경 단위: `express/test/e2e/events.e2e.test.ts`, `nestjs/test/unit/book-event.listener.test.ts`, `nestjs/test/e2e/events.e2e.test.ts`
- 처음 가설: 이벤트 프로젝트는 로그보다 테스트가 더 중요하다. listener가 불렸는지 안 불렸는지가 계약이기 때문이다.
- 실제 조치: Express e2e는 `DELETE /books/nonexistent`에서 handler가 호출되지 않음을 검증하고, Nest unit은 console log output까지 확인했다.
- CLI: `pnpm run test:e2e`
- 검증 신호: Express는 failed delete에서 handler not called, Nest는 e2e에서 `book.updated`, `book.deleted` 로그를 확인
- 핵심 코드 앵커: `vi.fn()` handler assertions, `BookEventListener` tests
- 새로 배운 것: 도메인 이벤트는 "나중에 뭐라도 할 수 있게 해 둔다"보다 "지금 이 서비스가 책임질 일을 줄인다"는 효과가 더 크다.
- 다음: `08-production-readiness`에서 기능 내부가 아니라 운영 surface를 프로젝트 중심으로 끌어올린다.
