# 04-request-pipeline development timeline

REST foundation에서 Books CRUD를 두 레인으로 비교했다면, 여기서는 그 CRUD가 어떤 공통 규약 위에서 움직여야 하는지가 주제가 된다. 소스를 읽다 보면 분명해진다. 새 기능을 늘린 게 아니라 validation, logging, error envelope, response wrapper를 먼저 고정했다. 그래서 이후 auth와 persistence가 들어와도 요청 흐름이 흔들리지 않는다.

## 구현 순서 요약

- Express에서 middleware 순서를 먼저 고정한다.
- NestJS에서 같은 규약을 global pipe/filter/interceptor로 다시 세운다.
- e2e로 success/data envelope와 실패 응답의 일관성을 확인한다.

## Phase 1

- 당시 목표: Express에서 요청이 들어와 응답으로 나가기까지의 순서를 middleware로 명시한다.
- 변경 단위: `express/src/app.ts`, `express/src/middleware/validate.ts`, `express/src/middleware/error-handler.ts`
- 처음 가설: auth나 DB보다 먼저 공통 실패 언어를 정해 두지 않으면 프로젝트가 커질수록 응답 형식이 흐트러진다.
- 실제 진행: `createApp()`에서 `requestLogger`, `express.json`, `responseWrapper`, router, `errorHandler`를 순서대로 등록하고, Zod validator가 실패를 `ValidationError`로 바꿔 넘기게 했다.

CLI:

```bash
$ cd express
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test:e2e
Tests 16 passed (16)
Tests 9 passed (9)
```

검증 신호:

- unit test는 validator와 error handler의 envelope를 검증한다.
- e2e는 full CRUD가 모두 `success/data` 형식을 유지하는지 확인한다.

핵심 코드:

```ts
app.use(requestLogger);
app.use(express.json());
app.use(responseWrapper);
app.use("/books", createBookRouter());
app.use(errorHandler);
```

왜 이 코드가 중요했는가:

이 순서가 곧 프로젝트의 규약이다. logger는 제일 먼저, response wrapper는 라우트 앞, error handler는 라우트 뒤에 있어야 한다는 판단이 여기서 고정된다.

새로 배운 것:

- middleware 프로젝트의 본질은 개별 함수보다 "순서가 의미를 만든다"는 점에 있다.

## Phase 2

- 당시 목표: NestJS에서 같은 규약을 framework primitive로 끌어올린다.
- 변경 단위: `nestjs/src/main.ts`, `nestjs/src/common/filters/http-exception.filter.ts`, `nestjs/src/common/interceptors/transform.interceptor.ts`
- 처음 가설: NestJS는 route별 middleware보다 전역 pipe/filter/interceptor로 공통 규약을 묶는 편이 자연스럽다.
- 실제 진행: `ValidationPipe`로 입력 정리를, `HttpExceptionFilter`로 오류 envelope를, `TransformInterceptor`로 성공 응답 래핑을 전역 등록했다.

CLI:

```bash
$ cd ../nestjs
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test:e2e
Tests 7 passed (7)
Tests 8 passed (8)
```

검증 신호:

- unit test가 service 동작을 유지하는 동안 e2e가 전역 파이프라인의 실제 적용 여부를 닫는다.
- NestJS에서도 성공 응답은 `success: true`, 실패 응답은 `success: false`로 맞춰진다.

핵심 코드:

```ts
app.useGlobalPipes(new ValidationPipe({ whitelist: true, forbidNonWhitelisted: true, transform: true }));
app.useGlobalFilters(new HttpExceptionFilter());
app.useGlobalInterceptors(new LoggingInterceptor(), new TransformInterceptor());
```

왜 이 코드가 중요했는가:

Express에선 app wiring이 규약을 만들었고, NestJS에선 bootstrap이 그 역할을 맡는다. 이 차이를 잡아야 이후 auth나 events를 어디에 꽂을지 흔들리지 않는다.

새로 배운 것:

- 프레임워크가 달라도 공통 규약의 핵심은 같다. 다만 Express는 "등록 순서"로, NestJS는 "전역 primitive"로 그걸 표현한다.

## Phase 3

- 당시 목표: envelope와 로그가 실제 CRUD 시나리오에서 유지되는지 확인한다.
- 변경 단위: `express/test/e2e/pipeline.e2e.test.ts`, `nestjs/test/e2e/pipeline.e2e.test.ts`
- 처음 가설: request pipeline은 코드보다 e2e 출력이 더 많은 사실을 말해 줄 것이다.
- 실제 진행: Express e2e는 success wrapper, validation failure, missing resource, full CRUD를 한 파일에서 모두 검증했고, 실제 로그도 stdout에 남겼다.

CLI:

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test:e2e
{"timestamp":"...","method":"PUT","url":"/books/...","statusCode":200,"durationMs":1}
{"timestamp":"...","method":"DELETE","url":"/books/...","statusCode":204,"durationMs":0}
{"timestamp":"...","method":"GET","url":"/books/...","statusCode":404,"durationMs":0}
```

검증 신호:

- 성공 path와 실패 path가 모두 같은 logging shape를 쓴다.
- Nest e2e 8개 시나리오도 같은 envelope를 유지하며 통과한다.

핵심 코드:

```ts
response.status(status).json({
  success: false,
  error: errorBody,
});
```

왜 이 코드가 중요했는가:

이 시점부터 나머지 프로젝트는 새로운 기능을 추가해도 응답 형식을 다시 설계할 필요가 없어진다. pipeline이 먼저 고정됐기 때문이다.

새로 배운 것:

- API 프로젝트를 안정화하는 가장 빠른 길은 기능 추가가 아니라 실패 언어를 먼저 고정하는 일이다.

다음:

- [`../05-auth-and-authorization/00-series-map.md`](../05-auth-and-authorization/00-series-map.md)에서 이 pipeline 위에 JWT와 RBAC 규칙이 올라간다.
