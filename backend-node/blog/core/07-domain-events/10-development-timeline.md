# 07-domain-events development timeline

여기까지 오면 CRUD와 persistence는 이미 익숙하다. 그래서 이 프로젝트의 관심사는 "어떻게 저장하느냐"보다 "저장된 사실을 어떻게 바깥으로 전달하느냐"로 옮겨 간다. 읽는 흐름도 자연스럽게 service 내부가 아니라 event boundary 쪽으로 기운다.

## 흐름 먼저 보기

1. EventBus와 listener로 side effect 수신자를 분리한다.
2. 저장 성공 뒤에만 event를 발행한다.
3. listener unit test와 e2e로 경계를 고정한다.

## EventBus를 만든 장면

처음 전환점은 service 안에서 바로 `console.log` 하던 상상을 접고, event boundary를 따로 만든 데서 나온다.

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

이 코드가 중요한 이유는, service가 이제 side effect를 직접 실행하지 않고 "무슨 일이 일어났는가"만 말하면 되기 때문이다. 누가 그 사실을 듣고 무엇을 할지는 listener가 맡는다.

listener 쪽은 바로 그 구독자를 드러낸다.

```ts
this.eventBus.on("book.created", this.onBookCreated.bind(this));
this.eventBus.on("book.updated", this.onBookUpdated.bind(this));
this.eventBus.on("book.deleted", this.onBookDeleted.bind(this));
```

즉 이 프로젝트는 이벤트를 도입했다기보다, service와 side effect의 경계를 하나 더 만든 셈에 가깝다.

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run build && pnpm run test && pnpm run test:e2e
Tests       5 passed (5)
test:e2e    5 passed (5)
```

## emit를 저장 뒤에 둔 장면

다음 장면은 emit 시점이다. 이벤트를 쓰기로 했다고 해서 아무 때나 emit해도 되는 건 아니다.

```ts
const created = this.bookRepository.create(book);

this.eventBus.emit("book.created", {
  bookId: created.id,
  title: created.title,
  author: created.author,
  timestamp: new Date(),
});
```

Express에서는 repository가 먼저 성공하고, 그다음에야 event가 나간다. 이 순서가 중요한 이유는 event가 "일어나기를 바라는 일"이 아니라 "이미 일어난 일"이어야 하기 때문이다.

NestJS도 같은 흐름을 유지한다.

```ts
const saved = await this.bookRepository.save(book);

this.eventEmitter.emit(
  "book.created",
  new BookCreatedEvent(saved.id, saved.title, saved.author),
);
```

프레임워크가 달라도 emit가 저장 뒤에 오는 이유는 같다. 그 순서가 깨지면 listener는 아직 확정되지 않은 상태 변화를 믿게 된다.

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run build && pnpm run test && pnpm run test:e2e
Tests       8 passed (8)
test:e2e    4 passed (4)
```

## listener와 e2e로 경계를 고정한 장면

이 프로젝트의 마지막 장면은 이벤트가 존재한다는 사실이 아니라, emit와 consume 경계가 실제로 검증된다는 점이다.

```ts
bus.on("book.created", handler);
bus.emit("book.created", event);
expect(handler).toHaveBeenCalledWith(event);
```

Express unit test는 event bus가 publish/subscribe abstraction으로 제대로 서 있는지 보여 준다. Nest listener는 다른 방식으로 같은 확인을 한다.

```ts
const spy = vi.spyOn(console, "log").mockImplementation(() => {});
listener.handleBookUpdated(new BookUpdatedEvent("1", ["title", "price"]));
expect(spy).toHaveBeenCalledWith(expect.stringContaining("title, price"));
```

listener가 event payload를 실제로 읽어 의미 있는 side effect를 만들고 있다는 걸 붙잡는 셈이다. 여기에 e2e CRUD가 더해지면서, 이제 이 프로젝트는 "event를 쓴다"가 아니라 "성공한 상태 변화 뒤에만 side effect가 따라온다"는 규칙을 가지게 된다.

다음 프로젝트에서는 기능보다 앞에 오는 운영성 규약, 즉 health/readiness, runtime config, structured logging이 중심으로 올라온다.
