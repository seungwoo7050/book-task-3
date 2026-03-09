# 저장 그 이후 — 도메인 이벤트로 side effect를 분리하다

## 프롤로그: "저장했다. 그 다음은?"

프로젝트 06에서 데이터가 디스크에 살아남게 되었다. 하지만 현실 세계의 서비스에서는 "저장" 자체가 끝이 아니다. 새 책이 등록되면 알림을 보내야 하고, 가격이 바뀌면 캐시를 갱신해야 하며, 삭제되면 검색 인덱스에서 제거해야 한다.

이런 작업들을 어디에 넣어야 할까? `BookService.create()` 메서드 끝에 알림 코드를 붙이고, 캐시 코드를 붙이고, 로그 코드를 붙이면? 곧 서비스 메서드는 본래 책임과 무관한 코드로 가득 찬다. 이것이 "side effect 오염"이다.

도메인 이벤트는 이 문제에 대한 우아한 답이다. **"무슨 일이 일어났다"**라는 사실만 발행하고, 그 사실에 관심 있는 쪽에서 알아서 반응하게 만드는 것이다.

---

## 1. EventEmitter — Node.js의 원시 도구

Express 레인에서는 Node.js 표준 라이브러리의 `EventEmitter`를 감싸서 타입-안전한 이벤트 버스를 만든다.

### 이벤트 타입 설계

모든 것은 `EventMap` 인터페이스에서 시작한다:

```typescript
export interface EventMap {
  "book.created": BookCreatedEvent;
  "book.updated": BookUpdatedEvent;
  "book.deleted": BookDeletedEvent;
}
```

이 매핑이 있기 때문에 `eventBus.emit("book.created", ...)` 호출 시 컴파일러가 페이로드 타입을 검사할 수 있다. 잘못된 데이터를 넘기면 컴파일 에러. 문자열 기반 이벤트 시스템에 타입 안전성을 부여하는 패턴이다.

각 이벤트는 `readonly` 필드만 가진 순수 데이터 객체다. `bookId`, `timestamp`는 모든 이벤트에 공통이고, `BookCreatedEvent`에는 `title`과 `author`가, `BookUpdatedEvent`에는 변경된 필드 목록인 `changes: string[]`가 포함된다.

### EventBus — 얇은 래퍼

`EventBus` 클래스는 `EventEmitter`를 내부에 감추고 `emit`, `on`, `off`, `removeAllListeners` 네 개 메서드만 노출한다. 제네릭 시그니처 `<K extends keyof EventMap>`으로 타입 안전성을 보장한다.

이 클래스가 하는 일은 거의 없다. 하지만 그것이 정확히 의도된 것이다. **래퍼의 역할은 인터페이스를 좁히는 것이다.** `EventEmitter`가 제공하는 수십 개의 메서드 중 필요한 것만 남김으로써, 이벤트 버스의 계약을 명확히 한다.

### Service에서의 이벤트 발행

`BookService`의 변화를 보면, 이전 프로젝트 대비 달라진 부분은 딱 두 가지다:

1. 생성자에 `EventBus`가 추가되었다.
2. CUD 연산 후 `this.eventBus.emit(...)` 호출이 추가되었다.

```typescript
create(dto: CreateBookDto): Book {
  // ...기존 로직 그대로...
  const created = this.bookRepository.create(book);
  
  this.eventBus.emit("book.created", {
    bookId: created.id,
    title: created.title,
    author: created.author,
    timestamp: new Date(),
  });
  
  return created;
}
```

핵심은 **이벤트 발행이 성공 경로에서만 일어난다**는 것이다. `bookRepository.create(book)`이 예외를 던지면 `emit`에 도달하지 않는다. 실패 시 이벤트가 발행되지 않는 것은 코드 구조가 자연스럽게 보장한다. 이 설계 의도는 E2E 테스트에서 명시적으로 검증된다: "should not emit events on failed operations".

### BookEventListener — 관심사의 분리

`BookEventListener`는 생성자에서 세 개의 이벤트에 대한 핸들러를 등록한다. 현재는 `console.log`로 로깅만 하지만, 실제 서비스라면 이메일 발송, 웹훅 호출, 통계 업데이트 등이 여기에 들어간다.

각 핸들러에 `try/catch`가 있다. 리스너에서 에러가 발생해도 이벤트 발행자(Service)에 영향을 주지 않기 위해서다. 이것이 이벤트 기반 아키텍처의 핵심 원칙 중 하나다: **발행자는 구독자의 실패에 무관해야 한다.**

---

## 2. NestJS 레인: @nestjs/event-emitter

NestJS 쪽에서는 `@nestjs/event-emitter` 패키지가 제공하는 `EventEmitter2`와 `@OnEvent` 데코레이터를 사용한다.

### EventEmitter2 — 프레임워크 통합

`AppModule`에 `EventEmitterModule.forRoot()`를 추가하면 NestJS의 DI 컨테이너에 `EventEmitter2` 인스턴스가 등록된다. Service에서는 `@Inject(EventEmitter2)`로 주입받는다.

```typescript
@Inject(EventEmitter2)
private readonly eventEmitter: EventEmitter2,
```

Express에서 `EventBus`를 수동으로 조립하던 것이 NestJS에서는 모듈 임포트와 DI로 자동화된다.

### 이벤트 클래스 vs 인터페이스

Express 쪽에서는 이벤트를 인터페이스로 정의했지만, NestJS 쪽에서는 클래스로 정의한다. `BookCreatedEvent` 클래스의 생성자는 필요한 데이터를 받고, `timestamp`는 기본값으로 `new Date()`를 갖는다.

```typescript
export class BookCreatedEvent {
  constructor(
    public readonly bookId: string,
    public readonly title: string,
    public readonly author: string,
    public readonly timestamp: Date = new Date(),
  ) {}
}
```

