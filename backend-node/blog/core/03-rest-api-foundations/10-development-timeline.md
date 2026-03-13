# 03-rest-api-foundations development timeline

`bridge`에서 프레임워크 없는 HTTP를 한 번 손으로 만져 본 뒤, 여기서 처음으로 Express와 NestJS를 나란히 세운다. 이 프로젝트의 재미는 CRUD 자체보다, 같은 문제를 두 프레임워크가 어디서부터 다르게 감싸는지가 코드 표면에 드러난다는 데 있다.

## 흐름 먼저 보기

1. Express에서 service와 router/controller 경계를 먼저 세운다.
2. NestJS에서 같은 CRUD를 decorator와 container 위로 옮긴다.
3. 두 레인이 정말 같은 계약을 통과하는지 테스트로 묶는다.

## Express에서 경계를 세운 장면

처음 비교 기준이 되는 건 `BookService`다. 이 서비스는 Express 프로젝트 안에 있지만 request/response를 전혀 모른다.

```ts
export class BookService {
  private readonly books = new Map<string, Book>();

  create(dto: CreateBookDto): Book {
    const book: Book = {
      id: randomUUID(),
      ...dto,
    };
    this.books.set(book.id, book);
    return book;
  }
}
```

이 지점이 중요한 이유는, 비교의 기준선을 HTTP가 아니라 순수 CRUD 도메인 로직에 두기 때문이다. framework choice보다 먼저 "이 문제의 핵심 로직은 어디까지인가"를 고정해 둔 셈이다.

router는 그 바깥에서 의존성을 연결한다.

```ts
export function createBookRouter(controller: BookController): Router {
  const router = Router();
  router.get("/", asyncHandler(controller.findAll));
  router.get("/:id", asyncHandler(controller.findById));
  router.post("/", asyncHandler(controller.create));
  router.put("/:id", asyncHandler(controller.update));
  router.delete("/:id", asyncHandler(controller.delete));
  return router;
}
```

Express에서는 "누가 controller를 만들고 누가 router에 꽂는가"가 이처럼 그대로 보인다. 이게 manual DI가 남기는 표면이다.

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run build && pnpm run test
Test Files  2 passed (2)
Tests       18 passed (18)
Duration    486ms
```

이 검증 결과는 Express 레인이 이미 service unit과 HTTP flow를 한 묶음으로 통과하고 있다는 신호가 된다.

## NestJS로 같은 문제를 옮긴 장면

같은 CRUD를 NestJS로 옮기면 service 책임은 크게 바뀌지 않는다. 바뀌는 건 HTTP 경계가 보이는 방식이다.

```ts
@Injectable()
export class BooksService {
  private readonly books = new Map<string, Book>();

  findOne(id: string): Book {
    const book = this.books.get(id);
    if (!book) {
      throw new NotFoundException(`Book with ID "${id}" not found`);
    }
    return book;
  }
}
```

service는 여전히 CRUD를 말하고 있지만, `undefined`를 반환하던 자리에 `NotFoundException`이 올라오면서 프레임워크 친화적인 오류 전파가 들어온다.

controller는 আরও 노골적으로 달라진다.

```ts
@Controller("books")
export class BooksController {
  constructor(private readonly booksService: BooksService) {}

  @Get(":id")
  findOne(@Param("id") id: string): Book {
    return this.booksService.findOne(id);
  }
}
```

Express에서 별도 파일이던 router가 controller 안으로 접히고, method/path 선언은 decorator가 맡는다. 즉 같은 CRUD여도 NestJS에서는 HTTP 표면이 더 안쪽으로, 더 선언적으로 들어온다.

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run build && pnpm run test && pnpm run test:e2e
Tests       8 passed (8)
test:e2e    8 passed (8)
```

여기서부터는 "둘 다 된다"가 아니라, 같은 문제를 어떤 보일러플레이트 비용으로 풀고 있는지가 비교 포인트가 된다.

## 같은 계약을 두 방식으로 고정한 장면

이 프로젝트가 설명문으로 끝나지 않는 이유는 테스트가 두 레인의 차이를 다른 방식으로 붙잡고 있기 때문이다. Express는 service unit test가 강하고, NestJS는 e2e가 더 많은 이야기를 한다.

```ts
const created = service.create(dto);
const found = service.findById(created.id);
expect(found).toEqual(created);
```

Express 쪽에서는 서비스가 HTTP 없이도 자기 계약을 지키는지를 먼저 확인한다. 반면 Nest e2e는 framework 전체를 포함한 route surface를 직접 친다.

```ts
const res = await request(app.getHttpServer()).get(`/books/${createRes.body.id}`);
expect(res.status).toBe(200);
expect(res.body.title).toBe("Test Book");
```

그래서 이 프로젝트를 다 읽고 나면 "Express vs NestJS"라는 비교가 문체나 취향 문제가 아니라, 의존성 연결과 HTTP 경계가 어디에 드러나는지의 차이로 남게 된다.

다음 프로젝트에서는 그 위에 validation, error handling, response envelope, logging 같은 공통 규약이 따로 서기 시작한다.
