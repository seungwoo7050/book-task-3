# 03-rest-api-foundations evidence ledger

근거는 [`README.md`](../../../study/Node-Backend-Architecture/core/03-rest-api-foundations/README.md), [`express/src/app.ts`](../../../study/Node-Backend-Architecture/core/03-rest-api-foundations/express/src/app.ts), [`express/src/services/book.service.ts`](../../../study/Node-Backend-Architecture/core/03-rest-api-foundations/express/src/services/book.service.ts), [`nestjs/src/books/books.controller.ts`](../../../study/Node-Backend-Architecture/core/03-rest-api-foundations/nestjs/src/books/books.controller.ts), [`nestjs/src/books/books.service.ts`](../../../study/Node-Backend-Architecture/core/03-rest-api-foundations/nestjs/src/books/books.service.ts), 두 레인의 테스트 출력이다.

## Phase 1

- 순서: 1
- 시간 표지: Phase 1
- 당시 목표: 같은 Books CRUD를 Express 쪽에서 수동 DI와 composition root로 먼저 푼다.
- 변경 단위: `express/src/app.ts`, `express/src/controllers/book.controller.ts`, `express/src/services/book.service.ts`
- 처음 가설: 프레임워크 비교를 하려면 먼저 Express 쪽에서 service -> controller -> router -> app 연결을 손으로 드러내야 한다.
- 실제 조치: `createApp()`이 `BookService`, `BookController`, `bookRouter`를 직접 생성해 mount하고, `BookService`는 in-memory `Map`으로 CRUD를 처리한다.
- CLI: `COREPACK_ENABLE_AUTO_PIN=0 pnpm run build`, `COREPACK_ENABLE_AUTO_PIN=0 pnpm run test`
- 검증 신호: `✓ test/unit/book.service.test.ts (9 tests)`, `✓ test/e2e/books.e2e.test.ts (9 tests)`, `Tests 18 passed (18)`
- 핵심 코드 앵커: `createApp()`, `BookService.create()`
- 새로 배운 것: Express 비교의 핵심은 기능 수가 아니라 "의존성을 어디서 연결하는지"를 눈으로 볼 수 있다는 데 있었다.
- 다음: 같은 문제를 NestJS DI container 안에서 다시 묶는다.

## Phase 2

- 순서: 2
- 시간 표지: Phase 2
- 당시 목표: 같은 CRUD 계약을 NestJS module/controller/service로 옮겨 framework DI 차이를 드러낸다.
- 변경 단위: `nestjs/src/books/books.controller.ts`, `nestjs/src/books/books.service.ts`, `nestjs/src/books/books.module.ts`
- 처음 가설: NestJS는 route decorator와 예외 처리 기본값이 있으니 Express에서 손으로 하던 wiring이 module 경계로 이동할 것이다.
- 실제 조치: `@Controller("books")`, `@Injectable()` service, DTO/entity 파일을 나누고 `NotFoundException`으로 실패를 처리했다.
- CLI: `COREPACK_ENABLE_AUTO_PIN=0 pnpm run build`, `COREPACK_ENABLE_AUTO_PIN=0 pnpm run test`, `COREPACK_ENABLE_AUTO_PIN=0 pnpm run test:e2e`
- 검증 신호: `Tests 8 passed (8)` unit, `Tests 8 passed (8)` e2e
- 핵심 코드 앵커: `BooksController`, `BooksService.findOne()`
- 새로 배운 것: NestJS의 편의는 코드를 덜 쓰는 데 있지 않고, "controller는 요청만 받고 service는 예외를 던진다"는 역할 분담을 프레임워크가 받쳐 준다는 점에 있었다.
- 다음: 두 레인이 같은 CRUD 계약을 유지하는지 테스트로 비교한다.

## Phase 3

- 순서: 3
- 시간 표지: Phase 3
- 당시 목표: 레인이 달라도 같은 Books 계약을 재현할 수 있음을 확인한다.
- 변경 단위: `express/test/*`, `nestjs/test/*`
- 처음 가설: 레인 비교 프로젝트는 구현 설명보다 "둘 다 같은 문제를 어떻게 닫았는가"를 검증으로 보여 줘야 한다.
- 실제 조치: Express는 unit/e2e를 함께 돌리고, NestJS는 service unit과 e2e를 분리해 같은 CRUD 시나리오를 재현했다.
- CLI: `pnpm run test`, `pnpm run test:e2e`
- 검증 신호: Express `18 passed`, NestJS `8 + 8 passed`
- 핵심 코드 앵커: `express/test/e2e/books.e2e.test.ts`, `nestjs/test/e2e/books.e2e.test.ts`
- 새로 배운 것: 비교 학습의 핵심은 어느 프레임워크가 더 짧은지가 아니라 "같은 계약을 어떤 레이어 분해로 설명하는가"를 보는 데 있다.
- 다음: `04-request-pipeline`에서 CRUD 기능보다 공통 요청 규약을 먼저 고정한다.
