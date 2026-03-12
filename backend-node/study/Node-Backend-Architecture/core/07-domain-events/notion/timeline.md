# 07-domain-events — 개발 타임라인

> 소스 코드에 남지 않는 개발 과정을 시간순으로 기록한다.

---

## Phase 1: 프로젝트 구조 확장

이 프로젝트는 06-persistence-and-repositories의 코드베이스 위에 이벤트 시스템을 추가한다. 기존 영속 계층(better-sqlite3, TypeORM)은 그대로 유지된다.

### 1-1. 새 디렉토리 생성

Express 쪽:
```bash
mkdir -p express/src/events
mkdir -p express/src/types   # 이미 존재하면 생략
```

NestJS 쪽:
```bash
mkdir -p nestjs/src/events
```

### 1-2. 의존성 추가

Express 쪽은 `node:events` 빌트인 모듈만 사용하므로 추가 설치 없음.

NestJS 쪽:
```bash
cd nestjs/
pnpm add @nestjs/event-emitter
```

`@nestjs/event-emitter`는 내부적으로 `eventemitter2` 패키지에 의존한다. 별도 설치 불필요.

### 1-3. better-sqlite3 빌드 (06에서 이어짐)

```bash
pnpm install
pnpm approve-builds
pnpm rebuild better-sqlite3
```

이 과정은 프로젝트 06과 동일하다. CI/CD에서도 매번 실행해야 한다.

---

## Phase 2: Express 레인 — 이벤트 시스템 구현

### 2-1. 이벤트 타입 정의

`src/types/events.ts` 생성:

- `BookCreatedEvent`, `BookUpdatedEvent`, `BookDeletedEvent` 인터페이스 정의
- `EventMap` 인터페이스로 이벤트 이름과 페이로드를 매핑
- 모든 필드에 `readonly` 적용 — 이벤트는 불변 데이터

설계 결정: 이벤트 이름을 `"book.created"` 형태의 도트 구분 문자열로 통일. 이 관례는 NestJS, RabbitMQ 등에서도 일반적이다.

### 2-2. EventBus 클래스

`src/events/event-bus.ts` 생성:

- `EventEmitter`를 `private` 프로퍼티로 감쌈
- `emit<K>`, `on<K>`, `off<K>`, `removeAllListeners` — 네 개 메서드만 노출
- 제네릭 시그니처 `<K extends keyof EventMap>`으로 타입 체크

검증:
```bash
# TypeScript 컴파일 시 잘못된 이벤트 페이로드에 타입 에러 발생하는지 확인
pnpm run build
```

### 2-3. BookEventListener 클래스

`src/events/book-event-listener.ts` 생성:

- 생성자에서 `registerListeners()` 호출 → 세 이벤트에 핸들러 바인딩
- 각 핸들러에 `try/catch` — 리스너 에러가 발행자에게 전파되지 않도록
- `bind(this)` 필수 — 클래스 메서드를 콜백으로 전달할 때 `this` 바인딩

### 2-4. BookService 수정

기존 `BookService`의 변경 사항:

1. 생성자에 `EventBus` 파라미터 추가
2. `create()` 끝에 `this.eventBus.emit("book.created", ...)` 추가
3. `update()` 끝에 `this.eventBus.emit("book.updated", ...)` 추가 — `changes`는 `Object.keys(dto)`
4. `delete()` 끝에 `this.eventBus.emit("book.deleted", ...)` 추가

핵심 원칙: 이벤트 발행은 **DB 연산 성공 후**에만 실행. 예외가 발생하면 emit에 도달하지 않음.

### 2-5. 의존성 조립 업데이트

`src/routes/book.router.ts` 수정:

```
createBookRouter(db, eventBus)
```

`EventBus`가 외부에서 주입되도록 시그니처 변경.

`src/app.ts` 수정:

```
createApp(db, eventBus)
```

`src/main.ts` 수정 — `EventBus` 인스턴스 생성 + `BookEventListener` 생성 후 서버 시작.

---

## Phase 3: NestJS 레인 — @nestjs/event-emitter 도입

### 3-1. AppModule 수정

`src/app.module.ts`에 `EventEmitterModule.forRoot()` 추가:

```typescript
imports: [
  TypeOrmModule.forRoot({...}),
  EventEmitterModule.forRoot(),   // ← 추가
  BooksModule,
  EventsModule,                    // ← 추가
]
```

`EventEmitterModule.forRoot()`은 `EventEmitter2` 인스턴스를 DI에 등록한다.

### 3-2. 이벤트 클래스 정의

`src/events/events.ts` 생성:

- `BookCreatedEvent`, `BookUpdatedEvent`, `BookDeletedEvent` — 클래스로 정의
- `timestamp`의 기본값: `new Date()` (생성자 파라미터 기본값)
- Express의 인터페이스와 달리 클래스 → `instanceof` 체크 가능

