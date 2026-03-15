# 04-request-pipeline series map

이 lab은 CRUD 기능을 더 붙이는 단계가 아니라, 그 CRUD 앞뒤를 감싸는 공통 규약을 세우는 단계다. validation, error handling, logging, response shaping을 handler 바깥으로 끌어내야 이후 auth, persistence, async job 같은 주제를 올려도 API 표면이 흔들리지 않는다.

이번에 소스를 다시 따라가며 보니 중심 질문은 네 가지였다.

- Express에서는 middleware 순서가 어떤 식으로 계약이 되는가
- NestJS에서는 pipe, filter, interceptor가 같은 계약을 어디까지 대체하는가
- 성공과 실패 응답을 누가 `{ success, data }` / `{ success, error }`로 고정하는가
- 로깅은 구현돼 있어도 실제 테스트가 무엇을 검증하고 무엇은 아직 검증하지 않는가

읽는 순서는 Express를 먼저 보는 편이 좋다. `requestLogger -> express.json() -> responseWrapper -> router -> errorHandler` 순서를 먼저 잡아야, NestJS의 `ValidationPipe -> HttpExceptionFilter -> TransformInterceptor`가 같은 문제를 다른 프레임워크 표면으로 푼다는 점이 선명해진다.

## 이 글에서 볼 것

- Zod middleware와 class-validator pipeline이 어떻게 handler 바깥에서 input contract를 만드는지
- 성공/실패 envelope를 공통화하면 controller/service가 얼마나 단순해지는지
- 다만 `DELETE 204`처럼 body가 없는 경로는 양쪽 레인 모두 status-only로 남아, "모든 응답이 동일 envelope"라는 표현은 조금 더 조심해야 한다는 점
- Express의 logging은 실제 e2e에서 관찰되지만, NestJS의 logging interceptor는 구현에는 있고 e2e 계약에는 포함되지 않는다는 현재 상태

## source of truth

- `core/04-request-pipeline/problem/README.md`
- `core/04-request-pipeline/README.md`
- `core/04-request-pipeline/express/src/app.ts`
- `core/04-request-pipeline/express/src/middleware/request-logger.ts`
- `core/04-request-pipeline/express/src/middleware/validate.ts`
- `core/04-request-pipeline/express/src/middleware/response-wrapper.ts`
- `core/04-request-pipeline/express/src/middleware/error-handler.ts`
- `core/04-request-pipeline/express/src/schemas/book.schema.ts`
- `core/04-request-pipeline/express/test/e2e/pipeline.e2e.test.ts`
- `core/04-request-pipeline/nestjs/src/main.ts`
- `core/04-request-pipeline/nestjs/src/books/books.controller.ts`
- `core/04-request-pipeline/nestjs/src/books/dto/create-book.dto.ts`
- `core/04-request-pipeline/nestjs/src/common/filters/http-exception.filter.ts`
- `core/04-request-pipeline/nestjs/src/common/interceptors/logging.interceptor.ts`
- `core/04-request-pipeline/nestjs/src/common/interceptors/transform.interceptor.ts`
- `core/04-request-pipeline/nestjs/test/e2e/pipeline.e2e.test.ts`

## 구현 흐름 한눈에 보기

1. Express에서 body validation과 response shaping을 middleware로 고정한다.
2. Express error handler가 validation error, app error, malformed JSON을 같은 실패 envelope로 모은다.
3. NestJS에서 `ValidationPipe`, `HttpExceptionFilter`, `TransformInterceptor`로 거의 같은 계약을 다시 세운다.
4. 다만 NestJS 로깅은 `main.ts`에는 구현돼 있지만 e2e app에는 붙지 않아, 현재 검증 계약은 logging이 아니라 validation/error/transform까지다.
5. `DELETE` 성공 경로는 Express `res.status(204).send()`와 Nest `@HttpCode(NO_CONTENT)`라서 body가 비어 있고, e2e도 status만 잠근다.

## 대표 검증

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run build
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test:e2e
Test Files  4 passed (4)
Tests       25 passed (25)
```

```bash
$ node -e "const request=require('supertest'); const { createApp } = require('./dist/app.js'); request(createApp()).post('/books').set('Content-Type','application/json').send('{\"title\":').end((_,res)=>console.log(res.status,res.body))"
400 { success: false, error: { message: 'Invalid JSON', statusCode: 400 } }
```

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run build
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test:e2e
Test Files  2 passed (2)
Tests       15 passed (15)
```

## 다음 프로젝트와의 연결

다음 `05-auth-and-authorization`은 바로 이 pipeline 위에 JWT와 RBAC를 올린다. 요청이 어디서 검증되고, 실패가 어떤 envelope로 나가고, 성공 응답이 어떤 표면으로 감싸지는지 먼저 안정돼 있어야 보안 규칙도 어지럽지 않게 얹을 수 있다.
