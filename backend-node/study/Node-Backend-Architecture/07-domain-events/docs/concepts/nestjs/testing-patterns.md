# Testing Patterns — NestJS Event System

## 테스트 전략

| 레벨 | 대상 | 방식 |
|------|------|------|
| Unit (Service) | 이벤트 발행 검증 | Mock EventEmitter2 + Mock Repository |
| Unit (Listener) | 리스너 로직 검증 | 직접 인스턴스 + `console.log` 스파이 |
| E2E | 전체 통합 검증 | 실제 AppModule + EventEmitter2 스파이 |

## Unit Test: Service 이벤트 발행

```typescript
mockEmitter = { emit: vi.fn() };
mockRepository = {
  find: vi.fn().mockResolvedValue([mockBook]),
  save: vi.fn().mockResolvedValue(mockBook),
  // ...
};

const module = await Test.createTestingModule({
  providers: [
    BooksService,
    { provide: getRepositoryToken(Book), useValue: mockRepository },
    { provide: EventEmitter2, useValue: mockEmitter },
  ],
}).compile();
```

### 검증 포인트
```typescript
expect(mockEmitter.emit).toHaveBeenCalledWith(
  "book.created",
  expect.any(BookCreatedEvent),
);
```

- `expect.any(BookCreatedEvent)`: 이벤트 클래스를 사용하므로 `instanceof` 검증 가능
- 실패 시 이벤트 미발행: `expect(mockEmitter.emit).not.toHaveBeenCalled()`

## Unit Test: Listener 로직

Listener를 직접 생성하고 메서드를 호출:

```typescript
const listener = new BookEventListener();
const spy = vi.spyOn(console, "log").mockImplementation(() => {});

listener.handleBookCreated(new BookCreatedEvent("1", "Test Book", "Author"));

expect(spy).toHaveBeenCalledWith(expect.stringContaining("Test Book"));
```

Listener는 순수한 `@Injectable()` 클래스이므로 DI 없이 직접 테스트 가능.

## E2E Test: 실제 이벤트 전파

```typescript
const module = await Test.createTestingModule({
  imports: [AppModule],
}).compile();

eventEmitter = module.get(EventEmitter2);
```

실제 `AppModule`을 사용하고, `EventEmitter2`를 주입받아 스파이를 등록:

```typescript
it("should emit book.created event on POST /books", async () => {
  const handler = vi.fn();
  eventEmitter.on("book.created", handler);

  await request(app.getHttpServer()).post("/books").send(validBook);

  expect(handler).toHaveBeenCalledOnce();
  eventEmitter.off("book.created", handler);  // 정리
});
```

### Express E2E vs NestJS E2E

| 항목 | Express | NestJS |
|------|---------|--------|
| EventBus 접근 | 외부 주입 | `module.get(EventEmitter2)` |
| 스파이 등록 | `eventBus.on()` | `eventEmitter.on()` |
| 정리 | `removeAllListeners()` | `eventEmitter.off()` |
| 실제 리스너 실행 | ✅ (함께 실행됨) | ✅ (`@OnEvent` 핸들러 실행됨) |

## 이벤트 클래스 vs 이벤트 인터페이스 (테스트 관점)

Express는 이벤트를 `interface`로 정의하지만, NestJS는 `class`로 정의한다:

```typescript
// Express: 일반 객체 전달
eventBus.emit("book.created", { bookId: "1", ... });

// NestJS: 클래스 인스턴스 전달
this.eventEmitter.emit("book.created", new BookCreatedEvent("1", ...));
```

클래스 기반의 장점: `expect.any(BookCreatedEvent)` 매처 사용 가능, 기본값(`timestamp = new Date()`) 지원.

## 근거 요약

- 근거: [문서] `backend-architecture/05-event-system/README.md`
- 근거: [문서] `backend-architecture/05-event-system/lab-report.md`
- 근거: [문서] `backend-architecture/05-event-system/nestjs-impl/docs/README.md`
- 근거: [문서] `backend-architecture/05-event-system/nestjs-impl/devlog/README.md`
