# 06-persistence-and-repositories — 개발 타임라인

> 소스 코드에 남지 않는 개발 과정을 시간순으로 기록한다.

---

## Phase 1: 프로젝트 초기화와 native 빌드

### 1-1. Express 프로젝트 설정

```bash
cd 06-persistence-and-repositories/express
pnpm init
```

**의존성 설치** — 기존 express, zod, supertest에 더해 `better-sqlite3` 추가:

```bash
pnpm add express better-sqlite3 zod
pnpm add -D typescript @types/express @types/better-sqlite3 vitest supertest @types/supertest tsx
```

### 1-2. NestJS 프로젝트 설정

```bash
cd 06-persistence-and-repositories/nestjs
# NestJS CLI로 프로젝트 생성 또는 수동 구성
pnpm add @nestjs/common @nestjs/core @nestjs/platform-express @nestjs/typeorm @nestjs/mapped-types typeorm better-sqlite3 reflect-metadata rxjs class-validator class-transformer
pnpm add -D typescript @nestjs/cli @nestjs/testing vitest supertest @types/supertest @types/better-sqlite3
```

### 1-3. better-sqlite3 native 빌드 (양쪽 공통)

better-sqlite3는 C++ 바인딩이 필요하다. `pnpm install`만으로는 부족하므로 반드시 다음 절차를 실행해야 한다:

```bash
pnpm install
pnpm approve-builds          # native 빌드 승인 (pnpm 9+)
pnpm rebuild better-sqlite3  # C++ 바인딩 컴파일
```

**실패 시**: "Could not locate the bindings file" 에러가 발생한다. 복구:

```bash
pnpm approve-builds
pnpm rebuild better-sqlite3
```

이미 승인된 상태라면 `pnpm approve-builds`에서 승인할 항목이 없다고 나온다. 그 경우 `pnpm rebuild better-sqlite3`만 재실행.

> 참고: 공통 복구 가이드는 `docs/native-sqlite-recovery.md`에 정리되어 있다.

### 1-4. tsconfig.json 설정

양쪽 모두 `tsconfig.base.json`을 확장하되, `better-sqlite3`를 위해 다음이 필요하다:

```json
{
  "extends": "../../../tsconfig.base.json",
  "compilerOptions": {
    "outDir": "dist",
    "rootDir": "src",
    "esModuleInterop": true,
    "experimentalDecorators": true,    // NestJS + TypeORM 필수
    "emitDecoratorMetadata": true      // NestJS + TypeORM 필수
  }
}
```

NestJS 쪽은 `experimentalDecorators`와 `emitDecoratorMetadata`가 반드시 `true`여야 한다. TypeORM의 `@Entity`, `@Column` 등이 이 설정에 의존한다.

---

## Phase 2: Express 레인 — 데이터베이스 계층 구현

### 2-1. 타입 정의

`src/types/book.ts` 생성:

- `Book` 인터페이스: 애플리케이션 도메인 모델 (camelCase)
- `BookRow` 인터페이스: 데이터베이스 행 매핑 (snake_case)

두 인터페이스를 분리한 이유: DB 컬럼 네이밍(`published_year`)과 TypeScript 네이밍(`publishedYear`)이 다르기 때문.

### 2-2. 데이터베이스 초기화 모듈

`src/database/init.ts` 생성:

- `createDatabase(filename)`: SQLite 인스턴스 생성, WAL 모드 활성화, foreign_keys ON
- `initDatabase(db)`: `CREATE TABLE IF NOT EXISTS books (...)` 실행

```bash
# 수동 검증 — sqlite3 CLI로 DB 내용 확인
sqlite3 bookstore.db ".tables"
sqlite3 bookstore.db ".schema books"
```

### 2-3. Repository 계층

`src/repositories/book.repository.ts` 생성:

- `findAll()`: `SELECT * FROM books ORDER BY created_at DESC`
- `findById(id)`: `SELECT * FROM books WHERE id = ?` (파라미터 바인딩으로 SQL injection 방지)
- `create(book)`: `INSERT INTO books (...) VALUES (?, ?, ?, ?, ?, ?, ?, ?)`
- `update(id, data)`: 기존 행을 먼저 조회 후 병합하여 `UPDATE`
- `delete(id)`: `DELETE FROM books WHERE id = ?`, 변경된 행 수로 성공/실패 판단
- `toBook(row)`: `BookRow` → `Book` 매핑 (snake_case → camelCase, 날짜 문자열 → Date 객체)

