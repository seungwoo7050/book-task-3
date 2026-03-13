# 06-persistence-and-repositories development timeline

auth까지는 여전히 메모리 안에서 문제를 풀 수 있었지만, 이 프로젝트부터는 상태를 프로세스 바깥으로 밀어내야 한다. 그렇다고 상위 API를 다 뜯어고치는 건 아니다. 오히려 핵심은 API 표면을 최대한 유지한 채 저장 전략만 교체하는 데 있다. 이게 repository 프로젝트를 읽는 올바른 기준이었다.

## 구현 순서 요약

- Express에서 SQLite schema와 raw SQL repository를 만든다.
- NestJS에서 entity와 injected repository로 같은 계약을 ORM 위에 옮긴다.
- API 응답과 실제 DB 상태를 함께 검증한다.

## Phase 1

- 당시 목표: Express 레인에서 저장 책임을 `BookRepository`로 밀어낸다.
- 변경 단위: `express/src/database/init.ts`, `express/src/repositories/book.repository.ts`
- 처음 가설: persistence 교체가 service/controller까지 흔들지 않게 하려면 DB 연결과 SQL을 repository 하나로 모아야 한다.
- 실제 진행: `initDatabase()`가 `books` 테이블을 만들고 WAL 모드를 켠다. `BookRepository`는 raw SQL로 CRUD를 수행하고 `BookRow -> Book` 변환을 담당한다.

CLI:

```bash
$ cd express
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test:e2e
Tests 7 passed (7)
Tests 6 passed (6)
```

검증 신호:

- repository unit test가 SQL 결과를 바로 검증한다.
- e2e는 생성한 책이 실제 DB row로 남는지까지 확인한다.

핵심 코드:

```ts
db.exec(`
  CREATE TABLE IF NOT EXISTS books (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    published_year INTEGER NOT NULL,
    genre TEXT NOT NULL,
    price REAL NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
  )
`);
```

왜 이 코드가 중요했는가:

저장 계층 교체는 결국 schema 선언에서 현실이 된다. 메모리 `Map` 대신 실제 column 이름과 타입이 생기는 순간, 이후 테스트 전략도 달라지기 시작한다.

새로 배운 것:

- persistence 프로젝트의 첫 질문은 ORM 여부가 아니라 "어떤 필드가 실제 저장소의 truth가 되는가"다.

## Phase 2

- 당시 목표: NestJS에서 같은 문제를 TypeORM과 injected repository로 푼다.
- 변경 단위: `nestjs/src/books/books.service.ts`
- 처음 가설: Express에서 SQL을 직접 썼다면 NestJS에서는 entity와 repository injection이 저장 전략의 중심이 될 것이다.
- 실제 진행: `@InjectRepository(Book)`로 `Repository<Book>`를 받고, `find`, `findOneBy`, `save`, `remove`로 CRUD를 수행하게 했다.

CLI:

```bash
$ cd ../nestjs
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test:e2e
Tests 5 passed (5)
Tests 6 passed (6)
```

검증 신호:

- unit test는 service가 repository를 통해 책을 읽고 쓰는지 확인한다.
- e2e는 in-memory SQLite에서 생성 후 재조회, 삭제 후 404를 검증한다.

핵심 코드:

```ts
constructor(
  @InjectRepository(Book)
  private readonly bookRepository: Repository<Book>,
) {}
```

왜 이 코드가 중요했는가:

Express에서는 repository가 직접 new 되었고, NestJS에서는 framework가 repository를 주입한다. storage 교체를 같은 주제로 보더라도 연결 방식은 또 한 번 달라진다.

새로 배운 것:

- ORM의 장점은 SQL을 덜 쓰는 데 있기도 하지만, 더 큰 차이는 저장 계층 의존성을 service constructor에서 명시할 수 있다는 데 있다.

## Phase 3

- 당시 목표: 저장 계층이 바뀌어도 API contract와 실패 경계가 유지되는지 증명한다.
- 변경 단위: `express/test/e2e/database.e2e.test.ts`, `nestjs/test/e2e/database.e2e.test.ts`
- 처음 가설: persistence 프로젝트는 API 응답만 보면 충분하지 않다. 적어도 한 번은 DB 상태를 직접 확인해야 한다.
- 실제 진행: Express e2e는 DB에서 row를 직접 `SELECT`해 확인하고, Nest e2e는 생성/재조회/삭제/404/validation을 in-memory DB 위에서 모두 재현했다.

CLI:

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test:e2e
{"timestamp":"...","method":"POST","url":"/books","statusCode":201,"durationMs":0}
{"timestamp":"...","method":"DELETE","url":"/books/...","statusCode":204,"durationMs":0}
{"timestamp":"...","method":"GET","url":"/books/nonexistent","statusCode":404,"durationMs":0}
```

검증 신호:

- API surface는 여전히 `/books` CRUD다.
- 하지만 내부 상태는 이제 프로세스 종료 후에도 남을 수 있는 구조로 바뀌었다.

핵심 코드:

```ts
const row = db.prepare("SELECT * FROM books WHERE id = ?").get(id);
expect(row).toBeDefined();
```

왜 이 코드가 중요했는가:

이 한 줄이 "API가 성공했다"를 넘어서 "정말 저장됐다"는 사실을 보여 준다. persistence 교체의 완료 신호는 여기서 나온다.

새로 배운 것:

- 저장 계층 설계는 응답 payload보다도 검증 방법을 먼저 바꾼다. 이후 이벤트 설계가 DB 이후에 붙는 것도 이 때문이다.

다음:

- [`../07-domain-events/00-series-map.md`](../07-domain-events/00-series-map.md)에서 저장이 끝난 뒤 side effect를 이벤트 경계로 분리한다.