클래스를 쓰는 이유는 NestJS 생태계의 관례이기도 하지만, `instanceof` 검사가 가능하다는 실용적 이점도 있다. 런타임에서 이벤트 타입을 판별할 수 있다.

### @OnEvent 데코레이터

`BookEventListener`는 `@Injectable()`이면서 메서드에 `@OnEvent("book.created")` 데코레이터를 붙인다. Express에서 `this.eventBus.on("book.created", this.onBookCreated.bind(this))`라고 한 줄씩 등록하던 것이 데코레이터 한 줄로 대체된다.

```typescript
@OnEvent("book.created")
handleBookCreated(event: BookCreatedEvent): void { ... }
```

내부적으로 `EventEmitter2`가 데코레이터를 스캔해서 핸들러를 등록한다. 이 과정은 NestJS 모듈 초기화 시 자동으로 일어난다.

### EventsModule

`EventsModule`은 `BookEventListener`를 provider로 등록하고 export한다. `AppModule`이 이 모듈을 import하면 리스너가 활성화된다. 모듈을 import하지 않으면 이벤트가 발행되어도 아무도 듣지 않는다. 이 모듈 단위의 활성화/비활성화가 NestJS 아키텍처의 장점이다.

---

## 3. 두 레인의 대조

| 관점 | Express (EventBus) | NestJS (EventEmitter2) |
|------|-------------------|----------------------|
| 이벤트 정의 | 인터페이스 (`EventMap`) | 클래스 (`BookCreatedEvent`) |
| 타입 안전성 | 제네릭 (`<K extends keyof EventMap>`) | 문자열 키 + 클래스 타입 |
| 핸들러 등록 | 명시적 `.on()` 호출 | `@OnEvent()` 데코레이터 |
| 라이프사이클 관리 | 수동 `removeAllListeners()` | NestJS 모듈이 자동 관리 |
| 주입 방식 | 생성자에 수동 전달 | `@Inject(EventEmitter2)` |
| 테스트 | `vi.fn()` 핸들러 직접 등록 | `Test.createTestingModule` + spy |

Express의 `EventBus`는 더 투명하다. 코드를 읽으면 무슨 일이 일어나는지 바로 보인다. NestJS의 `@OnEvent`는 더 간결하지만, 데코레이터 뒤에서 무슨 일이 일어나는지는 프레임워크를 신뢰해야 한다.

---

## 4. 테스트에서 드러나는 설계 의도

### 이벤트 발행 검증

Express E2E 테스트에서는 `vi.fn()`으로 스파이 핸들러를 만들어 `eventBus.on()`에 등록한다. 그 뒤 HTTP 요청을 보내고, 스파이가 호출되었는지 확인한다.

```typescript
const handler = vi.fn();
eventBus.on("book.created", handler);
await request(app).post("/books").send(validBook);
expect(handler).toHaveBeenCalledOnce();
```

이 테스트가 증명하는 것: HTTP 요청 → 서비스 로직 → 이벤트 발행이 하나의 흐름으로 동작한다.

### 실패 시 이벤트 미발행

```typescript
it("should not emit events on failed operations", async () => {
  const handler = vi.fn();
  eventBus.on("book.deleted", handler);
  await request(app).delete("/books/nonexistent");
  expect(handler).not.toHaveBeenCalled();
});
```

존재하지 않는 책을 삭제하려 하면 `NotFoundError`가 발생하고 이벤트는 발행되지 않는다. 이것은 성공/실패 경로의 이벤트 경계를 테스트로 고정한 것이다.

### 리스너 정리

Express E2E 테스트의 `afterEach`에서 `eventBus.removeAllListeners()`를 호출한다. 테스트 간 리스너가 누적되면 한 테스트에서 등록한 핸들러가 다른 테스트의 이벤트에 반응할 수 있다. 이벤트 시스템 테스트에서 격리를 보장하는 필수 작업이다.

---

## 5. 아키텍처의 확장 지점

현재 이벤트 리스너는 `console.log`만 한다. 하지만 이 구조 위에 무엇이든 올릴 수 있다:

- **감사 로그**: 누가 언제 어떤 책을 수정했는지 별도 테이블에 기록
- **알림**: 특정 장르의 새 책이 등록되면 구독자에게 이메일 발송
- **캐시 무효화**: 책이 수정/삭제되면 Redis 캐시에서 해당 항목 제거
- **비동기 처리**: 이벤트를 큐에 넣고 별도 워커에서 처리

이 중 어떤 것을 추가하더라도 `BookService`를 수정할 필요가 없다. 새 리스너를 등록하기만 하면 된다. 이것이 Open/Closed 원칙의 실전 적용이다.

---

## 에필로그: 동기에서 비동기로

이 프로젝트의 이벤트 시스템은 동기적이다. `emit` 호출 시 핸들러가 즉시 실행되고 완료된다. 같은 프로세스 안에서, 같은 스레드에서. 이것은 단순하고 디버깅이 쉽다.

하지만 서비스가 성장하면 이벤트 처리가 무거워질 수 있다. 이메일 발송에 2초가 걸린다면 API 응답도 2초 느려진다. 이때 비동기 이벤트 처리, 즉 메시지 큐가 등장한다. RabbitMQ나 Redis Pub/Sub 같은 도구가 이벤트를 프로세스 경계 너머로 운반한다.

이 프로젝트에서 동기 이벤트를 먼저 경험하는 것은, 나중에 비동기 이벤트가 왜 필요한지 체감하기 위한 준비다. 다음 프로젝트(08-production-readiness)에서는 이 이벤트 로그를 포함한 운영 수준의 로깅과 모니터링을 다룬다.