### 3-3. BookEventListener

`src/events/book-event.listener.ts` 생성:

- `@Injectable()` + `@OnEvent("book.created")` 데코레이터
- Express의 수동 `.on()` 등록이 데코레이터로 대체
- NestJS가 모듈 초기화 시 자동으로 리스너 등록

### 3-4. EventsModule

`src/events/events.module.ts` 생성:

- `BookEventListener`를 provider 및 export로 등록
- `AppModule`이 이 모듈을 import해야 리스너가 활성화

### 3-5. BooksService 수정

기존 `BooksService` 변경:

1. `@Inject(EventEmitter2)` 추가
2. `create()` 후 `this.eventEmitter.emit("book.created", new BookCreatedEvent(...))`
3. `update()` — 변경된 키 계산 후 `BookUpdatedEvent` 발행
4. `remove()` 후 `BookDeletedEvent` 발행

---

## Phase 4: 테스트 전략

### 4-1. Express 단위 테스트 — EventBus

`test/unit/event-bus.test.ts`:

```bash
pnpm run test
```

- `vi.fn()`으로 스파이 핸들러 생성
- `bus.emit` 후 `handler`가 호출되었는지. 올바른 데이터가 전달되었는지
- 복수 리스너 테스트, `off` 해제 테스트
- 테스트마다 새 `EventBus` 인스턴스 (`beforeEach`)

### 4-2. Express E2E 테스트 — 완전한 흐름

`test/e2e/events.e2e.test.ts`:

```bash
pnpm run test:e2e
```

- `createApp(db, eventBus)` — 인메모리 DB + EventBus 모두 테스트 전용
- `vi.fn()` 핸들러를 eventBus에 등록 → HTTP 요청 → 핸들러 호출 확인
- **실패 경로 테스트**: `DELETE /books/nonexistent` 시 이벤트 미발행 검증
- `afterEach`에서 `eventBus.removeAllListeners()` — 테스트 간 리스너 격리

### 4-3. NestJS 단위 테스트

`test/unit/books.service.test.ts`:

```bash
pnpm run test
```

- `Test.createTestingModule`으로 인메모리 DB + EventEmitterModule 구성
- Service를 통한 CRUD 후 이벤트 발행 확인

`test/unit/book-event.listener.test.ts`:

- `BookEventListener`의 핸들러를 직접 호출하여 로직 검증

### 4-4. NestJS E2E 테스트

`test/e2e/events.e2e.test.ts`:

```bash
pnpm run test:e2e
```

- NestJS 앱 전체를 띄우고 HTTP 요청 → 이벤트 검증

---

## Phase 5: 빌드 및 검증

### 전체 검증 순서

Express:
```bash
cd express/
pnpm install && pnpm approve-builds && pnpm rebuild better-sqlite3
pnpm run build
pnpm run test
pnpm run test:e2e
```

NestJS:
```bash
cd nestjs/
pnpm install && pnpm approve-builds && pnpm rebuild better-sqlite3
pnpm run build
pnpm run test
pnpm run test:e2e
```

### 수동 검증

```bash
# 서버 실행
pnpm run start

# POST 요청 보내고 콘솔에 [Event] 로그가 출력되는지 확인
curl -X POST http://localhost:3000/books \
  -H "Content-Type: application/json" \
  -d '{"title":"Event Test","author":"Dev","publishedYear":2024,"genre":"Tech","price":19.99}'

# 콘솔 출력 예시:
# [Event] Book created: "Event Test" by Dev (xxxx-xxxx-xxxx)
```

---

## 도구 및 커맨드 요약

| 도구/커맨드 | 용도 |
|-------------|------|
| `pnpm add @nestjs/event-emitter` | NestJS 이벤트 모듈 설치 |
| `node:events` (EventEmitter) | Express 이벤트 버스 기반 (빌트인) |
| `vi.fn()` | 이벤트 핸들러 스파이 생성 (Vitest) |
| `removeAllListeners()` | 테스트 간 리스너 격리 |
| `pnpm run test` | 단위 테스트 |
| `pnpm run test:e2e` | E2E 테스트 |

## 핵심 파일 생성 순서 (Express)

```
types/events.ts → events/event-bus.ts → events/book-event-listener.ts
→ services/book.service.ts (수정) → routes/book.router.ts (수정)
→ app.ts (수정) → main.ts (수정)
→ test/unit/event-bus.test.ts → test/e2e/events.e2e.test.ts
```

## 핵심 파일 생성 순서 (NestJS)

```
events/events.ts → events/book-event.listener.ts → events/events.module.ts
→ books/books.service.ts (수정) → app.module.ts (수정)
→ test/unit/ → test/e2e/
```
