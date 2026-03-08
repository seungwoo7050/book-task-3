# Testing Patterns — Express Database

## 테스트 전략 개요

Chapter 04에서는 데이터 영속성이 도입되었으므로, 테스트가 두 레벨로 분리된다:

| 레벨 | 대상 | 격리 방식 |
|------|------|----------|
| Unit | `BookRepository` 클래스 | In-memory SQLite 직접 사용 |
| E2E | HTTP → Controller → Service → Repository → SQLite | Supertest + In-memory SQLite |

## In-Memory SQLite 테스트 패턴

```typescript
let db: Database.Database;

beforeEach(() => {
  db = new Database(":memory:");  // 매 테스트마다 새 DB
  initDatabase(db);                // 스키마 생성
});

afterEach(() => {
  db.close();                      // 리소스 해제
});
```

### 장점
1. **완전 격리** — 각 테스트가 독립적인 빈 DB에서 실행
2. **실제 SQL** — 프로덕션과 동일한 쿼리가 실행됨 (mock 아님)
3. **빠른 속도** — 디스크 I/O 없이 메모리에서 동작
4. **정리 불필요** — 임시 파일이나 DB cleanup 로직 불필요

## Unit Test: BookRepository

Repository를 직접 테스트하여 SQL이 올바르게 동작하는지 검증한다:

```typescript
it("should create and find a book", () => {
  const book = makeBook();
  repo.create(book);
  const found = repo.findById("test-id");
  expect(found!.title).toBe("Clean Code");
  expect(found!.createdAt).toBeInstanceOf(Date);
});
```

**핵심 포인트**: `createdAt`이 `Date` 인스턴스인지 확인 → `toBook()` 매핑의 ISO 문자열 → Date 변환이 정상 동작하는지 검증.

## E2E Test: 직접 DB 검증

API 응답뿐 아니라 DB 상태도 직접 확인하는 이중 검증 패턴:

```typescript
it("should persist a book to the database", async () => {
  const createRes = await request(app).post("/books").send(validBook);
  const id = createRes.body.data.id;

  // HTTP 응답 검증
  expect(createRes.status).toBe(201);

  // DB 직접 검증
  const row = db.prepare("SELECT * FROM books WHERE id = ?").get(id);
  expect(row).toBeDefined();
});
```

### 이 패턴이 중요한 이유
- API가 200을 반환했다고 데이터가 반드시 영속된 것은 아님
- DB 핸들을 테스트에서 접근할 수 있기 때문에 가능한 기법
- 삭제 테스트에서도 DB에 실제로 없음을 확인

## Helper: makeBook 팩토리

```typescript
const makeBook = (overrides?: Partial<Book>): Book => ({
  id: "test-id",
  title: "Clean Code",
  author: "Robert C. Martin",
  publishedYear: 2008,
  genre: "Programming",
  price: 33.99,
  createdAt: new Date("2024-01-01T00:00:00Z"),
  updatedAt: new Date("2024-01-01T00:00:00Z"),
  ...overrides,
});
```

`Partial<Book>` 스프레드로 특정 필드만 오버라이드할 수 있어 테스트의 의도가 명확해진다.

## 파이프라인 통합 테스트

Ch03의 검증/에러 처리가 올바르게 유지되는지도 함께 테스트:

```typescript
it("should validate request body", async () => {
  const res = await request(app).post("/books").send({ title: "Only Title" });
  expect(res.status).toBe(400);
  expect(res.body.success).toBe(false);
});
```

DB 계층 추가로 인해 기존 파이프라인이 깨지지 않았음을 보장한다.

## 근거 요약

- 근거: [문서] `backend-architecture/04-database/README.md`
- 근거: [문서] `backend-architecture/04-database/lab-report.md`
- 근거: [문서] `backend-architecture/04-database/express-impl/docs/README.md`
- 근거: [문서] `backend-architecture/04-database/express-impl/devlog/README.md`
