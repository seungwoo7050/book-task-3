# Testing Patterns — NestJS Database (TypeORM)

## 테스트 전략 개요

| 레벨 | 대상 | 격리 방식 |
|------|------|----------|
| Unit | `BooksService` + 실제 TypeORM Repository | `Test.createTestingModule` + `:memory:` DB |
| E2E | HTTP → Pipe → Controller → Service → Repository → SQLite | NestJS App + Supertest + `:memory:` DB |

## NestJS 테스트 모듈 패턴

```typescript
beforeEach(async () => {
  module = await Test.createTestingModule({
    imports: [
      TypeOrmModule.forRoot({
        type: "better-sqlite3",
        database: ":memory:",
        entities: [Book],
        synchronize: true,   // 테스트에서 자동 스키마 생성
      }),
      BooksModule,
    ],
  }).compile();

  service = module.get(BooksService);
});

afterEach(async () => {
  await module.close();     // DataSource 정리
});
```

### Express와의 차이
- Express: `new Database(":memory:")` → `db.close()`
- NestJS: `Test.createTestingModule()` → `module.close()`
- NestJS에서는 TypeORM이 connection lifecycle을 관리

## Unit Test: BooksService

실제 TypeORM Repository와 함께 Service를 테스트한다 (mock 없음):

```typescript
it("should create and find a book", async () => {
  const book = await service.create(dto);
  expect(book.id).toBeDefined();

  const found = await service.findOne(book.id);
  expect(found.title).toBe("Clean Code");
});
```

**mock을 사용하지 않는 이유**: In-memory SQLite가 충분히 빠르고, ORM 매핑 오류를 실제로 검출할 수 있기 때문이다.

## E2E Test: 전체 파이프라인

```typescript
beforeEach(async () => {
  app = moduleFixture.createNestApplication();
  app.useGlobalPipes(new ValidationPipe({ ... }));
  app.useGlobalFilters(new HttpExceptionFilter());
  app.useGlobalInterceptors(new TransformInterceptor());
  await app.init();
});
```

E2E 테스트에서는 프로덕션과 동일한 Pipe/Filter/Interceptor를 등록하여 실제 환경을 재현한다.

## Express E2E vs NestJS E2E

| 비교 항목 | Express | NestJS |
|----------|---------|--------|
| DB 직접 검증 | ✅ `db.prepare().get()` | ❌ TypeORM Repository 통해서만 |
| 설정 복잡도 | 낮음 (3줄) | 높음 (module + pipes + filters) |
| 리소스 정리 | `db.close()` | `module.close()` (async) |
| 격리 보장 | 개발자 책임 | 프레임워크가 DI 스코프 관리 |

Express E2E는 DB 핸들을 직접 보유하고 있어 SQL로 데이터를 직접 검증할 수 있다. NestJS E2E는 HTTP 응답만으로 검증해야 한다.

## NotFoundException 검증

```typescript
it("should throw NotFoundException", async () => {
  await expect(service.findOne("nonexistent"))
    .rejects.toThrow(NotFoundException);
});
```

NestJS에서는 `NotFoundException`이 `HttpException`을 상속하므로, ExceptionFilter가 자동으로 404 응답을 생성한다. Unit test에서는 예외 자체를, E2E test에서는 HTTP 404 응답을 검증한다.

## 테스트 데이터 전략

Express는 `makeBook()` 팩토리로 완전한 `Book` 객체를 생성하지만, NestJS는 DTO만 제공하고 나머지(id, timestamps)는 Service와 TypeORM이 자동 생성한다:

```typescript
// Express: 완전한 Book 객체
const makeBook = (): Book => ({ id: "test-id", title: ..., createdAt: ... });

// NestJS: DTO만 제공
const dto = { title: "Clean Code", author: "Robert C. Martin", ... };
```

이 차이는 TypeORM의 `@CreateDateColumn()`/`@UpdateDateColumn()`이 타임스탬프를 자동 관리하기 때문이다.

## 근거 요약

- 근거: [문서] `backend-architecture/04-database/README.md`
- 근거: [문서] `backend-architecture/04-database/lab-report.md`
- 근거: [문서] `backend-architecture/04-database/nestjs-impl/docs/README.md`
- 근거: [문서] `backend-architecture/04-database/nestjs-impl/devlog/README.md`
