# 04-request-pipeline evidence ledger

근거는 [`README.md`](../../../study/Node-Backend-Architecture/core/04-request-pipeline/README.md), [`express/src/app.ts`](../../../study/Node-Backend-Architecture/core/04-request-pipeline/express/src/app.ts), [`express/src/middleware/validate.ts`](../../../study/Node-Backend-Architecture/core/04-request-pipeline/express/src/middleware/validate.ts), [`express/src/middleware/error-handler.ts`](../../../study/Node-Backend-Architecture/core/04-request-pipeline/express/src/middleware/error-handler.ts), [`nestjs/src/main.ts`](../../../study/Node-Backend-Architecture/core/04-request-pipeline/nestjs/src/main.ts), [`nestjs/src/common/filters/http-exception.filter.ts`](../../../study/Node-Backend-Architecture/core/04-request-pipeline/nestjs/src/common/filters/http-exception.filter.ts), [`nestjs/src/common/interceptors/transform.interceptor.ts`](../../../study/Node-Backend-Architecture/core/04-request-pipeline/nestjs/src/common/interceptors/transform.interceptor.ts), 테스트 출력이다.

## Phase 1

- 순서: 1
- 시간 표지: Phase 1
- 당시 목표: Express 쪽에서 request pipeline 순서를 middleware로 먼저 고정한다.
- 변경 단위: `express/src/app.ts`, `express/src/middleware/*`
- 처음 가설: auth보다 먼저 validation, logging, response wrapper, error handler 순서를 결정해야 이후 API들이 같은 실패 언어를 쓴다.
- 실제 조치: `requestLogger -> express.json -> responseWrapper -> /books router -> errorHandler` 순서로 파이프라인을 만들고 Zod validator를 붙였다.
- CLI: `COREPACK_ENABLE_AUTO_PIN=0 pnpm run test`, `COREPACK_ENABLE_AUTO_PIN=0 pnpm run test:e2e`
- 검증 신호: unit `Tests 16 passed (16)`, e2e `Tests 9 passed (9)`
- 핵심 코드 앵커: `createApp()`, `validate()`, `errorHandler()`
- 새로 배운 것: 이 단계의 주인공은 Books 도메인이 아니라 요청이 들어와 응답으로 나갈 때의 공통 규약이다.
- 다음: 같은 규약을 NestJS에서는 global pipe/filter/interceptor로 올린다.

## Phase 2

- 순서: 2
- 시간 표지: Phase 2
- 당시 목표: NestJS에서 pipeline 책임을 framework primitive로 옮긴다.
- 변경 단위: `nestjs/src/main.ts`, `nestjs/src/common/filters/http-exception.filter.ts`, `nestjs/src/common/interceptors/*`
- 처음 가설: NestJS에서는 middleware보다 global pipe/filter/interceptor가 공통 규약의 중심이 될 것이다.
- 실제 조치: `ValidationPipe`, `HttpExceptionFilter`, `LoggingInterceptor`, `TransformInterceptor`를 전역으로 등록했다.
- CLI: `COREPACK_ENABLE_AUTO_PIN=0 pnpm run test`, `COREPACK_ENABLE_AUTO_PIN=0 pnpm run test:e2e`
- 검증 신호: Nest unit `Tests 7 passed (7)`, e2e `Tests 8 passed (8)`
- 핵심 코드 앵커: `main.ts`, `HttpExceptionFilter`, `TransformInterceptor`
- 새로 배운 것: NestJS 파이프라인은 controller 메서드보다 먼저 "입력 정리 -> 예외 변환 -> 응답 래핑"을 전역 규약으로 올리는 데 강했다.
- 다음: e2e에서 envelope와 log가 실제로 유지되는지 확인한다.

## Phase 3

- 순서: 3
- 시간 표지: Phase 3
- 당시 목표: 성공 응답 envelope, validation failure, missing book, CRUD 전체 흐름을 e2e로 고정한다.
- 변경 단위: `express/test/e2e/pipeline.e2e.test.ts`, `nestjs/test/e2e/pipeline.e2e.test.ts`
- 처음 가설: pipeline 프로젝트는 구현 코드보다 e2e가 더 많은 사실을 보여 준다.
- 실제 조치: Express e2e는 `success/data`, `success:false/error`, full CRUD를 모두 검증했고, 실제 로그 출력까지 남겼다.
- CLI: `pnpm run test:e2e`
- 검증 신호: Express 로그에 `PUT ... statusCode:200`, `DELETE ... statusCode:204`, `GET ... statusCode:404`가 남고, Nest e2e도 8개 시나리오를 통과했다.
- 핵심 코드 앵커: `pipeline.e2e.test.ts`
- 새로 배운 것: 공통 규약은 문서보다 테스트가 더 잘 설명한다. envelope가 정말 일관적인지는 결국 e2e가 보여 준다.
- 다음: `05-auth-and-authorization`에서 이 pipeline 위에 JWT와 RBAC가 올라간다.
