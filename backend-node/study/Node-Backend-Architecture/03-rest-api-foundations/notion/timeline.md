# 03-rest-api-foundations — 개발 타임라인

이 문서는 Express와 NestJS 두 레인의 전체 개발 과정을 순서대로 기록한다.
프레임워크 설치, 프로젝트 구조 잡기, DI 조립 등 소스 코드만으로는 알 수 없는 과정을 담는다.

---

## 1단계: 공통 기반 작업

### 디렉토리 생성

```bash
mkdir -p 03-rest-api-foundations/express/src/{controllers,services,routes,types,utils}
mkdir -p 03-rest-api-foundations/express/test/{unit,e2e}
mkdir -p 03-rest-api-foundations/nestjs/src/books/{dto,entities}
mkdir -p 03-rest-api-foundations/nestjs/test/{unit,e2e}
mkdir -p 03-rest-api-foundations/problem/code
mkdir -p 03-rest-api-foundations/problem/script
mkdir -p 03-rest-api-foundations/docs/concepts/{express,nestjs}
```

### 문제 정의 (problem/)

`problem/README.md` — Books CRUD API를 Express와 NestJS로 각각 구현하라는 과제를 명시했다. 저장소는 in-memory, ID는 UUID, 응답은 JSON.

---

## 2단계: Express 레인 셋업

### 패키지 초기화 및 의존성 설치

```bash
cd express
pnpm init
pnpm add express
pnpm add -D typescript @types/express @types/node @types/supertest supertest ts-node vitest
```

- `express` (^4.21.0): 웹 프레임워크 — 유일한 런타임 의존성
- `ts-node` (^10.9.0): 빌드 없이 TypeScript를 직접 실행 (`pnpm dev` 용)
- 나머지는 이전 과제와 동일한 개발 의존성

### TypeScript, Vitest 설정

- `tsconfig.json`: 루트 `tsconfig.base.json` extends
- `vitest.config.ts`: `environment: "node"`, `globals: true`

### npm 스크립트

```json
{
  "build": "tsc",
  "start": "node dist/main.js",
  "dev": "ts-node src/main.ts",
  "test": "vitest run"
}
```

`dev` 스크립트가 추가되었다. 개발 중에 빌드 없이 바로 실행할 수 있다.

---

## 3단계: Express 구현

### 구현 순서

1. **타입 정의** (`src/types/book.ts`, `src/types/index.ts`): `Book`, `CreateBookDto`, `UpdateBookDto` 타입을 먼저 확정했다.

2. **서비스 구현** (`src/services/book.service.ts`): `Map<string, Book>` 기반 in-memory 저장소. `randomUUID()`로 ID 생성. `findAll`, `findById`, `create`, `update`, `delete` 메서드. Express에 대한 의존이 전혀 없는 순수 비즈니스 로직.

3. **컨트롤러 구현** (`src/controllers/book.controller.ts`): 생성자에서 `BookService`를 주입받는다. 각 메서드는 `req`에서 데이터를 추출하고, 서비스를 호출하고, `res`로 응답한다. 생성자에서 `bind(this)` 필요.

4. **유틸리티** (`src/utils/async-handler.ts`): Express 4에서 async 핸들러의 에러를 자동으로 잡아주는 래퍼 함수.

5. **라우터** (`src/routes/book.router.ts`): `Router()` 인스턴스에 `GET /`, `GET /:id`, `POST /`, `PUT /:id`, `DELETE /:id`를 `asyncHandler`로 감싸서 등록.

6. **앱 조립** (`src/app.ts`): composition root. `BookService` → `BookController` → `createBookRouter` → `app.use("/books", bookRouter)`. `express.json()` 미들웨어와 글로벌 에러 핸들러 등록.

7. **진입점** (`src/main.ts`): `createApp()`으로 앱 생성 후 `PORT` 환경 변수 또는 3000번 포트에서 listen.

---

## 4단계: NestJS 레인 셋업

### 패키지 초기화 및 의존성 설치

```bash
cd nestjs
pnpm init
pnpm add @nestjs/common @nestjs/core @nestjs/platform-express reflect-metadata rxjs
pnpm add -D @nestjs/cli @nestjs/testing @types/node @types/supertest supertest typescript vitest
```

NestJS는 런타임 의존성이 Express보다 많다:
- `@nestjs/common`, `@nestjs/core`: 프레임워크 코어
- `@nestjs/platform-express`: Express 어댑터
- `reflect-metadata`: 데코레이터 메타데이터 지원
- `rxjs`: NestJS 내부에서 사용하는 반응형 라이브러리
- `@nestjs/cli`: `nest build`, `nest start` 명령
- `@nestjs/testing`: 테스트 모듈 빌더

### NestJS CLI 설정

`nest-cli.json` — NestJS CLI가 프로젝트를 인식하기 위한 설정 파일:
```json
{
  "collection": "@nestjs/schematics",
  "sourceRoot": "src"
}
```

### npm 스크립트

```json
{
  "build": "nest build",
  "start": "nest start",
  "start:dev": "nest start --watch",
  "test": "vitest run",
  "test:e2e": "vitest run --config vitest.e2e.config.ts"
}
```

`nest build`는 `tsc`를 내부적으로 호출하지만, NestJS 프로젝트의 관례를 따른다. E2E 테스트는 별도 설정 파일을 사용한다.

### E2E 테스트 설정

`vitest.e2e.config.ts`를 별도로 만들었다. E2E 테스트 파일은 `test/e2e/` 디렉토리에 위치한다.

---

## 5단계: NestJS 구현

### 구현 순서

