# 04-request-pipeline — 개발 타임라인

이 문서는 Express와 NestJS 두 레인에서 요청 파이프라인을 구축한 전체 개발 과정을 순서대로 기록한다.

---

## 1단계: Express 레인 셋업

### 의존성 설치

```bash
cd express
pnpm init
pnpm add express zod
pnpm add -D typescript @types/express @types/node @types/supertest supertest tsx vitest
```

이 과제에서 새로 추가된 주요 의존성:
- `zod` (^3.23.0): 스키마 기반 런타임 검증 라이브러리
- `tsx` (^4.19.0): `ts-node` 대신 사용하는 더 빠른 TypeScript 실행기 (개발 모드)

### npm 스크립트

```json
{
  "build": "tsc",
  "start": "node dist/main.js",
  "dev": "tsx watch src/main.ts",
  "test": "vitest run",
  "test:watch": "vitest",
  "test:e2e": "vitest run --config vitest.e2e.config.ts"
}
```

`dev` 스크립트가 `tsx watch`로 바뀌었다. 파일 변경 시 자동 재시작된다.

---

## 2단계: Express 에러 클래스 구현

### 구현 순서

1. **`AppError`** (`src/errors/app-error.ts`): `Error`를 상속, `statusCode` 필드 추가. 모든 커스텀 에러의 기본 클래스.

2. **`NotFoundError`** (`src/errors/not-found-error.ts`): `AppError` 상속, statusCode 404 고정.

3. **`ValidationError`** (`src/errors/validation-error.ts`): `AppError` 상속, statusCode 400 고정, `details` 배열로 필드별 검증 실패 정보 포함.

4. **barrel export** (`src/errors/index.ts`): 세 클래스를 한 경로에서 import할 수 있게 re-export.

---

## 3단계: Express 미들웨어 구현

### 구현 순서

1. **`validate`** (`src/middleware/validate.ts`): Zod 스키마를 받아 `req.body`를 파싱, 실패 시 `ZodError` → `ValidationError`로 변환해서 `next(err)`.

2. **`errorHandler`** (`src/middleware/error-handler.ts`): 글로벌 에러 핸들러. `ValidationError`, `AppError`, `SyntaxError`를 분기해서 통일된 에러 응답 생성.

3. **`responseWrapper`** (`src/middleware/response-wrapper.ts`): `res.json()` 오버라이드로 성공 응답을 `{ success: true, data }` 형태로 래핑.

4. **`requestLogger`** (`src/middleware/request-logger.ts`): `res.on("finish")` 이벤트로 요청 완료 후 구조화된 JSON 로그 출력.

5. **barrel export** (`src/middleware/index.ts`): 네 미들웨어를 한 경로에서 import 가능하게 re-export.

### Zod 스키마

`src/schemas/book.schema.ts` — `createBookSchema`와 `updateBookSchema`를 Zod로 정의. title, author, publishedYear의 타입과 제약 조건을 선언적으로 명시.

---

## 4단계: Express 앱 조립

`src/app.ts`에서 미들웨어를 순서대로 등록:

```
1. express.json()        — JSON body 파싱
2. requestLogger         — 요청 로깅
3. responseWrapper       — 응답 래핑
4. book router           — 비즈니스 라우트
5. errorHandler          — 글로벌 에러 처리 (반드시 마지막)
```

서비스 → 컨트롤러 → 라우터 → 앱 조립은 이전 과제와 동일한 수동 DI 패턴.

---

## 5단계: NestJS 레인 셋업

### 의존성 설치

```bash
cd nestjs
pnpm init
pnpm add @nestjs/common @nestjs/core @nestjs/platform-express @nestjs/mapped-types reflect-metadata rxjs class-transformer class-validator
pnpm add -D @nestjs/cli @nestjs/testing @types/express @types/node @types/supertest supertest typescript vitest
```

이 과제에서 새로 추가된 주요 의존성:
- `class-validator` (^0.14.1): 데코레이터 기반 DTO 검증
- `class-transformer` (^0.5.1): plain object → 클래스 인스턴스 변환 (class-validator와 함께 사용)
- `@nestjs/mapped-types` (^2.0.0): `PartialType`, `PickType` 등 DTO 유틸리티

---

## 6단계: NestJS 공통 모듈 구현

### HttpExceptionFilter

