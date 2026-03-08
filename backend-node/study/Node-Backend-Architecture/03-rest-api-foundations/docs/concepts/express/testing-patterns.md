# Testing Patterns for Express REST APIs

## Overview

Express 애플리케이션의 테스트 전략은 크게 **유닛 테스트**와 **E2E(End-to-End) 테스트** 두 가지로 나뉜다. 레이어드 아키텍처를 따를 경우, 각 레이어를 독립적으로 테스트할 수 있다는 것이 핵심 이점이다.

## 테스트 레벨 구분

```
┌───────────────────────────────────┐
│  E2E Tests (supertest)           │   HTTP 요청 → 응답 전체 사이클
│  ┌─────────────────────────────┐ │
│  │  Integration Tests          │ │   Controller + Service 연동
│  │  ┌───────────────────────┐  │ │
│  │  │  Unit Tests           │  │ │   Service 단독 로직 검증
│  │  └───────────────────────┘  │ │
│  └─────────────────────────────┘ │
└───────────────────────────────────┘
```

## 1. 유닛 테스트 — Service Layer

Service는 HTTP 의존이 없으므로 가장 테스트하기 쉽다. `new BookService()`로 인스턴스를 만들고 메서드를 직접 호출한다.

```typescript
import { describe, it, expect, beforeEach } from "vitest";
import { BookService } from "../../src/services/book.service";

describe("BookService", () => {
  let service: BookService;

  beforeEach(() => {
    service = new BookService(); // 매 테스트마다 새 인스턴스
  });

  it("빈 상태에서 findAll은 빈 배열을 반환한다", () => {
    expect(service.findAll()).toEqual([]);
  });

  it("create 후 findById로 찾을 수 있다", () => {
    const created = service.create({
      title: "Test", author: "A", publishedYear: 2024, genre: "G", price: 10
    });
    expect(service.findById(created.id)).toEqual(created);
  });
});
```

### 핵심 포인트
- `beforeEach`에서 새 인스턴스를 생성해 테스트 간 상태 격리
- in-memory `Map`이므로 외부 DB mock이 불필요
- 경계 조건 테스트: 존재하지 않는 ID, 부분 업데이트, 삭제 후 재조회

## 2. E2E 테스트 — Supertest

[supertest](https://github.com/ladjs/supertest)는 Express 앱을 메모리에서 띄우고 실제 HTTP 요청을 보내는 라이브러리이다. 서버를 별도 포트에 바인딩하지 않아도 된다.

```typescript
import request from "supertest";
import { createApp } from "../../src/app";

describe("Books API (E2E)", () => {
  let app: Express;

  beforeEach(() => {
    app = createApp(); // 매 테스트마다 깨끗한 앱
  });

  it("POST → GET 흐름 검증", async () => {
    const createRes = await request(app)
      .post("/books")
      .send({ title: "Clean Code", author: "R. Martin", ... });

    expect(createRes.status).toBe(201);

    const getRes = await request(app).get(`/books/${createRes.body.id}`);
    expect(getRes.status).toBe(200);
    expect(getRes.body.title).toBe("Clean Code");
  });
});
```

### `createApp()` 팩토리 패턴

`createApp()`은 호출할 때마다 **완전히 새로운** Express 앱 인스턴스를 생성한다. 이것이 중요한 이유:

1. **상태 격리** — 각 테스트가 빈 데이터 저장소에서 시작
2. **독립적 DI** — 테스트별로 다른 의존성을 주입할 수 있음
3. **병렬 실행 안전** — 공유 상태가 없으므로 동시 실행 가능

## 3. Controller 유닛 테스트 (Mock Service)

DI 패턴 덕분에 Service를 mock으로 교체해 Controller만 테스트할 수 있다:

```typescript
const mockService = {
  findAll: vi.fn().mockReturnValue([{ id: "1", title: "Mock Book" }]),
  findById: vi.fn(),
  create: vi.fn(),
  update: vi.fn(),
  delete: vi.fn(),
};

const controller = new BookController(mockService as any);
```

이 접근법은 Service 로직에 의존하지 않고 Controller의 HTTP 변환 로직만 검증한다.

## Vitest 설정

```typescript
// vitest.config.ts
import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    globals: true,
    environment: "node",
  },
});
```

## 테스트 실행 명령어

```bash
pnpm run test          # 모든 테스트
pnpm run test:unit     # 유닛 테스트만
pnpm run test:e2e      # E2E 테스트만
pnpm run test -- --watch  # watch 모드
```

## 참고 자료

- [Vitest Documentation](https://vitest.dev/)
- [Supertest GitHub](https://github.com/ladjs/supertest)
- [Testing Express with Supertest — Best Practices](https://expressjs.com/en/guide/testing.html)

## 근거 요약

- 근거: [문서] `backend-architecture/01-rest-api/README.md`
- 근거: [문서] `backend-architecture/01-rest-api/lab-report.md`
- 근거: [문서] `backend-architecture/01-rest-api/express-impl/docs/README.md`
- 근거: [문서] `backend-architecture/01-rest-api/express-impl/devlog/README.md`
