# 07-domain-events development timeline

`06-persistence-and-repositories`까지는 저장 경계를 세우는 일이 중심이었다면, 이 lab은 그 저장 경계 바깥으로 무엇을 언제 흘려보낼지 정하는 단계다. 이번 재검토에서는 이벤트를 "로그를 좀 더 구조적으로 찍는 기능"처럼 읽지 않기 위해, emit 시점과 실패 경로를 중심으로 chronology를 다시 세웠다.

## 흐름 먼저 보기

1. Express에서 EventEmitter 기반 `EventBus`와 listener를 따로 세운다.
2. service는 저장 성공 뒤에만 `book.*` 이벤트를 emit하고, 실패 경로에서는 emit하지 않는다.
3. NestJS는 `EventEmitterModule`, `@OnEvent`, `EventEmitter2`로 같은 구조를 옮기고, 테스트가 어떤 경계를 고정하는지 비교한다.

## Express에서 service와 side effect를 갈라 놓은 장면

Express 쪽의 첫 전환점은 `EventBus`가 생기는 순간이다.

```ts
export class EventBus {
  private emitter = new EventEmitter();

  emit<K extends keyof EventMap>(event: K, data: EventMap[K]): void {
    this.emitter.emit(event, data);
  }

  on<K extends keyof EventMap>(event: K, handler: (data: EventMap[K]) => void): void {
    this.emitter.on(event, handler as (...args: unknown[]) => void);
  }
}
```

여기서 중요한 건 EventEmitter를 썼다는 사실보다, service가 더 이상 `console.log` 같은 side effect를 직접 호출하지 않아도 된다는 점이다. service는 이제 "무슨 일이 일어났는가"만 말하고, 그 사실을 듣는 listener는 바깥에 둔다.

`createApp()`도 이 경계를 코드 표면에 드러낸다.

```ts
const bus = eventBus ?? new EventBus();
new BookEventListener(bus);
...
app.use("/books", createBookRouter(db, bus));
```

즉 Express lane에서는 event wiring이 숨겨져 있지 않다. 어떤 bus를 쓰고 어떤 listener가 붙는지, 테스트에서 bus를 주입할 수 있는지까지 명시적으로 보인다.

여기서 한 가지 더 분명히 해야 할 건 실행 모델이다. `EventBus.emit()`는 결국 Node `EventEmitter.emit()`를 그대로 감싼다. 즉 현재 Express 레인은 비동기 broker나 durable queue를 흉내 내지 않는다. service가 emit하면, 같은 프로세스 안에서 listener가 즉시 실행되는 동기 event boundary에 더 가깝다.

listener는 세 종류 이벤트를 구독하되, 각 handler 안에서 별도 `try/catch`를 둔다.

```ts
this.eventBus.on("book.created", this.onBookCreated.bind(this));
this.eventBus.on("book.updated", this.onBookUpdated.bind(this));
this.eventBus.on("book.deleted", this.onBookDeleted.bind(this));
```

```ts
try {
  console.log(`[Event] Book deleted: ${event.bookId}`);
} catch (err) {
  console.error("[Event Listener Error] book.deleted:", err);
}
```

이 때문에 listener 내부 side effect 오류가 서비스 본문을 다시 흔들지 않도록 의도한 구조라는 점도 읽힌다.

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run build
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test:e2e
Test Files  2 passed (2)
Tests       10 passed (10)
```

Express 검증은 unit 5개와 e2e 5개가 모두 통과했다. e2e 출력에는 실제 이벤트 로그와 request log가 함께 찍혀, 이벤트 발행이 HTTP 흐름과 같은 실행 안에서 일어나는 것도 관찰된다.

## emit를 저장 성공 뒤로 고정한 장면

이 lab의 핵심은 이벤트가 있다는 사실보다 emit 시점이다. Express `BookService`는 먼저 repository를 호출하고, 성공한 결과를 받은 뒤에만 이벤트를 내보낸다.

```ts
const created = this.bookRepository.create(book);

this.eventBus.emit("book.created", {
  bookId: created.id,
  title: created.title,
  author: created.author,
  timestamp: new Date(),
});
```

update/delete도 같은 패턴이다.

```ts
const updated = this.bookRepository.update(id, dto);
if (!updated) throw new NotFoundError(...);

const changes = Object.keys(dto);
this.eventBus.emit("book.updated", { bookId: id, changes, timestamp: new Date() });
```

```ts
const deleted = this.bookRepository.delete(id);
if (!deleted) throw new NotFoundError(...);