`src/common/filters/http-exception.filter.ts` — `@Catch()` 데코레이터로 모든 `HttpException`을 잡아서 `{ success: false, error }` 형태로 변환. Express의 `errorHandler`와 같은 역할.

### TransformInterceptor

`src/common/interceptors/transform.interceptor.ts` — 컨트롤러 반환값을 `{ success: true, data }` 형태로 래핑. RxJS `map` 연산자 사용.

### LoggingInterceptor

`src/common/interceptors/logging.interceptor.ts` — 요청 시작/완료 시점에 구조화된 로그 출력. RxJS `tap` 연산자 사용.

---

## 7단계: NestJS DTO와 ValidationPipe

### DTO 클래스

`src/books/dto/create-book.dto.ts`:
```typescript
@IsString() @IsNotEmpty() title: string;
@IsString() @IsNotEmpty() author: string;
@IsInt() publishedYear: number;
```

`src/books/dto/update-book.dto.ts`: `PartialType(CreateBookDto)`로 모든 필드를 선택적으로 만든다.

### 글로벌 ValidationPipe 등록

`src/main.ts`에서:
```typescript
app.useGlobalPipes(new ValidationPipe({ whitelist: true, transform: true }));
app.useGlobalFilters(new HttpExceptionFilter());
app.useGlobalInterceptors(new LoggingInterceptor(), new TransformInterceptor());
```

- `whitelist: true`: DTO에 정의되지 않은 필드를 자동 제거
- `transform: true`: plain object를 클래스 인스턴스로 자동 변환

---

## 8단계: 테스트

### Express 테스트

**단위 테스트**: 서비스 CRUD 로직 검증
**E2E 테스트**: 
- 성공 응답이 `{ success: true, data }` 형태인지 확인
- 검증 실패 시 `{ success: false, error: { details } }` 형태인지 확인
- 404가 `{ success: false, error }` 형태인지 확인

### NestJS 테스트

**단위 테스트**: 서비스와 컨트롤러 검증
**E2E 테스트**: 동일한 응답 규약 확인

---

## 9단계: 빌드와 검증

### Express

```bash
cd express
pnpm install
pnpm run build
pnpm run test
pnpm run test:e2e
```

### NestJS

```bash
cd nestjs
pnpm install
pnpm run build
pnpm run test
pnpm run test:e2e
```

### curl 수동 검증

```bash
# 성공 응답 확인 — envelope 형식
curl http://localhost:3000/books
# → { "success": true, "data": [] }

# 검증 실패 확인
curl -X POST http://localhost:3000/books \
  -H "Content-Type: application/json" \
  -d '{"title": ""}'
# → { "success": false, "error": { "message": "Validation failed", ... } }
```

---

## 프로젝트 파일 구조 최종 상태

```
04-request-pipeline/
├── README.md
├── docs/concepts/{express/, nestjs/}
├── express/
│   ├── package.json
│   ├── src/
│   │   ├── app.ts, main.ts
│   │   ├── controllers/
│   │   ├── services/
│   │   ├── routes/
│   │   ├── types/
│   │   ├── errors/{app-error.ts, not-found-error.ts, validation-error.ts}
│   │   ├── middleware/{validate.ts, error-handler.ts, response-wrapper.ts, request-logger.ts}
│   │   ├── schemas/book.schema.ts
│   │   └── utils/
│   └── test/{unit/, e2e/}
├── nestjs/
│   ├── package.json, nest-cli.json
│   ├── src/
│   │   ├── app.module.ts, main.ts
│   │   ├── books/{controller, service, module, dto/, entities/}
│   │   └── common/
│   │       ├── filters/http-exception.filter.ts
│   │       └── interceptors/{logging.interceptor.ts, transform.interceptor.ts}
│   └── test/{unit/, e2e/}
└── problem/
```

---

## 사용한 도구 요약

| 도구 | 용도 |
|------|------|
| pnpm | 패키지 매니저 |
| Zod 3.23+ | Express 스키마 검증 |
| class-validator 0.14+ | NestJS DTO 검증 |
| class-transformer 0.5+ | plain object → 클래스 인스턴스 변환 |
| @nestjs/mapped-types | PartialType 등 DTO 유틸리티 |
| tsx | 개발 모드 TypeScript 실행 (watch 포함) |
| supertest | HTTP 통합 테스트 |
| curl | 수동 API 검증 |
