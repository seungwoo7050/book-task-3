# 메모리에서 디스크로 — 영속 계층이라는 결단

## 프롤로그: "서버를 끄면 데이터가 사라진다"

다섯 번째 프로젝트까지 만들어 온 Book API는 잘 동작했다. CRUD는 완벽했고, 인증도 붙였고, 파이프라인도 정리됐다. 하지만 한 가지 결정적인 문제가 있었다. 서버 프로세스를 종료하는 순간, 모든 데이터가 증발한다는 것이다.

인메모리 배열은 프로토타이핑에는 충분하지만 실제 서비스에는 쓸 수 없다. 이 프로젝트의 출발점은 단순하다. **배열을 데이터베이스로 교체하되, 기존 API 계약은 한 글자도 바꾸지 않는다.** 그리고 이 단순한 요구사항이 아키텍처 전체에 걸쳐 생각보다 많은 것을 가르쳐 준다.

---

## 1. 왜 SQLite인가

데이터베이스를 선택할 때 Postgres나 MySQL을 먼저 떠올릴 수 있다. 하지만 이 단계에서 SQLite를 선택한 데는 분명한 이유가 있다.

SQLite는 별도의 서버 프로세스가 필요 없다. 파일 하나가 곧 데이터베이스다. Docker도, 포트 설정도, 커넥션 풀도 아직 없는 이 단계에서 SQLite는 "영속이라는 개념 자체"에 집중할 수 있게 해준다. `:memory:` 모드를 쓰면 테스트할 때 파일조차 필요 없다. 테스트가 끝나면 메모리와 함께 데이터가 소멸한다. 완벽한 격리.

Node.js 생태계에서는 `better-sqlite3`라는 라이브러리가 이 역할을 맡는다. 이름에 "better"가 붙은 이유는 기존 `sqlite3` 대비 동기 API를 제공하기 때문이다. SQL 실행이 동기적이라는 것은 코드가 단순해진다는 뜻이기도 하다.

하지만 이 라이브러리에는 한 가지 관문이 있다. C++ 바인딩을 컴파일해야 한다는 것이다. `pnpm install`만으로는 부족하다. `pnpm approve-builds`로 native build를 명시적으로 승인하고, `pnpm rebuild better-sqlite3`로 바인딩을 다시 컴파일해야 한다. 이 과정을 빼먹으면 "Could not locate the bindings file"이라는 에러를 만나게 된다. 소스 코드에는 이 과정이 보이지 않는다. 실행 환경을 준비하는 것은 코드 밖의 일이다.

---

## 2. Express 레인: raw SQL이라는 정직한 선택

Express 쪽에서는 SQL을 직접 작성하는 길을 택했다. 이 선택은 "SQL을 모르면 ORM도 제대로 쓸 수 없다"는 원칙에서 비롯한다.

### 데이터베이스 초기화

`database/init.ts`에는 두 가지 함수가 있다. `createDatabase`는 SQLite 인스턴스를 만들고 WAL 모드와 외래 키를 활성화한다. `initDatabase`는 `CREATE TABLE IF NOT EXISTS`로 books 테이블을 보장한다.

```typescript
const db = new Database(filename);
db.pragma("journal_mode = WAL");
db.pragma("foreign_keys = ON");
```

WAL(Write-Ahead Logging)은 읽기와 쓰기를 동시에 허용하는 저널 모드다. 프로덕션 SQLite를 쓸 때 거의 항상 켜야 하는 설정인데, 이런 세부사항은 ORM 뒤에 숨겨지면 놓치기 쉽다.

### Repository 패턴

`BookRepository` 클래스는 `Database` 인스턴스를 생성자로 받아서 CRUD 메서드를 제공한다. 각 메서드 안에는 SQL 문자열이 직접 보인다.

```typescript
findAll(): Book[] {
  const rows = this.db.prepare("SELECT * FROM books ORDER BY created_at DESC").all() as BookRow[];
  return rows.map(this.toBook);
}
```

여기서 중요한 점은 `BookRow`와 `Book`이 분리되어 있다는 것이다. 데이터베이스 컬럼은 `snake_case`(`published_year`, `created_at`)이지만 애플리케이션 도메인은 `camelCase`(`publishedYear`, `createdAt`)다. `toBook` 메서드가 이 둘을 매핑한다. 문자열로 저장된 날짜를 `new Date()`로 변환하는 것도 이 경계에서 처리된다.

이 매핑 로직이 바로 "임피던스 불일치(impedance mismatch)"의 현장이다. 관계형 데이터베이스의 행(row)과 객체지향 프로그래밍의 인스턴스는 구조가 다르다. ORM이 해결하려는 문제가 바로 이것인데, raw SQL로 직접 구현해 보면 그 차이가 손에 잡힌다.

### 의존성 조립

