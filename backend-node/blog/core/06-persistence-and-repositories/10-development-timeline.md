# 06-persistence-and-repositories development timeline

이 프로젝트에 오면 새로운 API를 더 만드는 대신, 같은 API를 다른 저장 전략 위에서 계속 살려 두는 일이 중심이 된다. 그래서 읽는 순서도 controller보다 database init과 repository 쪽에서 시작하는 편이 훨씬 자연스럽다.

## 흐름 먼저 보기

1. Express에서 SQLite 초기화와 raw SQL repository를 만든다.
2. NestJS에서는 ORM repository 주입으로 같은 CRUD를 유지한다.
3. unit/e2e로 바깥 계약이 흔들리지 않았는지 확인한다.

## SQLite 경계를 세운 장면

처음 전환점은 `createDatabase`가 생기는 순간이다. 이 함수가 등장하면서 DB 설정과 schema 초기화가 애플리케이션 다른 계층과 분리된다.

```ts
export function createDatabase(filename: string = ":memory:"): Database.Database {
  const db = new Database(filename);
  db.pragma("journal_mode = WAL");
  db.pragma("foreign_keys = ON");
  initDatabase(db);
  return db;
}
```

여기서 중요한 건 WAL이 어떤 의미를 갖는지 장황하게 설명하는 게 아니다. 이 설정이 controller나 service가 아니라 database bootstrap에 머문다는 사실이 핵심이다. persistence concern이 어디까지인지 분명하게 나눠 둔 셈이기 때문이다.

그 바로 아래에서 repository가 raw SQL을 떠안는다.

```ts
findById(id: string): Book | null {
  const row = this.db.prepare("SELECT * FROM books WHERE id = ?").get(id) as BookRow | undefined;
  return row ? this.toBook(row) : null;
}
```

이 메서드가 중요한 이유는, 이제 service는 SQL을 모르고도 `Book | null` 계약만 보면 되기 때문이다. 저장 전략은 바뀌었지만 상위 계층이 보는 문제 정의는 그대로 남는다.

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run build && pnpm run test && pnpm run test:e2e
Tests       7 passed (7)
test:e2e    6 passed (6)
```

## Nest ORM으로 같은 swap을 한 장면

NestJS 쪽에서는 같은 실험을 TypeORM 위에서 반복한다. 흥미로운 건 service가 생각보다 많이 바뀌지 않는다는 점이다.

```ts
constructor(
  @InjectRepository(Book)
  private readonly bookRepository: Repository<Book>,
) {}

async create(dto: CreateBookDto): Promise<Book> {
  const book = this.bookRepository.create({
    id: crypto.randomUUID(),
    ...dto,
  });
  return this.bookRepository.save(book);
}
```

raw SQL이 사라지고 `save`가 들어왔지만, service는 여전히 create/find/update/remove라는 같은 언어를 쓴다. 이게 바로 persistence swap이 API rewrite와 다른 이유다.

목록 조회도 같은 흐름을 유지한다.

```ts
async findAll(): Promise<Book[]> {
  return this.bookRepository.find({ order: { createdAt: "DESC" } });
}
```

즉 persistence 세부 사항은 repository call 안으로 접히고, controller는 여전히 CRUD contract만 상대한다.

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run build && pnpm run test && pnpm run test:e2e
Tests       5 passed (5)
test:e2e    6 passed (6)
```

## 계약이 안 흔들렸는지 확인한 장면

저장 전략이 바뀌었을 때 가장 먼저 불안해지는 건 API contract다. 그래서 이 프로젝트의 마지막 장면은 repository unit test와 e2e를 나란히 두는 데서 나온다.

```ts
repo.create(makeBook());
const found = repo.findById("test-id");
expect(found!.createdAt).toBeInstanceOf(Date);
```

Express unit test는 DB row가 domain object로 제대로 돌아오는지 확인한다. 반면 Nest e2e는 persistence가 붙어도 HTTP 표면이 그대로인지 본다.

```ts
const res = await request(app.getHttpServer()).post("/books").send(validBook);
expect(res.body.success).toBe(true);
const getRes = await request(app.getHttpServer()).get(`/books/${id}`);
expect(getRes.body.data.title).toBe("Clean Code");
```

이 두 검증이 같이 있어야 "저장 계층만 바뀌었다"는 말이 진짜가 된다. 안쪽에서는 repository mapping을 보고, 바깥에서는 CRUD와 validation, 404 응답이 그대로인지 본다.

여기까지 오면 이 프로젝트의 요점은 분명해진다. persistence migration은 SQL 실습이 아니라, 경계를 얼마나 잘 지키고 있었는지를 확인하는 시험이었다. 다음 프로젝트에서는 그 위에 domain event 계층이 올라온다.
