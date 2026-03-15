# 04-request-pipeline structure plan

이 문서는 CRUD 설명문이 아니라, validation·response shaping·error handling·logging이 왜 feature 바깥의 공통 pipeline이어야 하는지 보여 주는 글이어야 한다. 서사의 중심은 `Express ordering -> malformed JSON까지 포함한 error envelope -> Nest global pipeline -> 구현과 검증 범위 분리`다.

## 읽기 구조

1. 왜 이 lab이 CRUD 다음이 아니라 auth 이전에 오는지 먼저 짚는다.
2. Express `app.ts`의 middleware ordering을 기준으로 pipeline 순서를 설명한다.
3. `validate`, `responseWrapper`, `errorHandler`, `requestLogger`가 각자 어떤 전제를 만드는지 잇는다.
4. NestJS `main.ts`, controller-level `ValidationPipe`, `HttpExceptionFilter`, `TransformInterceptor`로 같은 규약을 어떻게 옮기는지 보여 준다.
5. 마지막에는 NestJS logging이 구현에는 있지만 e2e에선 검증되지 않는다는 현재 한계를 분리해 적는다.

## 반드시 남길 근거

- Express `src/app.ts`
- Express `src/middleware/request-logger.ts`
- Express `src/middleware/validate.ts`
- Express `src/middleware/response-wrapper.ts`
- Express `src/middleware/error-handler.ts`
- Express malformed JSON 직접 재실행 결과
- NestJS `src/main.ts`
- NestJS `src/books/books.controller.ts`
- NestJS `src/books/dto/create-book.dto.ts`
- NestJS `src/common/filters/http-exception.filter.ts`
- NestJS `src/common/interceptors/logging.interceptor.ts`
- NestJS `src/common/interceptors/transform.interceptor.ts`
- NestJS e2e bootstrap 코드

## 리라이트 톤

- middleware/filter/interceptor를 사전식으로 나열하지 않는다.
- 순서가 왜 중요한지, 어떤 단계가 어떤 전제를 만드는지 중심으로 쓴다.
- 검증된 것과 source만으로 확인한 것을 섞지 않는다.
