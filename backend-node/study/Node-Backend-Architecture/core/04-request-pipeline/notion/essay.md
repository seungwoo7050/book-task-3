# 요청 파이프라인을 직접 만들어 보면 달라지는 것

## 왜 auth보다 먼저인가

보통은 인증(auth)을 파이프라인보다 먼저 배우고 싶어 한다. 그런데 인증도 결국 "요청이 들어오면 검증하고, 실패하면 적절한 에러를 반환하는" 파이프라인의 한 단계다. 인증을 제대로 구현하려면 validation, error handling, response shaping이 먼저 정리되어 있어야 한다.

그래서 이 과제는 auth 전에 놓는다. 여기서 만든 규약이 이후 auth, DB, capstone까지 그대로 재사용된다.

## 이전 과제에서 빠져 있던 것

`03-rest-api-foundations`에서 Books CRUD를 만들었지만, 몇 가지가 하드코딩 상태였다:

- **검증**: 컨트롤러나 서비스 안에 직접 `if (!title)` 같은 코드가 들어 있었다
- **에러 응답**: `res.status(404).json({ error: "..." })`를 여기저기서 직접 호출했다
- **응답 형식**: 성공 응답과 에러 응답의 구조가 달랐다
- **로깅**: 아예 없었다

이 과제는 이 네 가지를 **공통 미들웨어(Express) 또는 인터셉터/필터(NestJS)**로 추출해서, 컨트롤러가 비즈니스 로직에만 집중하도록 만든다.

## Express 레인: 미들웨어 체인으로 파이프라인 조립

### Zod로 검증 미들웨어 만들기

Express에서 검증을 공통화하기 위해 **Zod**를 선택했다. Zod는 스키마를 정의하면 파싱과 검증을 동시에 처리하고, 실패 시 구조화된 에러 목록을 반환한다.

`validate(schema)` 미들웨어를 만들어서 라우터에 꽂는 구조다:

```typescript
router.post("/", validate(createBookSchema), asyncHandler(controller.create));
```

요청 본문이 스키마에 맞지 않으면 `ZodError`가 나고, 이걸 `ValidationError`로 변환해서 `next(err)`로 넘긴다. 컨트롤러는 검증이 된 데이터만 받는다.

### 계층적 에러 클래스

에러를 세분화하기 위해 에러 클래스 계층을 만들었다:

- `AppError` — 기본 에러 클래스 (statusCode 포함)
- `NotFoundError extends AppError` — 404
- `ValidationError extends AppError` — 400 + details 배열

이렇게 하면 에러 핸들러에서 `instanceof` 체크로 에러 종류에 따라 다른 응답을 만들 수 있다.

### 글로벌 에러 핸들러

`errorHandler` 미들웨어가 모든 에러를 한 곳에서 처리한다:

- `ValidationError` → 400 + `{ success: false, error: { message, statusCode, details } }`
- `AppError` → 해당 statusCode + `{ success: false, error: { message, statusCode } }`
- `SyntaxError` (깨진 JSON) → 400
- 그 외 → 500 + `console.error`

컨트롤러에서 에러 응답 형식을 신경 쓸 필요가 없어진다.

### 응답 래퍼

`responseWrapper` 미들웨어가 성공 응답을 `{ success: true, data: ... }` 형태로 감싼다. `res.json()`을 오버라이드하는 방식이라 컨트롤러 코드를 바꿀 필요가 없다.

이러면 API를 쓰는 클라이언트가 `success` 필드만 보고 성공/실패를 구분할 수 있다. 성공과 실패의 응답 형식이 통일된다.

### 요청 로거

`requestLogger` 미들웨어가 모든 요청에 대해 method, URL, 상태 코드, 소요 시간을 구조화된 JSON으로 로깅한다. `res.on("finish")` 이벤트를 사용해서 응답이 완료된 후에 기록한다.

## NestJS 레인: 필터와 인터셉터로 파이프라인 구성

### class-validator + class-transformer로 DTO 검증

NestJS에서는 `class-validator`와 `class-transformer`를 사용한다. DTO 클래스에 데코레이터(`@IsString()`, `@IsNotEmpty()`, `@IsInt()` 등)를 붙이고, 글로벌 `ValidationPipe`를 등록하면 자동으로 검증된다.

Express에서 직접 만든 `validate()` 미들웨어와 같은 역할을, NestJS는 프레임워크 수준에서 제공하는 것이다.

### HttpExceptionFilter로 에러 응답 통일

`HttpExceptionFilter`는 NestJS의 `ExceptionFilter`를 구현해서, 모든 HTTP 예외를 `{ success: false, error: { ... } }` 형태로 변환한다. Express의 `errorHandler`와 역할이 같지만, NestJS의 `@Catch()` 데코레이터로 선언적으로 등록한다.

### TransformInterceptor로 응답 래핑

`TransformInterceptor`는 컨트롤러의 반환값을 `{ success: true, data: ... }` 형태로 감싼다. Express의 `responseWrapper`와 같은 역할이지만, RxJS의 `map` 연산자를 사용한다.

### LoggingInterceptor로 요청 로깅

`LoggingInterceptor`는 요청 시작과 완료를 기록한다. Express의 `requestLogger`와 같은 역할이지만, NestJS 인터셉터의 `intercept()` 메서드와 RxJS의 `tap` 연산자를 사용한다.

## Express와 NestJS의 파이프라인 비교

| 관점 | Express | NestJS |
|------|---------|--------|
| 검증 | Zod + 커스텀 미들웨어 | class-validator + ValidationPipe |
| 에러 처리 | 에러 핸들러 미들웨어 | ExceptionFilter |
| 응답 래핑 | res.json() 오버라이드 | Interceptor + RxJS map |
| 로깅 | res.on("finish") 미들웨어 | Interceptor + RxJS tap |
| 등록 방식 | app.use()로 수동 등록 | 데코레이터 + 글로벌 등록 |

Express에서는 미들웨어 하나로 모든 cross-cutting concern을 처리하지만, NestJS에서는 각각 전용 추상화(Pipe, Filter, Interceptor, Guard)가 있다. 이 분리는 NestJS가 더 복잡해 보일 수 있지만, 각 concern의 실행 순서가 명확해지는 장점이 있다.

## 이 과제에서 만든 규약이 이후에 쓰이는 곳

- **응답 envelope** (`{ success, data }` / `{ success, error }`): `05` ~ `10` 전체에서 동일하게 유지된다
- **검증 파이프라인**: `05-auth`에서 로그인 요청 검증, `06-persistence`에서 DB 입력 검증에 재사용된다
- **에러 클래스 계층**: `05-auth`에서 `UnauthorizedError`, `ForbiddenError`가 추가된다
- **요청 로깅**: `08-production-readiness`에서 구조화 로깅(structured logging)으로 발전한다

이 과제를 건너뛰면, 이후의 모든 과제에서 에러 응답 형식과 검증 로직이 뒤죽박죽이 된다. 파이프라인을 먼저 정리해 두는 게 나머지 과제를 진행하는 속도를 결정한다.
