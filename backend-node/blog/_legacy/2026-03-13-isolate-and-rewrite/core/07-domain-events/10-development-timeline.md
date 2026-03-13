# 07-domain-events development timeline

persistence가 들어오고 나면 service 본문이 금방 비대해진다. 저장도 해야 하고, 로그도 남겨야 하고, 나중엔 알림이나 메일도 붙고 싶어진다. 이 프로젝트가 중요한 이유는 그 유혹을 한 번 끊고, side effect를 이벤트 경계 뒤로 보내는 연습을 하기 때문이다.

## 구현 순서 요약

- Express에서 `EventEmitter`를 감싼 `EventBus`를 도입한다.
- NestJS에서 listener 클래스로 side effect 위치를 더 명확히 분리한다.
- 성공 경로와 실패 경로의 발행 조건을 테스트로 닫는다.

## Phase 1

- 당시 목표: Express 서비스에서 persistence 이후 side effect를 본문 밖으로 뺀다.
- 변경 단위: `express/src/events/event-bus.ts`, `express/test/e2e/events.e2e.test.ts`
- 처음 가설: create/update/delete 뒤에 console log나 후속 동작을 service 안에 계속 두면 나중에 책임이 섞인다.
- 실제 진행: `EventBus`를 `EventEmitter` wrapper로 만들고, service는 저장 성공 직후에만 `book.created`, `book.updated`, `book.deleted`를 emit하도록 정리했다.

CLI:

```bash
$ cd express
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test:e2e
Tests 5 passed (5)
Tests 5 passed (5)
```

검증 신호:

- e2e 출력에 `[Event] Book created: "Clean Code" ...` 로그가 남는다.
- failed delete에서는 handler가 호출되지 않는다.

핵심 코드:

```ts
export class EventBus {
  private emitter = new EventEmitter();

  emit<K extends keyof EventMap>(event: K, data: EventMap[K]): void {
    this.emitter.emit(event, data);
  }
}
```

왜 이 코드가 중요했는가:

이 래퍼 덕분에 서비스는 `EventEmitter` 구현 세부를 모르고도 "어떤 시점에 어떤 이벤트를 내보낼지"만 결정하면 된다. side effect의 책임이 한 단계 밀린다.

새로 배운 것:

- 이벤트 설계의 시작점은 분산 시스템이 아니라 단일 서비스 내부 책임 분리다.

## Phase 2

- 당시 목표: NestJS에서 listener registration을 프레임워크 문법으로 분리한다.
- 변경 단위: `nestjs/src/events/book-event.listener.ts`, `nestjs/src/books/books.service.ts`
- 처음 가설: NestJS에서는 event bus 자체보다 listener 등록 방식이 더 큰 구조 차이를 만들 것이다.
- 실제 진행: `BooksService`는 저장 성공 뒤 `eventEmitter.emit()`만 하고, `BookEventListener`는 `@OnEvent()` 메서드로 각각의 side effect를 담당한다.

CLI:

```bash
$ cd ../nestjs
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test:e2e
Tests 8 passed (8)
Tests 4 passed (4)
```

검증 신호:

- e2e 출력에 `[Event] Book updated ...`, `[Event] Book deleted ...` 로그가 남는다.
- unit test는 listener가 console log에 어떤 문자열을 남기는지까지 확인한다.

핵심 코드:

```ts
@OnEvent("book.updated")
handleBookUpdated(event: BookUpdatedEvent): void {
  console.log(`[Event] Book updated: id=${event.bookId}, changes=[${event.changes.join(", ")}]`);
}
```

왜 이 코드가 중요했는가:

이벤트가 service 본문을 떠나 listener 메서드로 이동한 순간, "저장 성공"과 "저장 후 로그/후속 동작"이 명확히 다른 책임이 된다.

새로 배운 것:

- NestJS listener는 단순 이벤트 소비자가 아니라 service 본문을 얇게 유지하는 구조 장치다.

## Phase 3

- 당시 목표: 성공 경로에서만 이벤트가 나가고 실패 경로에서는 나가지 않는다는 사실을 증명한다.
- 변경 단위: `express/test/e2e/events.e2e.test.ts`, `nestjs/test/unit/book-event.listener.test.ts`, `nestjs/test/e2e/events.e2e.test.ts`
- 처음 가설: 이벤트 설계는 로그를 보는 것만으로는 부족하고, handler 호출 여부를 테스트로 못 박아야 한다.
- 실제 진행: Express e2e는 `vi.fn()` handler를 걸어 `POST/PUT/DELETE` 성공 시 호출되고, `DELETE /books/nonexistent`에서는 호출되지 않음을 검증했다. Nest는 listener unit과 e2e 둘 다 유지했다.

CLI:

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test:e2e
[Event] Book updated: id=..., changes=[price]
[Event] Book deleted: id=...
```

검증 신호:

- Express는 failed operation에서 `handler`가 불리지 않는다.
- NestJS는 listener unit test 3개와 e2e 4개가 모두 통과한다.

핵심 코드:

```ts
await request(app).delete("/books/nonexistent");
expect(handler).not.toHaveBeenCalled();
```

왜 이 코드가 중요했는가:

이 한 줄이 이벤트 설계의 불변식을 보여 준다. 실패한 연산은 side effect를 내보내지 않는다. 이 규칙이 없으면 이벤트는 observability가 아니라 혼란이 된다.

새로 배운 것:

- 이벤트를 잘 설계한다는 건 많이 발행하는 게 아니라 발행하지 말아야 할 순간을 더 엄격히 정하는 일이다.

다음:

- [`../../applied/08-production-readiness/00-series-map.md`](../../applied/08-production-readiness/00-series-map.md)에서 기능 내부보다 운영 surface가 중심이 되는 applied 단계로 넘어간다.
