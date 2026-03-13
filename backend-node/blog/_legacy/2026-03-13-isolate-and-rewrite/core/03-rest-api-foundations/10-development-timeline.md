# 03-rest-api-foundations development timeline

Bridge 단계에서는 HTTP의 기본 부품을 손으로 만져 봤다면, 여기서는 같은 Books CRUD를 Express와 NestJS로 각각 다시 풀어 보면서 계층과 DI를 비교하기 시작한다. 이 프로젝트를 읽을 때 중요한 건 endpoint 목록이 아니라 "같은 계약을 두 프레임워크가 어떤 연결 방식으로 설명하는가"다.

## 구현 순서 요약

- Express에서 composition root를 드러내는 수동 DI 구조를 먼저 만든다.
- NestJS에서 module/controller/service로 같은 CRUD 계약을 다시 세운다.
- 두 레인의 unit/e2e 테스트로 공통 Books contract를 비교한다.

## Phase 1

- 당시 목표: Express에서 service, controller, router, app 경계를 눈에 보이게 만든다.
- 변경 단위: `express/src/app.ts`, `express/src/services/book.service.ts`
- 처음 가설: 비교 학습의 출발점은 Express가 얼마나 단순한가가 아니라, 어떤 의존성이 어디서 연결되는지 노출된다는 데 있다.
- 실제 진행: `createApp()`이 `BookService`, `BookController`, `bookRouter`를 순서대로 만들고 mount하며, `BookService`는 in-memory `Map`과 `randomUUID()`로 CRUD를 처리한다.

CLI:

```bash
$ cd express
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run build
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test
✓ test/unit/book.service.test.ts (9 tests)
✓ test/e2e/books.e2e.test.ts (9 tests)
Tests 18 passed (18)
```

검증 신호:

- service unit test와 e2e가 동시에 지나가므로 Express 쪽 계약이 service와 HTTP 양쪽에서 닫힌다.
- 생성, 수정, 삭제, missing book까지 한 흐름에서 확인된다.

핵심 코드:

```ts
const bookService = new BookService();
const bookController = new BookController(bookService);
const bookRouter = createBookRouter(bookController);
app.use("/books", bookRouter);
```

왜 이 코드가 중요했는가:

Express의 핵심 비교 포인트가 여기 있다. 의존성 연결이 전부 `createApp()`에 노출돼 있어서, "어디가 composition root인가"를 말로 설명하지 않아도 코드가 바로 보여 준다.

새로 배운 것:

- 수동 DI의 장점은 간단함보다도 흐름 가시성이다. 의존성 연결이 노출돼 있으니 비교 기준이 분명해진다.

## Phase 2

- 당시 목표: NestJS에서 같은 CRUD를 decorator와 DI container 기반으로 다시 만든다.
- 변경 단위: `nestjs/src/books/books.controller.ts`, `nestjs/src/books/books.service.ts`, `nestjs/src/books/books.module.ts`
- 처음 가설: NestJS에서는 Express에서 손으로 하던 router/controller wiring이 module과 decorator로 올라갈 것이다.
- 실제 진행: `@Controller("books")` 아래에 GET/POST/PUT/DELETE를 두고, `BooksService`는 `NotFoundException`을 던지는 방식으로 실패를 처리한다.

CLI:

```bash
$ cd ../nestjs
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run build
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test:e2e
Tests 8 passed (8)
Tests 8 passed (8)
```

검증 신호:

- unit test는 service 동작을, e2e는 controller와 framework wiring을 각각 닫는다.
- `findOne`, `update`, `remove`에서 없는 책을 `NotFoundException`으로 다루는 규칙이 테스트로 이어진다.

핵심 코드:

```ts
@Controller("books")
export class BooksController {
  constructor(
    @Inject(BooksService)
    private readonly booksService: BooksService,
  ) {}
```

왜 이 코드가 중요했는가:

Express에서 composition root에 있던 wiring이 NestJS에서는 controller와 module 선언으로 흩어진다. 이 변화가 바로 framework DI가 주는 구조적 차이다.

새로 배운 것:

- NestJS의 편의는 "자동 주입"보다 "HTTP layer와 service layer를 프레임워크 문법으로 강제 분리한다"는 데 있다.

## Phase 3

- 당시 목표: 두 레인이 같은 Books 문제를 정말 같은 표면으로 닫았는지 확인한다.
- 변경 단위: `express/test/*`, `nestjs/test/*`
- 처음 가설: 비교 프로젝트는 코드 길이보다 검증 표면이 더 중요하다. 둘 다 같은 CRUD 계약을 재현하지 못하면 비교 자체가 성립하지 않는다.
- 실제 진행: Express는 unit + e2e를 한 `pnpm run test`에 묶고, NestJS는 service unit과 e2e를 나눠 같은 Books 시나리오를 검증했다.

CLI:

```bash
$ cd express && COREPACK_ENABLE_AUTO_PIN=0 pnpm run test
$ cd ../nestjs && COREPACK_ENABLE_AUTO_PIN=0 pnpm run test && COREPACK_ENABLE_AUTO_PIN=0 pnpm run test:e2e
Express: Tests 18 passed (18)
NestJS: Tests 8 passed (8) + Tests 8 passed (8)
```

검증 신호:

- CRUD 생성/조회/수정/삭제가 두 레인 모두에서 같은 문제로 통과한다.
- 달라지는 건 구현 위치와 예외 처리 방식이지, 외부 contract가 아니다.

핵심 코드:

```ts
findOne(id: string): Book {
  const book = this.books.get(id);
  if (!book) {
    throw new NotFoundException(`Book with ID "${id}" not found`);
  }
  return book;
}
```

왜 이 코드가 중요했는가:

동일한 missing-book 경계가 Express에서는 `undefined` 반환 후 controller에서 처리되고, NestJS에서는 service에서 예외를 던지는 방식으로 바뀐다. 비교 학습의 실질적인 차이가 바로 여기 있다.

새로 배운 것:

- 프레임워크 비교는 "무엇이 자동화되는가"보다 "실패를 어느 계층에서 책임지는가"를 보는 쪽이 더 선명하다.

다음:

- [`../04-request-pipeline/00-series-map.md`](../04-request-pipeline/00-series-map.md)에서 CRUD 자체보다 공통 요청 규약이 앞자리로 올라온다.
