# 04-request-pipeline evidence ledger

이 lab의 path history도 `2026-03-12` 이관 커밋 한 번으로 압축돼 있어, chronology는 `problem`, Express/NestJS 구현, 테스트, 추가 재실행 CLI를 따라 다시 복원했다. 기존 blog 본문은 사실 근거로 사용하지 않았다.

| 순서 | 시간 표지 | 당시 목표 | 변경 단위 | 처음 가설 | 실제 조치 | CLI | 검증 신호 | 핵심 코드 앵커 | 새로 배운 것 | 다음 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Phase 1 | Express에서 handler 바깥에 validation을 세운다 | `express/src/app.ts`, `express/src/routes/book.router.ts`, `express/src/middleware/validate.ts`, `express/src/schemas/book.schema.ts` | controller 안에서 조건문으로 검사해도 충분할 것 같았다 | `express.json()` 뒤에 들어온 body를 Zod schema로 검사하고, route는 `validate(schema)`를 먼저 통과한 뒤 controller로 들어가게 했다 | `COREPACK_ENABLE_AUTO_PIN=0 pnpm run build`, `COREPACK_ENABLE_AUTO_PIN=0 pnpm run test`, `COREPACK_ENABLE_AUTO_PIN=0 pnpm run test:e2e` (`express/`) | unit 16개, e2e 9개 통과 | `router.post("/", validate(CreateBookSchema), asyncHandler(controller.create))` | validation을 pipeline 단계로 빼면 controller는 "이미 검증된 입력"을 전제로 훨씬 단순해진다 | 성공/실패 응답을 같은 표면으로 묶는다 |
| 2 | Phase 2 | Express 성공/실패 응답을 공통 envelope로 고정한다 | `express/src/middleware/response-wrapper.ts`, `express/src/middleware/error-handler.ts`, `express/src/middleware/request-logger.ts` | 성공 응답만 감싸면 충분할 것 같았다 | 성공은 `{ success: true, data }`, 실패는 `{ success: false, error }`로 통일했고, `res.on("finish")` 기반 logger로 응답 완료 시점을 기록하게 했다 | 같은 명령 재실행 + `node -e "const request=require('supertest'); ... send('{\\\"title\\\":') ..."` (`express/`) | malformed JSON도 `400 { success:false, error:{ message:'Invalid JSON', statusCode:400 } }` 반환 | `if (err instanceof SyntaxError && "body" in err)` | Express는 실패 응답도 logger가 잡기 때문에, e2e 출력만으로도 logging이 실제 pipeline 일부임을 관찰할 수 있다 | NestJS에서 같은 규약을 다시 세운다 |
| 3 | Phase 3 | NestJS에서 validation, filter, transform을 global pipeline으로 재구성한다 | `nestjs/src/main.ts`, `nestjs/src/books/books.controller.ts`, `nestjs/src/books/dto/create-book.dto.ts`, `nestjs/src/common/filters/http-exception.filter.ts`, `nestjs/src/common/interceptors/transform.interceptor.ts` | NestJS는 기본값만으로도 충분히 비슷한 응답을 줄 것 같았다 | `ValidationPipe`, `HttpExceptionFilter`, `TransformInterceptor`를 직접 연결해 unknown property와 bad request까지 프로젝트 공통 envelope로 맞췄다 | `COREPACK_ENABLE_AUTO_PIN=0 pnpm run build`, `COREPACK_ENABLE_AUTO_PIN=0 pnpm run test`, `COREPACK_ENABLE_AUTO_PIN=0 pnpm run test:e2e` (`nestjs/`) | unit 7개, e2e 8개 통과 | `response.status(status).json({ success: false, error: errorBody })` | NestJS도 프레임워크 기본 응답을 그대로 쓰지 않고, 팀 규약을 filter/interceptor로 다시 명시한다. 단, `204` delete success는 body 없이 status만 남는다 | logging이 실제로 어디까지 검증되는지 확인한다 |
| 4 | Phase 4 | 구현 범위와 검증 범위를 분리한다 | `nestjs/src/common/interceptors/logging.interceptor.ts`, `nestjs/test/e2e/pipeline.e2e.test.ts` | `main.ts`에 logging interceptor가 있으니 e2e도 그 흐름을 다 덮는다고 생각하기 쉽다 | 실제 e2e app은 `ValidationPipe`, `HttpExceptionFilter`, `TransformInterceptor`만 붙이고 `LoggingInterceptor`는 등록하지 않는다는 점을 확인했다 | 위 Nest 명령 재실행 + e2e 소스 점검 | logging은 구현 존재만 확인되고, 검증 계약은 validation/error/transform까지 | `app.useGlobalInterceptors(new TransformInterceptor())` (e2e) vs `new LoggingInterceptor(), new TransformInterceptor()` (`main.ts`) | "구현돼 있음"과 "테스트가 고정함"은 다르며, 문서도 이 둘을 섞지 말아야 한다 | `05-auth-and-authorization`에서 pipeline 위에 JWT/RBAC를 올린다 |

## 근거 파일

- `core/04-request-pipeline/problem/README.md`
- `core/04-request-pipeline/README.md`
- `core/04-request-pipeline/express/src/app.ts`
- `core/04-request-pipeline/express/src/middleware/request-logger.ts`
- `core/04-request-pipeline/express/src/middleware/validate.ts`
- `core/04-request-pipeline/express/src/middleware/response-wrapper.ts`
- `core/04-request-pipeline/express/src/middleware/error-handler.ts`
- `core/04-request-pipeline/express/src/schemas/book.schema.ts`
- `core/04-request-pipeline/express/test/unit/validate.test.ts`
- `core/04-request-pipeline/express/test/unit/errors.test.ts`
- `core/04-request-pipeline/express/test/e2e/pipeline.e2e.test.ts`
- `core/04-request-pipeline/nestjs/src/main.ts`
- `core/04-request-pipeline/nestjs/src/books/books.controller.ts`
- `core/04-request-pipeline/nestjs/src/books/books.service.ts`
- `core/04-request-pipeline/nestjs/src/books/dto/create-book.dto.ts`
- `core/04-request-pipeline/nestjs/src/common/filters/http-exception.filter.ts`
- `core/04-request-pipeline/nestjs/src/common/interceptors/logging.interceptor.ts`
- `core/04-request-pipeline/nestjs/src/common/interceptors/transform.interceptor.ts`
- `core/04-request-pipeline/nestjs/test/unit/books.service.test.ts`
- `core/04-request-pipeline/nestjs/test/e2e/pipeline.e2e.test.ts`

## 이번 후속 보강에서 더 선명히 남긴 점

- 양쪽 레인 모두 JSON success/error envelope는 강하지만 `DELETE 204`는 예외로 body 대신 status만 고정한다.
- Express logging은 test run 출력으로 관찰되지만, e2e matcher가 log payload를 직접 assert하는 형태는 아니다.