`createBookRouter` 함수는 라우터를 생성하면서 의존성을 수동으로 조립한다. `Database → BookRepository → BookService → BookController` 순서로 생성자를 통해 전달한다. NestJS의 DI 컨테이너가 자동으로 해주는 일을 Express에서는 직접 한다.

```typescript
const repository = new BookRepository(db);
const service = new BookService(repository);
const controller = new BookController(service);
```

이 코드는 의존성 주입(DI)의 가장 원시적인 형태다. 프레임워크 없이도 DI는 가능하다. 다만 규모가 커지면 이 수동 조립이 점점 고통이 된다는 것을 체감할 수 있다.

---

## 3. NestJS 레인: TypeORM이라는 추상 위의 추상

NestJS 쪽에서는 TypeORM을 도입한다. 같은 SQLite, 같은 books 테이블, 같은 CRUD. 하지만 코드의 표면은 완전히 다르다.

### Entity — 데코레이터로 그리는 테이블

```typescript
@Entity("books")
export class Book {
  @PrimaryColumn("text")
  id!: string;

  @Column({ type: "text" })
  title!: string;

  @CreateDateColumn({ type: "datetime" })
  createdAt!: Date;

  @UpdateDateColumn({ type: "datetime" })
  updatedAt!: Date;
}
```

SQL의 `CREATE TABLE`이 클래스 위의 데코레이터로 바뀌었다. `@CreateDateColumn`과 `@UpdateDateColumn`은 TypeORM이 자동으로 시간을 채워준다. Express 쪽에서 `new Date().toISOString()`을 직접 넣던 일이 자동화된 것이다.

`synchronize: true` 옵션은 TypeORM이 Entity 정의를 보고 자동으로 테이블을 생성/수정해 준다. 개발 환경에서는 편리하지만 프로덕션에서는 사용하면 안 된다. 데이터 유실 위험이 있기 때문이다. 이 주의사항은 코드에 주석으로 남아있지 않지만, 모든 TypeORM 입문자가 반드시 알아야 하는 것이다.

### Repository — 직접 만들지 않는 Repository

NestJS 쪽에서는 `BookRepository` 같은 클래스를 직접 만들지 않는다. 대신 TypeORM이 제공하는 `Repository<Book>`을 `@InjectRepository(Book)` 데코레이터로 주입받는다.

```typescript
constructor(
  @InjectRepository(Book)
  private readonly bookRepository: Repository<Book>,
) {}
```

`findAll`은 `this.bookRepository.find({ order: { createdAt: "DESC" } })`로 충분하다. SQL을 한 줄도 쓰지 않는다. `create`와 `save`도 마찬가지다. Express 쪽에서 7줄이 필요했던 INSERT가 두 줄로 줄어든다.

```typescript
const book = this.bookRepository.create({ id: crypto.randomUUID(), ...dto });
return this.bookRepository.save(book);
```

하지만 이 간결함 뒤에는 트레이드오프가 있다. ORM이 생성하는 SQL이 비효율적일 수 있고, 복잡한 쿼리에서는 결국 QueryBuilder나 raw SQL로 돌아가야 하며, 디버깅할 때 실제 실행되는 SQL을 보려면 별도 설정이 필요하다.

### 동기 vs 비동기

Express 레인의 `BookRepository`는 모든 메서드가 동기다. `better-sqlite3`가 동기 API를 제공하기 때문이다. NestJS 레인의 `BooksService`는 모든 메서드가 `async/await`다. TypeORM의 Repository 메서드가 Promise를 반환하기 때문이다.

같은 SQLite를 사용하면서도 접근 방식이 다른 이유는 이렇다. TypeORM은 다양한 데이터베이스를 지원하는 범용 ORM이므로, Postgres처럼 비동기가 필수인 데이터베이스를 고려해서 API 전체가 Promise 기반이다. SQLite는 실제로는 동기적으로 동작하지만, TypeORM이라는 추상 레이어가 비동기 인터페이스를 강제한다.

---

## 4. 테스트 격리라는 숙제

영속 계층을 다루기 시작하면 테스트가 갑자기 어려워진다. 인메모리 배열이었을 때는 매 테스트마다 새 배열을 만들면 됐다. 데이터베이스는 그렇지 않다.

### Express: `:memory:` + `beforeEach`

Express 쪽의 테스트는 매 테스트 전에 인메모리 SQLite 인스턴스를 새로 만든다.

```typescript
beforeEach(() => {
  db = new Database(":memory:");
  initDatabase(db);
  repo = new BookRepository(db);
});

afterEach(() => {
  db.close();
});
```

`:memory:` 모드이므로 파일이 남지 않는다. 각 테스트는 빈 데이터베이스에서 시작한다. 완벽한 격리.