### 2-4. 서비스·컨트롤러 수정

기존 프로젝트의 `BookService`를 수정:

- 생성자가 `BookRepository` 인스턴스를 받도록 변경
- 내부 로직은 동일, 데이터 접근만 repository 메서드로 위임

`BookController`는 변경 없음 — Service 인터페이스가 그대로이므로.

### 2-5. 의존성 조립

`src/routes/book.router.ts`에서 수동 DI:

```
Database → BookRepository → BookService → BookController
```

`app.ts`에서 `createApp(db)` 패턴 — Database 인스턴스를 외부에서 주입.

`main.ts`에서 환경변수로 DB 경로 설정:

```typescript
const DB_PATH = process.env.DB_PATH || "bookstore.db";
const db = createDatabase(DB_PATH);
```

`SIGINT` 핸들러로 graceful shutdown 시 `db.close()` 호출.

---

## Phase 3: NestJS 레인 — TypeORM 도입

### 3-1. Entity 정의

`src/books/entities/book.entity.ts` 생성:

- `@Entity("books")` 데코레이터로 테이블 매핑
- `@PrimaryColumn("text")`: UUID를 직접 생성하므로 자동 증가 아닌 text PK
- `@CreateDateColumn`, `@UpdateDateColumn`: TypeORM이 자동 관리하는 시간 컬럼

### 3-2. AppModule에서 TypeORM 연결

`src/app.module.ts`:

```typescript
TypeOrmModule.forRoot({
  type: "better-sqlite3",
  database: process.env.DB_PATH || ":memory:",
  entities: [Book],
  synchronize: true,   // ⚠️ 개발 전용, 프로덕션 금지
})
```

`synchronize: true`는 Entity 변경 시 자동으로 스키마를 동기화한다. 프로덕션에서 활성화하면 데이터 손실 위험이 있으므로 마이그레이션을 사용해야 한다.

### 3-3. BooksModule 구현

`src/books/books.module.ts`:

- `TypeOrmModule.forFeature([Book])`: Book Repository를 DI 컨테이너에 등록
- `BooksController`, `BooksService`를 모듈에 등록

### 3-4. DTO 정의

- `create-book.dto.ts`: class-validator 데코레이터로 검증 규칙 정의
- `update-book.dto.ts`: `PartialType(CreateBookDto)`로 모든 필드를 optional로 변환

`@nestjs/mapped-types` 패키지가 `PartialType`을 제공한다. Express 쪽에서 Zod의 `.optional()`로 구현한 것과 같은 역할.

### 3-5. Service — TypeORM Repository 사용

`src/books/books.service.ts`:

- `@InjectRepository(Book)`으로 TypeORM Repository 주입
- 모든 메서드가 `async` — TypeORM Repository가 Promise 반환
- `create` + `save` 패턴: `create`는 엔티티 인스턴스 생성, `save`가 실제 DB INSERT
- `update`는 `findOne` → `Object.assign` → `save` 패턴
- `remove`는 `findOne` → `remove` 패턴

### 3-6. Controller

`src/books/books.controller.ts`:

- 각 핸들러에서 `ValidationPipe`를 인라인으로 적용 (`whitelist: true`, `forbidNonWhitelisted: true`)
- `@HttpCode(HttpStatus.CREATED)`, `@HttpCode(HttpStatus.NO_CONTENT)` 등 명시적 상태 코드

---

## Phase 4: 테스트 전략

### 4-1. Express 단위 테스트

`test/unit/book.repository.test.ts`:

```bash
pnpm run test
```

- 매 테스트마다 `:memory:` DB 생성 → `initDatabase` → 테스트 → `db.close()`
- `BookRepository`를 직접 호출하여 CRUD 동작 검증
- `makeBook()` 헬퍼로 테스트 데이터 팩토리 패턴 사용