1. **엔티티** (`src/books/entities/book.entity.ts`): `Book` 클래스 정의 (id, title, author, publishedYear).

2. **DTO** (`src/books/dto/create-book.dto.ts`, `update-book.dto.ts`): `CreateBookDto`, `UpdateBookDto` 클래스 정의.

3. **서비스** (`src/books/books.service.ts`): `@Injectable()` 데코레이터. `Map<string, Book>` 기반 in-memory 저장소. `findAll`, `findOne`, `create`, `update`, `remove` 메서드. 리소스가 없으면 `NotFoundException` throw.

4. **컨트롤러** (`src/books/books.controller.ts`): `@Controller("books")` 데코레이터. `@Get()`, `@Post()`, `@Put(":id")`, `@Delete(":id")` 라우트. `@Param("id")`, `@Body()`로 파라미터 추출. 반환값을 그대로 return — NestJS가 직렬화와 상태 코드를 처리.

5. **모듈** (`src/books/books.module.ts`): `BooksController`와 `BooksService`를 묶는 feature module.

6. **앱 모듈** (`src/app.module.ts`): `BooksModule`을 import하는 root module.

7. **진입점** (`src/main.ts`): `NestFactory.create(AppModule)`로 앱 생성 후 listen.

---

## 6단계: 테스트 작성

### Express 테스트

**단위 테스트** (`test/unit/`): `BookService`의 CRUD 메서드를 직접 호출해서 검증.
**E2E 테스트** (`test/e2e/`): `supertest`로 `createApp()`에 HTTP 요청을 보내서 전체 스택 검증.

### NestJS 테스트

**단위 테스트** (`test/unit/`): `Test.createTestingModule`으로 `BooksService`만 주입한 컨트롤러를 만들어서 검증.
**E2E 테스트** (`test/e2e/`): `Test.createTestingModule`으로 전체 앱을 구성하고 `supertest`로 HTTP 요청을 보내서 검증.

---

## 7단계: 빌드와 검증

### Express 빌드와 테스트

```bash
cd express
pnpm install
pnpm run build
pnpm run test
```

### NestJS 빌드와 테스트

```bash
cd nestjs
pnpm install
pnpm run build
pnpm run test
pnpm run test:e2e
```

### 수동 검증

```bash
# Express
cd express && pnpm start
# 다른 터미널에서
curl http://localhost:3000/books
curl -X POST http://localhost:3000/books -H "Content-Type: application/json" \
  -d '{"title":"Test","author":"Alice","publishedYear":2026}'

# NestJS
cd nestjs && pnpm start
# 동일한 curl 명령으로 검증
```

---

## 8단계: 문서 작성 (docs/)

### Express 개념 문서 (docs/concepts/express/)

- `express-fundamentals.md` — Express 기본 개념 정리
- `layered-architecture.md` — 계층 분리 패턴
- `dependency-injection.md` — 수동 DI의 조립 방식
- `testing-patterns.md` — 단위 테스트와 E2E 테스트 전략

### NestJS 개념 문서 (docs/concepts/nestjs/)

- `nestjs-fundamentals.md` — NestJS 기본 개념 정리
- `decorators-and-metadata.md` — 데코레이터 동작 원리
- `express-vs-nestjs.md` — 두 프레임워크 비교
- `testing-patterns.md` — NestJS 테스트 모듈 사용법

---

## 프로젝트 파일 구조 최종 상태

```
03-rest-api-foundations/
├── README.md
├── docs/
│   ├── README.md
│   └── concepts/
│       ├── express/
│       │   ├── dependency-injection.md
│       │   ├── express-fundamentals.md
│       │   ├── layered-architecture.md
│       │   └── testing-patterns.md
│       └── nestjs/
│           ├── decorators-and-metadata.md
│           ├── express-vs-nestjs.md
│           ├── nestjs-fundamentals.md
│           └── testing-patterns.md
├── express/
│   ├── package.json
│   ├── tsconfig.json
│   ├── vitest.config.ts
│   ├── src/
│   │   ├── app.ts
│   │   ├── main.ts
│   │   ├── controllers/book.controller.ts
│   │   ├── services/book.service.ts
│   │   ├── routes/book.router.ts
│   │   ├── types/{book.ts, index.ts}
│   │   └── utils/async-handler.ts
│   └── test/{unit/, e2e/}
├── nestjs/
│   ├── package.json
│   ├── nest-cli.json
│   ├── tsconfig.json
│   ├── vitest.config.ts
│   ├── vitest.e2e.config.ts
│   ├── src/
│   │   ├── app.module.ts
│   │   ├── main.ts
│   │   └── books/
│   │       ├── books.module.ts
│   │       ├── books.controller.ts
│   │       ├── books.service.ts
│   │       ├── dto/{create-book.dto.ts, update-book.dto.ts}
│   │       └── entities/book.entity.ts
│   └── test/{unit/, e2e/}
└── problem/
    ├── README.md
    ├── code/
    └── script/
```

---

## 사용한 도구 요약

| 도구 | 용도 |
|------|------|
| pnpm | 패키지 매니저 |
| TypeScript 5.6+ | 컴파일러 |
| Express 4.21+ | 웹 프레임워크 (원리 학습 레인) |
| NestJS 10.4+ | 웹 프레임워크 (실무 적용 레인) |
| @nestjs/cli | NestJS 빌드 및 실행 도구 (`nest build`, `nest start`) |
| reflect-metadata | NestJS 데코레이터 메타데이터 지원 |
| supertest 7+ | HTTP 통합 테스트 |
| Vitest 2.1+ | 테스트 러너 |
| ts-node | Express 개발 모드 실행 |
| curl | 수동 API 검증 |
