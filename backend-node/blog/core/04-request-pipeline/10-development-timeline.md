# 04-request-pipeline development timeline

`03-rest-api-foundations`에서 같은 CRUD를 두 프레임워크로 비교했다면, 이 lab은 그 CRUD보다 앞에서 API 전체를 지배하는 공통 흐름을 고정하는 단계다. 이번 재검토에서는 "middleware/filter/interceptor를 배웠다"는 식의 분류보다, 실제로 어떤 순서가 계약이 되고 그 순서가 바뀌면 무엇이 흐트러지는지에 집중해 다시 정리했다.

## 흐름 먼저 보기

1. Express에서 validation을 route handler 밖으로 빼고, 응답 래핑과 오류 처리를 middleware 순서로 묶는다.
2. Express가 malformed JSON까지 같은 실패 envelope로 모으는지 직접 확인한다.
3. NestJS에서 `ValidationPipe`, `HttpExceptionFilter`, `TransformInterceptor`를 global pipeline으로 다시 세운다.
4. NestJS 로깅은 구현돼 있지만 e2e app에는 연결되지 않아, 현재 테스트가 보장하는 범위를 따로 구분한다.

## Express에서 순서 자체를 규약으로 만든 장면

Express 쪽에서 가장 먼저 봐야 할 파일은 `app.ts`다. 여기서는 feature 코드보다 middleware ordering이 더 중요하다.

```ts
app.use(requestLogger);
app.use(express.json());
app.use(responseWrapper);

app.use("/books", createBookRouter());

app.use(errorHandler);
```

이 순서가 중요한 이유는 각 단계가 다음 단계의 전제를 만들어 주기 때문이다. `express.json()`이 body를 파싱한 뒤에야 `validate()`가 schema 검사로 들어갈 수 있고, `responseWrapper`는 route handler가 성공 응답으로 호출하는 `res.json()`을 가로채야 하므로 라우트 앞에 있어야 한다. 반대로 `errorHandler`는 앞에서 던진 예외를 한곳에서 모아야 하니 맨 뒤에 있어야 한다.

route 단에서도 validation은 이미 handler 밖으로 분리돼 있다.

```ts
router.post("/", validate(CreateBookSchema), asyncHandler(controller.create));
router.put("/:id", validate(UpdateBookSchema), asyncHandler(controller.update));
```

`validate()`는 Zod 오류를 `ValidationError("검증 실패", details)`로 바꿔 다음 단계로 넘긴다.

```ts
req.body = schema.parse(req.body);
...
next(new ValidationError("검증 실패", details));
```