### 4-2. Express E2E 테스트

`test/e2e/database.e2e.test.ts`:

```bash
pnpm run test:e2e
```

- `createApp(db)`로 인메모리 DB가 연결된 Express 앱 생성
- `supertest`로 HTTP 요청 후 응답과 DB 직접 조회를 모두 검증
- API 응답 확인 + `db.prepare("SELECT ...").get(id)` 직접 DB 검증 = 양면 검증

### 4-3. NestJS 단위 테스트

`test/unit/books.service.test.ts`:

```bash
pnpm run test
```

- `Test.createTestingModule`으로 인메모리 DB + BooksModule 구성
- `module.get(BooksService)`로 서비스 인스턴스 획득
- `module.close()`로 TypeORM 커넥션 정리 (리소스 누수 방지)

### 4-4. NestJS E2E 테스트

`test/e2e/database.e2e.test.ts`:

```bash
pnpm run test:e2e
```

- `moduleFixture.createNestApplication()` 후 전역 Pipe/Filter/Interceptor 등록
- `app.getHttpServer()`로 supertest에 전달
- 실제 앱과 동일한 미들웨어 스택에서 테스트

### 4-5. Vitest 설정

양쪽 모두 `vitest.config.ts`(단위)와 `vitest.e2e.config.ts`(E2E) 분리:

```bash
# 단위 테스트만
pnpm run test

# E2E 테스트만
pnpm run test:e2e
```

---

## Phase 5: 빌드 및 검증

### 5-1. Express 빌드·실행

```bash
cd express/
pnpm run build    # tsc → dist/ 출력
pnpm run start    # node dist/main.js
```

수동 검증:

```bash
# 서버 실행 후 curl로 API 테스트
curl -X POST http://localhost:3000/books \
  -H "Content-Type: application/json" \
  -d '{"title":"Clean Code","author":"Robert C. Martin","publishedYear":2008,"genre":"Programming","price":33.99}'

curl http://localhost:3000/books

# 서버 종료 후 DB 파일 확인
ls -la bookstore.db
sqlite3 bookstore.db "SELECT * FROM books;"
```

### 5-2. NestJS 빌드·실행

```bash
cd nestjs/
pnpm run build    # nest build → dist/ 출력
pnpm run start    # node dist/main.js
```

### 5-3. 전체 검증 순서 (양쪽 공통)

```bash
pnpm install
pnpm approve-builds
pnpm rebuild better-sqlite3
pnpm run build
pnpm run test
pnpm run test:e2e
```

---

## Phase 6: Graceful Shutdown

Express `main.ts`에서 `process.on("SIGINT")`로 DB를 닫는다:

```bash
# Ctrl+C로 서버 종료 시 DB 커넥션이 정리되는지 확인
node dist/main.js
# Ctrl+C
```

---

## 도구 및 커맨드 요약

| 도구/커맨드 | 용도 |
|-------------|------|
| `pnpm install` | 의존성 설치 |
| `pnpm approve-builds` | better-sqlite3 native 빌드 승인 |
| `pnpm rebuild better-sqlite3` | C++ 바인딩 재컴파일 |
| `pnpm run build` | TypeScript 컴파일 |
| `pnpm run test` | 단위 테스트 실행 (Vitest) |
| `pnpm run test:e2e` | E2E 테스트 실행 (Vitest) |
| `sqlite3` | SQLite CLI로 직접 DB 내용 확인 |
| `curl` | 수동 API 테스트 |
| `supertest` | 테스트 내 HTTP 요청 자동화 |

## 핵심 파일 생성 순서 (Express)

```
types/book.ts → database/init.ts → repositories/book.repository.ts
→ services/book.service.ts (수정) → routes/book.router.ts (수정)
→ app.ts (DB 주입) → main.ts (DB 경로·종료 핸들러)
→ test/unit/ → test/e2e/
```

## 핵심 파일 생성 순서 (NestJS)

```
entities/book.entity.ts → dto/ (create, update)
→ books.service.ts → books.controller.ts → books.module.ts
→ app.module.ts (TypeORM 설정)
→ test/unit/ → test/e2e/
```
