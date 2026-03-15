# 03-rest-api-foundations development timeline

`bridge` 구간에서는 frameworkless HTTP로 request/response를 직접 다뤘다. 이 lab부터는 같은 Books CRUD를 두 프레임워크에 올려 보면서, 프레임워크가 무엇을 대신해 주고 무엇은 여전히 직접 설계해야 하는지 비교하게 된다. 이번 재검토에서는 "Express vs NestJS"라는 익숙한 구도를 반복하기보다, 두 구현이 실제로 어떤 계약을 검증하고 무엇을 아직 검증하지 않는지부터 다시 정리했다.

## 흐름 먼저 보기

1. Express lane에서 manual composition root와 controller/router 분리를 확인한다.
2. NestJS lane에서 module, decorator, exception 기반 flow로 같은 CRUD를 다시 읽는다.
3. 두 lane 모두 테스트는 통과하지만 runtime validation은 아직 비어 있음을 별도 재실행으로 확인한다.

## Express에서 경계를 손으로 세운 장면

Express 쪽의 출발점은 `createApp()`이다. 여기서 서비스와 컨트롤러와 라우터를 프레임워크 대신 직접 연결한다.

```ts
export function createApp() {
  const app = express();
  const bookService = new BookService();
  const bookController = new BookController(bookService);

  app.use(express.json());
  app.use("/books", createBookRouter(bookController));
  ...
}
```

이 장면이 중요한 이유는 "누가 의존성을 만들고 누가 HTTP에 꽂는가"가 코드 표면에 남기 때문이다. `BookService`는 in-memory `Map`과 `randomUUID()`만 알고 있고, HTTP는 controller/router 바깥에서 덧씌워진다.

```ts
export class BookService {
  private readonly books = new Map<string, Book>();

  create(dto: CreateBookDto): Book {
    const book: Book = { id: randomUUID(), ...dto };
    this.books.set(book.id, book);
    return book;
  }
}
```

router는 다시 `asyncHandler()`를 써서 Express 비동기 오류 전달을 수동으로 정리한다.

```ts
router.get("/", asyncHandler(controller.findAll));
router.get("/:id", asyncHandler(controller.findById));
router.post("/", asyncHandler(controller.create));
router.put("/:id", asyncHandler(controller.update));
router.delete("/:id", asyncHandler(controller.delete));
```

여기까지 보면 Express lane의 핵심은 CRUD 기능보다 수동 composition과 명시적인 request pipeline에 있다. 프레임워크가 숨겨 주지 않는 대신, 연결 지점을 모두 직접 볼 수 있다.

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run build
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test
Test Files  2 passed (2)
Tests       18 passed (18)
```

unit 9개와 e2e 9개가 모두 통과하므로, 현재 Express lane은 service 계약과 HTTP surface를 함께 유지하고 있다는 점까지는 확인된다.

## NestJS에서 같은 경계를 프레임워크 안으로 옮긴 장면

NestJS로 넘어오면 service의 책임 자체는 크게 달라지지 않는다. 대신 controller 선언, 의존성 주입, 예외 전파가 프레임워크 표면 안으로 들어간다.

```ts
@Module({
  controllers: [BooksController],
  providers: [BooksService],
})
export class BooksModule {}
```

controller는 route 등록과 parameter binding을 decorator로 표현한다.

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

service도 CRUD 자체는 비슷하지만, 없는 리소스를 만났을 때 Express처럼 `undefined`를 올리지 않고 Nest exception을 던진다.

```ts
findOne(id: string): Book {
  const book = this.books.get(id);
  if (!book) {
    throw new NotFoundException(`Book with ID "${id}" not found`);
  }
  return book;
}
```

이 차이 덕분에 비교 포인트가 선명해진다. Express는 composition root와 error forwarding을 직접 보여 주고, NestJS는 module/DI/decorator가 그 반복 작업을 프레임워크 안으로 흡수한다.

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run build
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test:e2e
Tests       8 passed (8)
```

Nest unit 8개와 e2e 8개가 모두 통과하므로, route surface와 `NotFoundException -> 404` 흐름은 현재 구현에서 안정적이라고 볼 수 있다.

## 테스트가 말해 주지 않는 빈칸을 다시 확인한 장면

이번 lab에서 가장 중요한 재확인 포인트는 둘 다 "DTO가 있으니 validation도 있겠지"라고 착각하기 쉽다는 점이었다. 실제 코드를 보면 Express DTO는 타입 별칭일 뿐이고, NestJS DTO 클래스도 `class-validator` decorator가 없으며 `main.ts`에도 `ValidationPipe`가 없다.

그래서 빌드 후 직접 빈 제목 payload를 보내 봤다.

```bash
$ node -e "const request=require('supertest'); const {createApp}=require('./dist/app.js'); request(createApp()).post('/books').send({title:''}).end((_,res)=>console.log(res.status,res.body))"
201 { id: '...', title: '' }
```

```bash
$ node -e "require('reflect-metadata'); ... request(app.getHttpServer()).post('/books').send({title:''}) ..."
201 { id: '...', title: '' }
```

즉 이 lab은 "Express와 NestJS가 validation을 어떻게 다르게 제공하는가"를 보여 주는 단계가 아니라, 아직 둘 다 CRUD 골격과 404 계약까지만 고정한 단계다. validation은 다음 pipeline lab에서 별도 규약으로 세워야 할 일로 남아 있다.

## 여기서 남는 것

이 문서를 다시 쓰고 나니, 핵심 비교는 더 단순해졌다. Express와 NestJS의 차이는 CRUD 기능 그 자체가 아니라, 같은 CRUD를 둘러싼 의존성 연결 방식과 HTTP 표면의 선언 방식에 있다. 그리고 둘 다 아직 payload validation은 넣지 않았다는 사실을 함께 봐야, 다음 `04-request-pipeline`에서 왜 validation과 error envelope가 주제가 되는지 자연스럽게 이어진다.