그래서 controller는 `req.body`를 다시 해석하지 않고 service 호출에만 집중할 수 있다. pipeline을 세운다는 말이 추상적으로 들릴 수 있지만, 실제로는 handler 안의 방어 코드를 middleware로 끌어내는 일에 가깝다.

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run build
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test:e2e
Test Files  4 passed (4)
Tests       25 passed (25)
```

Express 재실행에서는 unit 16개와 e2e 9개가 모두 통과했고, e2e 출력에 `requestLogger`의 JSON 로그가 실제로 찍혔다. 즉 이 lane에서는 logging도 현재 테스트에서 관찰 가능한 파이프라인 일부다.

## 성공과 실패를 같은 표면으로 고정한 장면

success envelope는 `responseWrapper`가 담당한다.

```ts
res.json = function (body?: unknown): Response {
  if (body && typeof body === "object" && "success" in (body as Record<string, unknown>)) {
    return originalJson(body);
  }
  return originalJson({ success: true, data: body });
};
```

이 코드가 생기면 controller는 결과 객체만 넘기면 되고, API 표면은 바깥에서 `{ success: true, data }`로 통일된다. error path는 `errorHandler`가 맡는다.

```ts
if (err instanceof ValidationError) {
  res.status(err.statusCode).json({
    success: false,
    error: {
      message: err.message,
      statusCode: err.statusCode,
      details: err.details,
    },
  });
  return;
}
```

여기서 한 단계 더 확인하고 싶었던 건 malformed JSON이었다. e2e는 missing field, invalid type, negative price, 404를 모두 검증하지만 `express.json()`이 던지는 `SyntaxError` branch는 직접 치지 않는다. 그래서 빌드 결과물에 malformed body를 넣어 봤다.

```bash
$ node -e "const request=require('supertest'); const { createApp } = require('./dist/app.js'); request(createApp()).post('/books').set('Content-Type','application/json').send('{\"title\":').end((_,res)=>console.log(res.status,res.body))"
400 { success: false, error: { message: 'Invalid JSON', statusCode: 400 } }
```

이 결과로 Express pipeline은 validation failure뿐 아니라 parse failure까지도 같은 실패 envelope 안으로 모은다는 점이 분명해졌다.

여기서 한 가지 더 조심해야 할 점도 있었다. 이 lab은 성공/실패 envelope를 공통화한다고 설명할 수 있지만, 그 말이 literal하게 모든 status code에 적용되는 건 아니다. Express `BookController.delete()`는 `res.status(204).send()`로 끝나고, e2e도 삭제 성공에서는 body가 아니라 `204` status만 본다. 즉 "성공 응답이 전부 `{ success, data }`"라는 표현은 JSON body가 있는 경로에 더 잘 맞는다.

## NestJS에서 같은 문제를 global pipeline으로 다시 세운 장면

NestJS 쪽에서는 이 흐름이 `main.ts`에서 전역 설정으로 드러난다.

```ts
app.useGlobalPipes(
  new ValidationPipe({
    whitelist: true,
    forbidNonWhitelisted: true,
    transform: true,
  }),
);
app.useGlobalFilters(new HttpExceptionFilter());
app.useGlobalInterceptors(
  new LoggingInterceptor(),
  new TransformInterceptor(),
);
```

이 구성만 보면 "NestJS는 전역 설정 한 번으로 끝난다"처럼 보일 수 있지만, controller는 여전히 route별 body type을 분명히 적고 있다.

```ts
@Post()
create(
  @Body(
    new ValidationPipe({
      transform: true,
      whitelist: true,
      forbidNonWhitelisted: true,
      expectedType: CreateBookDto,
    }),
  )
  dto: CreateBookDto,
) {
  return this.booksService.create(dto);
}
```

DTO도 이제는 단순 타입 이름이 아니라 `class-validator` 규칙을 갖는다.

```ts
@IsInt({ message: "Published year must be an integer" })
@Min(1000)
@Max(2100)
publishedYear!: number;
```

성공 응답은 `TransformInterceptor`가 감싸고, 실패 응답은 `HttpExceptionFilter`가 모은다.

```ts
return next.handle().pipe(
  map((data) => ({
    success: true as const,
    data,
  })),
);
```

```ts
response.status(status).json({
  success: false,
  error: errorBody,
});
```

즉 Express가 순차 middleware로 해결한 문제를, NestJS는 전역 pipe/filter/interceptor와 decorator 기반 route declaration으로 풀고 있다.

## 구현과 검증의 범위를 분리해서 본 장면

이번에 다시 보면서 가장 중요했던 건 "구현돼 있는 것"과 "테스트가 실제로 보장하는 것"을 나누는 일이었다. NestJS `main.ts`에는 `LoggingInterceptor`가 전역으로 등록돼 있다. 하지만 e2e 테스트는 test app을 따로 만들면서 `ValidationPipe`, `HttpExceptionFilter`, `TransformInterceptor`만 연결하고 `LoggingInterceptor`는 붙이지 않는다.

```ts
app.useGlobalPipes(new ValidationPipe(...));
app.useGlobalFilters(new HttpExceptionFilter());
app.useGlobalInterceptors(new TransformInterceptor());
```

그래서 현재 NestJS lane에서 검증된 계약은 validation, error envelope, success envelope까지고, logging은 구현 존재는 확인되지만 e2e로 고정된 규약은 아니다. 이 차이를 분리해 두어야 문서가 "구현 전체가 검증됐다"는 과장을 피할 수 있다.

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run build
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test:e2e
Test Files  2 passed (2)
Tests       15 passed (15)
```

unit 7개와 e2e 8개가 모두 통과했고, e2e는 missing field, invalid type, unknown property, partial update, 404, full CRUD까지 덮는다. 그러니 이 lab의 핵심 산출물은 CRUD 기능이 아니라, 그 CRUD가 올라타는 바닥 규약이 양쪽 프레임워크에서 어떻게 서는지 비교 가능한 형태로 드러난 것이라고 보는 편이 맞다.

여기서도 204 경로 예외를 같이 적어 두는 편이 정확했다. Nest `BooksController.remove()`는 값을 return하지 않고 `@HttpCode(HttpStatus.NO_CONTENT)`만 남긴다. 그래서 `TransformInterceptor`가 담당하는 `{ success: true, data }` 래핑은 사실상 body가 있는 경로를 중심으로 이해해야 한다. e2e도 삭제 성공에서는 envelope matcher가 아니라 status matcher만 쓴다.

## 여기서 남는 것

이 문서를 다시 쓰고 나니 다음 lab과의 연결도 더 선명해졌다. auth와 authorization은 개별 feature처럼 보이지만, 실제로는 이미 정해 둔 validation/error/response pipeline 위에 얹히는 정책이다. 그래서 `05-auth-and-authorization`은 보안 규칙을 새로 만든다기보다, 여기서 고정한 요청 파이프라인 위에 인증과 권한 판단을 올리는 단계로 읽는 편이 자연스럽다.