this.eventBus.emit("book.deleted", { bookId: id, timestamp: new Date() });
```

그래서 event는 "바라던 일"이 아니라 "이미 성공한 일"을 알리는 사실이 된다. e2e의 `DELETE /books/nonexistent` 시나리오에서 handler가 호출되지 않는 것도 바로 이 경계를 다시 확인하는 장면이다.

## NestJS에서 같은 경계를 프레임워크 안으로 옮긴 장면

NestJS는 같은 구조를 `EventEmitterModule`과 `@OnEvent`로 감싼다.

```ts
imports: [
  TypeOrmModule.forRoot(...),
  EventEmitterModule.forRoot(),
  BooksModule,
  EventsModule,
]
```

listener는 decorator로 구독 지점을 선언한다.

```ts
@OnEvent("book.created")
handleBookCreated(event: BookCreatedEvent): void {
  ...
}
```

서비스는 `EventEmitter2`를 주입받아, 저장 뒤에만 emit한다.

```ts
const saved = await this.bookRepository.save(book);

this.eventEmitter.emit(
  "book.created",
  new BookCreatedEvent(saved.id, saved.title, saved.author),
);
```

update는 전달할 `changes` 배열을 undefined-filter까지 거쳐 계산한다.

```ts
const changes = Object.keys(dto).filter(
  (key) => dto[key as keyof UpdateBookDto] !== undefined,
);
```

이 차이 덕분에 Express는 plain object event payload를, NestJS는 event class instance를 발행한다는 것도 같이 보인다. 둘 다 의미는 같지만, NestJS 쪽이 조금 더 명시적인 event type을 가지는 셈이다.

NestJS도 실행 모델 자체는 크게 다르지 않다. 여기서 쓰는 것은 `emitAsync`나 외부 transport가 아니라 plain `eventEmitter.emit(...)`이고, e2e는 HTTP 요청 직후 `handler` spy가 바로 호출됐는지를 본다. 그래서 이 lab의 "event-driven"은 cross-process delivery보다는 in-process side-effect decoupling에 가깝다.

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run build
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test:e2e
Test Files  3 passed (3)
Tests       12 passed (12)
```

Nest 검증은 listener unit 3개, service unit 5개, e2e 4개가 통과했다. 특히 service unit은 mock repository와 mock emitter를 써서 "찾지 못하면 NotFoundException을 던지고 emit는 호출되지 않는다"까지 고정한다.

## 테스트가 증명하는 경계가 서로 조금 다른 장면

이번에 다시 보며 가장 유용했던 건 두 레인이 같은 이벤트 구조를 갖더라도 테스트가 증명하는 범위는 약간 다르다는 점이었다. Express e2e는 이벤트 발행뿐 아니라 마지막에 다시 `GET /books/:id`를 쳐서 "이벤트가 있어도 persistence 흐름이 깨지지 않는다"는 걸 한 번 더 확인한다.

```ts
it("should still persist data with events", async () => {
  const createRes = await request(app).post("/books").send(validBook);
  ...
  const getRes = await request(app).get(`/books/${id}`);
  expect(getRes.body.data.title).toBe("Clean Code");
});
```

반면 Nest e2e는 이벤트 발행 자체와 실패 경로 비발행에 더 집중하고, persistence 확인은 service unit/e2e 전체 조합에 나눠 맡긴다. 그래서 두 레인을 비교할 때 "테스트 숫자"보다 "어떤 경계를 어디서 증명하는가"를 보는 편이 더 정확하다.

또 한 가지는 listener 정리 방식이다. Express e2e는 `afterEach`에서 `eventBus.removeAllListeners()`로 테스트 간 listener 누수를 정리하고, Nest e2e는 각 케이스에서 `eventEmitter.on/off`로 핸들러를 붙였다 떼는 방식을 쓴다. 두 방식 모두 이벤트 테스트가 서로의 구독 상태를 오염시키지 않도록 경계를 세운다는 점이 중요하다.

## 여기서 남는 것

이 문서를 다시 쓰고 나니, 이 lab의 요점은 이벤트 시스템을 도입했다는 선언이 아니라 "성공한 상태 변화 뒤에만 side effect가 따라온다"는 규칙을 테스트로 고정한 데 있다는 점이 더 분명해졌다. 동시에 이 규칙이 현재는 queue/outbox가 아니라 in-process synchronous emit 위에 서 있다는 것도 같이 보인다. 다음 `08-production-readiness`는 이 feature 경계 위에 health/readiness, runtime config, structured logging 같은 운영 규약을 얹는 단계로 이어진다.
