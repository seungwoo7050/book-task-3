# Testing Patterns — Express Event System

## 테스트 전략 개요

이벤트 시스템 테스트는 두 가지 관심사를 분리한다:
1. **이벤트 버스 자체** — emit/on/off 동작
2. **통합 동작** — HTTP 요청 → 서비스 → 이벤트 발행 → 리스너 실행

| 레벨 | 대상 | 도구 |
|------|------|------|
| Unit | `EventBus` 클래스 | `vi.fn()` 핸들러 |
| E2E | HTTP → Service → EventBus → Spy | Supertest + `vi.fn()` |

## Unit Test: EventBus

EventBus를 직접 생성하고, `vi.fn()` 핸들러를 등록하여 이벤트 전파를 검증:

```typescript
it("should emit and receive book.created events", () => {
  const handler = vi.fn();
  bus.on("book.created", handler);

  bus.emit("book.created", { bookId: "1", title: "Test", ... });

  expect(handler).toHaveBeenCalledOnce();
  expect(handler).toHaveBeenCalledWith(event);
});
```

### 검증 항목
- 이벤트별 핸들러 호출 확인 (created, updated, deleted)
- 다중 리스너 지원 (`handler1`, `handler2` 모두 호출됨)
- `off()` 로 리스너 제거 후 호출되지 않음

## E2E Test: 이벤트 스파이 패턴

`createApp(db, eventBus)` 으로 EventBus를 외부에서 주입하여 스파이를 등록:

```typescript
beforeEach(() => {
  eventBus = new EventBus();
  app = createApp(db, eventBus);
});

it("should emit book.created event on POST", async () => {
  const handler = vi.fn();
  eventBus.on("book.created", handler);

  await request(app).post("/books").send(validBook);

  expect(handler).toHaveBeenCalledOnce();
  expect(handler.mock.calls[0][0]).toMatchObject({
    title: "Clean Code",
    author: "Robert C. Martin",
  });
});
```

### 핵심: 실패 시 이벤트 미발행 테스트

```typescript
it("should not emit events on failed operations", async () => {
  const handler = vi.fn();
  eventBus.on("book.deleted", handler);

  await request(app).delete("/books/nonexistent");

  expect(handler).not.toHaveBeenCalled();
});
```

이벤트는 **성공한 작업 후에만** 발행되어야 한다. 이 테스트는 그 보장을 검증한다.

## EventBus 주입 패턴

`createApp(db, eventBus?)` 의 선택적 파라미터가 핵심:
- 프로덕션: 파라미터 없이 호출 → 내부에서 `new EventBus()` 생성
- 테스트: EventBus를 외부에서 주입 → 스파이 핸들러 등록 가능

이 패턴으로 테스트에서 이벤트 발행을 직접 관찰할 수 있다.

## afterEach에서 리소스 정리

```typescript
afterEach(() => {
  eventBus.removeAllListeners();  // 이전 테스트의 핸들러 잔류 방지
  db.close();
});
```

`removeAllListeners()`로 이벤트 핸들러 누적을 방지한다.

## 근거 요약

- 근거: [문서] `backend-architecture/05-event-system/README.md`
- 근거: [문서] `backend-architecture/05-event-system/lab-report.md`
- 근거: [문서] `backend-architecture/05-event-system/express-impl/docs/README.md`
- 근거: [문서] `backend-architecture/05-event-system/express-impl/devlog/README.md`
