# NestJS Testing Patterns

## Overview

NestJS는 `@nestjs/testing` 패키지를 통해 강력한 테스트 유틸리티를 제공한다. Express에서 `createApp()` 팩토리를 사용한 것처럼, NestJS에서는 `Test.createTestingModule()`로 격리된 테스트 모듈을 생성한다.

## 1. 유닛 테스트 — Service Layer

Service 클래스는 NestJS 프레임워크와 얕게 결합되어 있으므로(`@Injectable()` 데코레이터만 사용), 프레임워크 없이도 직접 인스턴스를 생성하여 테스트할 수 있다.

```typescript
import { describe, it, expect, beforeEach } from "vitest";
import { BooksService } from "../../src/books/books.service";
import { NotFoundException } from "@nestjs/common";

describe("BooksService", () => {
  let service: BooksService;

  beforeEach(() => {
    service = new BooksService();
  });

  it("findAll은 빈 배열을 반환한다", () => {
    expect(service.findAll()).toEqual([]);
  });

  it("findOne은 존재하지 않는 ID에 NotFoundException을 던진다", () => {
    expect(() => service.findOne("invalid")).toThrow(NotFoundException);
  });
});
```

### Express와의 차이점

| 항목 | Express (BookService) | NestJS (BooksService) |
|------|----------------------|----------------------|
| 존재하지 않는 리소스 | `undefined` 반환 | `NotFoundException` throw |
| 테스트 검증 방식 | `expect(result).toBeUndefined()` | `expect(() => ...).toThrow()` |
| DI 데코레이터 | 없음 | `@Injectable()` (테스트에 영향 없음) |

## 2. E2E 테스트 — Testing Module

NestJS E2E 테스트는 `@nestjs/testing`의 `Test.createTestingModule()`을 사용한다:

```typescript
import { Test, TestingModule } from "@nestjs/testing";
import { INestApplication } from "@nestjs/common";
import request from "supertest";
import { AppModule } from "../../src/app.module";

describe("Books API (E2E)", () => {
  let app: INestApplication;

  beforeEach(async () => {
    const moduleFixture: TestingModule = await Test.createTestingModule({
      imports: [AppModule],
    }).compile();

    app = moduleFixture.createNestApplication();
    await app.init();
  });

  afterEach(async () => {
    await app.close();
  });

  it("GET /books → 200, 빈 배열", () => {
    return request(app.getHttpServer())
      .get("/books")
      .expect(200)
      .expect([]);
  });
});
```

### Express E2E와 비교

```typescript
// Express: 동기적, 즉시 사용 가능
const app = createApp();
await request(app).get("/books");

// NestJS: 비동기 초기화 필요
const module = await Test.createTestingModule({ ... }).compile();
const app = module.createNestApplication();
await app.init();
await request(app.getHttpServer()).get("/books");
```

NestJS는 모듈 컴파일과 앱 초기화가 비동기로 이루어지므로 `beforeEach`도 `async`여야 하고, `afterEach`에서 `app.close()`를 호출해야 한다.

## 3. Provider Mocking

NestJS 테스트 모듈에서는 `.overrideProvider()`로 의존성을 쉽게 교체할 수 있다:

```typescript
const module = await Test.createTestingModule({
  imports: [BooksModule],
})
  .overrideProvider(BooksService)
  .useValue({
    findAll: () => [{ id: "1", title: "Mock Book" }],
  })
  .compile();
```

Express에서 mock을 수동으로 주입하는 것과 비교하면, NestJS는 DI 컨테이너 레벨에서 교체가 이루어지므로 **모든 의존 그래프**가 자동으로 업데이트된다.

## 테스트 구성

```
test/
├── unit/
│   └── books.service.test.ts    # Service 유닛 테스트
└── e2e/
    └── books.e2e.test.ts        # HTTP 전체 사이클 테스트
```

## 참고 자료

- [NestJS Testing](https://docs.nestjs.com/fundamentals/testing)
- [Vitest Documentation](https://vitest.dev/)
- [Supertest GitHub](https://github.com/ladjs/supertest)

## 근거 요약

- 근거: [문서] `backend-architecture/01-rest-api/README.md`
- 근거: [문서] `backend-architecture/01-rest-api/lab-report.md`
- 근거: [문서] `backend-architecture/01-rest-api/nestjs-impl/docs/README.md`
- 근거: [문서] `backend-architecture/01-rest-api/nestjs-impl/devlog/README.md`
