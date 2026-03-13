# 07-domain-events evidence ledger

이 프로젝트의 git path history도 `2026-03-12` 이관 커밋 하나로만 남아 있다. chronology는 event bus/listener, service emit 시점, unit/e2e tests, 재검증 CLI를 기준으로 재구성했다.

| 순서 | 시간 표지 | 당시 목표 | 변경 단위 | 처음 가설 | 실제 조치 | CLI | 검증 신호 | 핵심 코드 앵커 | 새로 배운 것 | 다음 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Phase 1 | service 안의 부수효과를 별도 event 계층으로 분리한다 | `express/src/events/event-bus.ts`, `book-event-listener.ts` | 학습용 서비스면 create/update/delete 뒤에 직접 `console.log` 해도 충분해 보였다 | typed `EventBus`와 별도 listener를 만들어 side effect 수신자를 service 바깥으로 뺐다 | `COREPACK_ENABLE_AUTO_PIN=0 pnpm run build && pnpm run test && pnpm run test:e2e` (`express/`) | `Tests 5 passed`, `test:e2e 5 passed` | `emit/on/off/removeAllListeners` | event는 로그보다 "성공한 상태 변화를 바깥으로 알리는 계약"에 더 가깝다 | emit 시점을 성공한 저장 뒤로 고정해야 한다 |
| 2 | Phase 2 | 저장 성공 뒤에만 event를 발행한다 | `express/src/services/book.service.ts`, `nestjs/src/books/books.service.ts` | create/update/delete 중간 어디서 emit해도 크게 다르지 않을 것 같았다 | repository save/remove가 끝난 뒤에만 `book.created`, `book.updated`, `book.deleted`를 발행하게 했다 | `COREPACK_ENABLE_AUTO_PIN=0 pnpm run build && pnpm run test && pnpm run test:e2e` (`nestjs/`) | `Tests 8 passed`, `test:e2e 4 passed` | `const saved = await this.bookRepository.save(book); this.eventEmitter.emit(...)` | domain event는 "일어나기를 바라는 일"이 아니라 "이미 성공한 일"을 뒤로 전달하는 신호다 | listener와 e2e가 이 경계를 붙잡아야 한다 |
| 3 | Phase 3 | emit/consume 경계를 테스트로 묶는다 | `express/test/unit/event-bus.test.ts`, `nestjs/test/unit/book-event.listener.test.ts` | 콘솔 로그가 찍히면 이벤트도 충분히 동작한 것처럼 느끼기 쉽다 | EventBus는 emit/subscribe/remove를 unit으로, listener는 `console.log` spy로, e2e는 CRUD 흐름으로 각각 고정했다 | 위 명령 재실행 | Express unit 5 + e2e 5, Nest unit 8 + e2e 4 통과 | listener test에서 payload를 읽어 의미 있는 로그를 남기는 검증 | domain event 학습에서 중요한 건 "이벤트가 있다"가 아니라 "어느 성공 경계 뒤에서만 나온다"는 사실이다 | 다음 프로젝트에서 기능보다 운영성 규약이 앞에 온다 |

## 근거 파일

- `core/07-domain-events/README.md`
- `core/07-domain-events/problem/README.md`
- `core/07-domain-events/express/src/events/event-bus.ts`
- `core/07-domain-events/express/src/events/book-event-listener.ts`
- `core/07-domain-events/express/src/services/book.service.ts`
- `core/07-domain-events/nestjs/src/events/book-event.listener.ts`
- `core/07-domain-events/nestjs/src/books/books.service.ts`
- `core/07-domain-events/express/test/unit/event-bus.test.ts`
- `core/07-domain-events/nestjs/test/unit/book-event.listener.test.ts`
