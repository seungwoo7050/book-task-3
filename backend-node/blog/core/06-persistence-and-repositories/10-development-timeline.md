# 06-persistence-and-repositories development timeline

`05-auth-and-authorization`까지는 request와 role 경계를 다뤘다면, 이 lab은 그 바깥 계약을 유지한 채 안쪽 저장 전략을 교체하는 단계다. 이번 재검토에서는 "SQLite를 배운다"는 설명보다, raw SQL과 ORM이 어디서 상위 계층을 보호하는지, 그리고 기본 실행값과 테스트 전략이 어디서 서로 달라지는지에 집중해 다시 정리했다.

## 흐름 먼저 보기

1. Express에서 DB bootstrap과 raw SQL repository를 분리해 persistence concern을 안쪽으로 가둔다.
2. NestJS에서 entity metadata와 framework repository로 같은 CRUD 계약을 유지한다.
3. 테스트 격리와 native dependency 준비 상태를 다시 확인해, 이 lab이 실제로 무엇을 보장하는지 분리한다.

## Express에서 SQL과 row mapping을 안쪽으로 밀어 넣은 장면

Express 쪽의 첫 전환점은 `createDatabase()`가 생기는 순간이다.

```ts
export function createDatabase(filename: string = ":memory:"): Database.Database {
  const db = new Database(filename);
  db.pragma("journal_mode = WAL");
  db.pragma("foreign_keys = ON");
  initDatabase(db);
  return db;
}
```

이 코드가 중요한 이유는 WAL 자체의 성능 특성보다, 이런 설정이 controller나 service가 아니라 DB bootstrap 경계에 머문다는 데 있다. persistence concern이 바깥으로 새지 않게 막는 첫 번째 장치다.

실제 런타임 기본값도 여기서 갈린다. `express/src/main.ts`는 `process.env.DB_PATH || "bookstore.db"`를 쓰므로, 별도 설정이 없으면 Express는 파일 기반 SQLite를 연다.

```ts
const DB_PATH = process.env.DB_PATH || "bookstore.db";
const db = createDatabase(DB_PATH);
```

raw SQL은 `BookRepository` 안으로 더 깊게 들어간다.

```ts
findById(id: string): Book | null {
  const row = this.db.prepare("SELECT * FROM books WHERE id = ?").get(id) as BookRow | undefined;
  return row ? this.toBook(row) : null;
}
```

```ts
private toBook(row: BookRow): Book {
  return {
    id: row.id,
    title: row.title,
    author: row.author,
    publishedYear: row.published_year,
    genre: row.genre,
    price: row.price,
    createdAt: new Date(row.created_at),
    updatedAt: new Date(row.updated_at),
  };
}
```

이 row-to-domain mapping이 있기 때문에 service는 SQL column 이름이나 `TEXT/REAL/INTEGER` 저장 형식을 몰라도 된다. 상위 계층은 여전히 `Book`만 본다.

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run build
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test:e2e
Test Files  2 passed (2)
Tests       13 passed (13)
```

Express 검증은 repository unit 7개와 e2e 6개가 모두 통과했다. 그리고 e2e는 `new Database(":memory:")` 뒤 `initDatabase(db)`를 직접 호출해 테스트마다 완전히 깨끗한 DB를 만든다. 덕분에 CRUD contract와 persistence 연결이 함께 검증된다.

다만 이 점은 동시에 한계도 알려 준다. 테스트는 `createDatabase()`가 아니라 `initDatabase()`를 직접 호출하므로 `journal_mode = WAL`과 `foreign_keys = ON` 경로 자체는 현재 테스트가 고정하지 않는다. 이 부분은 source-based fact로 남겨야 정확하다.

## NestJS에서 같은 교체를 ORM 경계로 옮긴 장면

NestJS 쪽에서는 같은 실험이 TypeORM으로 옮겨 간다. `AppModule`은 driver와 entity를 등록한다.

```ts
TypeOrmModule.forRoot({
  type: "better-sqlite3",
  database: process.env.DB_PATH || ":memory:",
  entities: [Book],
  synchronize: true,
})
```

여기서도 중요한 건 기능보다 기본값이다. NestJS는 `DB_PATH`가 없으면 기본이 `:memory:`이므로, Express와 달리 아무 설정 없이 실행하면 재시작 persistence가 남지 않는다. 즉 "둘 다 SQLite"라는 말만으로는 런타임 기본 동작까지 같다고 할 수 없다.

그 대신 entity와 framework repository 덕분에 service 코드는 훨씬 높은 수준의 추상화에 머문다.

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

`Book` entity가 컬럼 정의와 timestamp 전략을 들고 있기 때문에,

```ts
@Entity("books")
export class Book {
  @PrimaryColumn("text")
  id!: string;

  @CreateDateColumn({ type: "datetime" })
  createdAt!: Date;

  @UpdateDateColumn({ type: "datetime" })
  updatedAt!: Date;
}
```

service는 raw SQL 대신 `find`, `findOneBy`, `save`, `remove` 같은 TypeORM repository 언어만 알면 된다. 즉 Express가 "직접 mapping해서 경계를 세운다"면, NestJS는 "ORM 메타데이터에 mapping을 위임하고 service 표면을 유지한다"는 차이가 있다.

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run build
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test:e2e
Test Files  2 passed (2)
Tests       11 passed (11)
```

Nest 검증은 unit 5개와 e2e 6개가 모두 통과했다. e2e와 unit 모두 `TypeOrmModule.forRoot({ database: ":memory:" ... })`를 써서 DB를 테스트 단위로 격리한다.

## native dependency와 검증 범위를 분리해서 본 장면

README와 공통 recovery 문서는 `better-sqlite3` 때문에 아래 순서를 권장한다.

```bash
$ pnpm install
$ pnpm approve-builds
$ pnpm rebuild better-sqlite3
```

이번 재실행에서는 이 복구 단계를 다시 밟지 않아도 Express/NestJS 양쪽 `build`, `test`, `test:e2e`가 모두 통과했다. 즉 현재 환경의 native binding은 이미 건강한 상태다. 하지만 이 lab 문서에는 "문제가 없었다"와 "문제가 생기면 어떻게 복구하는가"를 둘 다 남겨야 한다. 그래서 recovery 문서는 현재 blocker가 아니라 재현 가능한 복구 절차의 source로 보는 편이 맞다.

또 한 가지는 검증 범위다. Express e2e는 DB에 직접 `SELECT`해 persistence를 확인하고, Nest e2e는 HTTP를 통해 다시 읽어서 영속화 여부를 간접 확인한다. 둘 다 충분히 의미 있지만, 검증 방식이 정확히 같지는 않다. 이 차이를 적어야 raw SQL 레인과 ORM 레인의 테스트 감각까지 함께 읽힌다.

## 여기서 남는 것

이 문서를 다시 쓰고 나니 이 lab의 요점도 더 또렷해졌다. persistence migration은 SQL 문법 실습이 아니라, 저장 계층만 바꿔도 controller/service 바깥 계약을 유지할 수 있을 만큼 경계를 잘 세워 두었는지를 점검하는 작업이다. 다음 `07-domain-events`는 바로 그 저장 경계 위에서, 저장 성공 이후에만 event/side effect가 흘러가도록 만드는 단계로 이어진다.