단위 테스트는 `BookRepository`를 직접 호출하고, E2E 테스트는 `createApp(db)`으로 HTTP 요청을 보내면서 `db.prepare`로 직접 데이터베이스 상태를 검증한다. API 응답뿐 아니라 실제 저장된 데이터를 확인하는 것이다. 이것이 영속 계층 E2E 테스트의 핵심이다.

### NestJS: `Test.createTestingModule`

NestJS 쪽도 같은 전략이지만, NestJS의 테스트 유틸리티를 거친다.

```typescript
beforeEach(async () => {
  module = await Test.createTestingModule({
    imports: [
      TypeOrmModule.forRoot({
        type: "better-sqlite3",
        database: ":memory:",
        entities: [Book],
        synchronize: true,
      }),
      BooksModule,
    ],
  }).compile();
  service = module.get(BooksService);
});
```

`module.close()`가 `afterEach`에서 호출되어 TypeORM 커넥션을 정리한다. 이 한 줄을 빼먹으면 테스트 후 리소스 누수가 발생할 수 있다.

E2E 테스트에서는 `moduleFixture.createNestApplication()`으로 실제 HTTP 서버를 띄운 뒤 `supertest`로 요청을 보낸다. `ValidationPipe`, `HttpExceptionFilter`, `TransformInterceptor`를 전역으로 등록해야 실제 애플리케이션과 동일한 동작을 검증할 수 있다.

---

## 5. 두 경로의 대조표

| 관심사 | Express (raw SQL) | NestJS (TypeORM) |
|--------|-------------------|------------------|
| 테이블 생성 | `CREATE TABLE IF NOT EXISTS` 직접 실행 | `@Entity` + `synchronize: true` |
| 읽기 | `db.prepare("SELECT ...").all()` | `repository.find()` |
| 쓰기 | `db.prepare("INSERT ...").run(...)` | `repository.create()` + `repository.save()` |
| 매핑 | `toBook()` 수동 변환 | 자동 (데코레이터 기반) |
| DI | 수동 생성자 조립 | `@InjectRepository()` |
| 동기/비동기 | 동기 | 비동기 (Promise) |
| 검증 | Zod 스키마 | class-validator 데코레이터 |
| 장점 | SQL 완전 제어, 투명성 | 코드 간결, 자동 매핑 |
| 약점 | 매핑 코드 수동, 규모 확장 시 반복 | SQL 비가시성, 학습 곡선 |

---

## 6. 아키텍처 관점에서 본 교훈

### Repository 패턴의 가치

두 레인 모두 Service가 Repository에 의존하고, Repository가 데이터 접근을 캡슐화한다. 이 구조 덕분에 `BookService`는 데이터가 메모리 배열에서 오든 SQLite에서 오든 상관없이 동일하게 동작한다. 이것이 Repository 패턴의 핵심 가치다.

Express 쪽에서 `BookService`의 코드를 보면, 이전 프로젝트에서 배열을 직접 조작하던 것과 거의 같은 인터페이스를 유지하고 있다. `findAll()`, `findById()`, `create()`, `update()`, `delete()`. 내부 구현만 바뀌었을 뿐 외부 계약은 동일하다.

### API 계약의 보존

이 프로젝트에서 가장 중요한 제약은 "기존 API의 요청/응답 형태를 바꾸지 않는다"는 것이었다. 영속 메커니즘을 교체하면서도 HTTP 인터페이스가 유지된다는 사실은, 관심사 분리가 제대로 작동하고 있다는 증거다.

### `BookRow` vs `Book` — 경계의 이름

Express 쪽에서 `BookRow`와 `Book`을 분리한 것은 형식적일 수 있지만 중요한 관습이다. 데이터베이스 스키마와 도메인 모델은 진화 속도가 다르다. 컬럼을 추가해도 도메인 인터페이스는 바뀌지 않을 수 있고, 반대도 마찬가지다. 이 분리가 나중에 마이그레이션이나 스키마 변경 시 버퍼가 된다.

---

## 에필로그: 다음 단계를 향해

데이터가 디스크에 살아남게 되었다. 하지만 아직 남은 질문이 있다. 데이터가 바뀔 때 다른 시스템에 알려야 한다면? 프로젝트 07에서는 이 영속된 데이터 위에 도메인 이벤트를 발행하는 패턴을 다룬다. "저장했다"에서 "저장했고, 세상에 알렸다"로의 전환이다.

더 먼 미래에는 SQLite 대신 Postgres가 오고(프로젝트 10), Docker Compose로 데이터베이스 서버가 별도 컨테이너에서 돌아가며, 마이그레이션 스크립트로 스키마를 관리하게 된다. 그때 이 프로젝트에서 raw SQL을 직접 써 본 경험이 ORM이 무엇을 숨기고 있는지 알려줄 것이다.
