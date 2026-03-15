# 07-domain-events evidence ledger

이 lab의 path history도 `2026-03-12` 이관 커밋 한 번으로 압축돼 있어, chronology는 event bus/listener 경계, emit 시점, unit/e2e 검증, native sqlite 준비 문서를 기준으로 다시 복원했다. 기존 blog 본문은 사실 근거로 사용하지 않았다.

| 순서 | 시간 표지 | 당시 목표 | 변경 단위 | 처음 가설 | 실제 조치 | CLI | 검증 신호 | 핵심 코드 앵커 | 새로 배운 것 | 다음 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Phase 1 | service 본문에서 side effect를 분리한다 | `express/src/events/event-bus.ts`, `express/src/events/book-event-listener.ts`, `express/src/app.ts` | 학습용 CRUD라면 service 안에서 직접 로그를 찍어도 충분해 보였다 | typed `EventBus`와 `BookEventListener`를 따로 두고, app wiring에서 bus와 listener를 연결하게 만들었다 | `COREPACK_ENABLE_AUTO_PIN=0 pnpm run build`, `COREPACK_ENABLE_AUTO_PIN=0 pnpm run test`, `COREPACK_ENABLE_AUTO_PIN=0 pnpm run test:e2e` (`express/`) | unit 5개 + e2e 5개 통과 | `new BookEventListener(bus)` | Express는 이벤트 경계를 프레임워크가 숨기지 않아 wiring 자체가 학습 포인트가 된다 | emit 시점을 성공 경계 뒤로 고정한다 |
| 2 | Phase 2 | 저장 성공 뒤에만 이벤트를 발행한다 | `express/src/services/book.service.ts`, `nestjs/src/books/books.service.ts`, `nestjs/src/events/events.ts` | create/update/delete 어느 시점에서 emit해도 큰 차이는 없을 것 같았다 | repository save/remove가 성공한 뒤에만 `book.created`, `book.updated`, `book.deleted`를 emit하고, 실패 시에는 예외를 던지고 종료하게 했다 | `COREPACK_ENABLE_AUTO_PIN=0 pnpm run build`, `COREPACK_ENABLE_AUTO_PIN=0 pnpm run test`, `COREPACK_ENABLE_AUTO_PIN=0 pnpm run test:e2e` (`nestjs/`) | unit 8개 + e2e 4개 통과 | `const saved = await this.bookRepository.save(book); this.eventEmitter.emit(...)` | 이벤트는 "일어나길 바라는 일"이 아니라 "이미 성공한 사실"이어야 한다. 다만 현재 emit는 durable publish가 아니라 process-local synchronous call이다 | 어떤 테스트가 어느 경계를 증명하는지 분리해 본다 |
| 3 | Phase 3 | emit와 consume 경계를 서로 다른 테스트 층에서 고정한다 | `express/test/unit/event-bus.test.ts`, `express/test/e2e/events.e2e.test.ts`, `nestjs/test/unit/book-event.listener.test.ts`, `nestjs/test/unit/books.service.test.ts`, `nestjs/test/e2e/events.e2e.test.ts` | 콘솔 로그가 찍히고 HTTP가 통과하면 이벤트 경계도 충분히 설명된 것처럼 보일 수 있다 | Express는 bus abstraction과 e2e persistence 유지까지 함께 보고, NestJS는 listener unit, service unit, e2e로 emit/consume/실패 비발행을 나눠 고정했다 | 위 명령 재실행 | Express 총 10개, Nest 총 12개 테스트 통과 | Express `removeAllListeners()`, Nest `eventEmitter.on/off` | 같은 이벤트 구조라도 테스트가 증명하는 경계 배치는 서로 조금 다르다. 둘 다 "요청 뒤 eventually"가 아니라 "요청 직후 handler가 불렸는가"를 본다 | 운영 규약 쪽으로 관심이 이동한다 |
| 4 | Phase 4 | native sqlite 문서와 이벤트 테스트 격리를 함께 정리한다 | `docs/native-sqlite-recovery.md`, Express/Nest README, 각 e2e teardown 코드 | recovery 문서는 persistence lab에서만 중요할 것 같았다 | 현재 환경에서는 복구 없이도 build/test/e2e가 통과했지만, `better-sqlite3` 준비 절차와 listener 정리 방식까지 재현 가능성의 일부로 함께 남겼다 | 위 build/test/e2e 재실행 + recovery 문서 점검 | binding 오류 없음, listener 정리 후 테스트 상호 오염 없음 | recovery 문서 + `removeAllListeners` / `eventEmitter.off` | 이벤트 테스트도 native dependency와 listener cleanup 두 축이 함께 안정적이어야 재현 가능하다 | `08-production-readiness`에서 운영 규약으로 넘어간다 |

## 근거 파일

- `core/07-domain-events/problem/README.md`
- `core/07-domain-events/README.md`
- `docs/native-sqlite-recovery.md`
- `core/07-domain-events/express/src/events/event-bus.ts`
- `core/07-domain-events/express/src/events/book-event-listener.ts`
- `core/07-domain-events/express/src/services/book.service.ts`
- `core/07-domain-events/express/src/app.ts`
- `core/07-domain-events/express/test/unit/event-bus.test.ts`
- `core/07-domain-events/express/test/e2e/events.e2e.test.ts`
- `core/07-domain-events/nestjs/src/app.module.ts`
- `core/07-domain-events/nestjs/src/events/events.module.ts`
- `core/07-domain-events/nestjs/src/events/book-event.listener.ts`
- `core/07-domain-events/nestjs/src/events/events.ts`
- `core/07-domain-events/nestjs/src/books/books.service.ts`
- `core/07-domain-events/nestjs/test/unit/book-event.listener.test.ts`
- `core/07-domain-events/nestjs/test/unit/books.service.test.ts`
- `core/07-domain-events/nestjs/test/e2e/events.e2e.test.ts`
