# 03-rest-api-foundations evidence ledger

이 lab의 path history도 `2026-03-12` 이관 커밋 한 번으로 압축돼 있어, chronology는 `problem`, 두 구현 레인, 테스트, 직접 재실행한 검증 명령을 따라 다시 복원했다. 기존 blog 본문은 사실 근거로 사용하지 않았다.

| 순서 | 시간 표지 | 당시 목표 | 변경 단위 | 처음 가설 | 실제 조치 | CLI | 검증 신호 | 핵심 코드 앵커 | 새로 배운 것 | 다음 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Phase 1 | 같은 Books CRUD를 Express 위에 먼저 세운다 | `express/src/app.ts`, `express/src/controllers/book.controller.ts`, `express/src/routes/book.router.ts`, `express/src/services/book.service.ts` | CRUD 예제라서 framework 차이는 route 문법 정도일 거라고 보기 쉬웠다 | `createApp()`에서 `BookService -> BookController -> Router`를 수동으로 조립하고 `asyncHandler()`로 비동기 오류 전달을 따로 감쌌다 | `COREPACK_ENABLE_AUTO_PIN=0 pnpm run build`, `COREPACK_ENABLE_AUTO_PIN=0 pnpm run test` (`express/`) | `Test Files 2 passed`, `Tests 18 passed` | `app.use("/books", createBookRouter(bookController))` | Express의 핵심 차이는 기능보다 composition root가 노출된다는 점이다 | 같은 CRUD를 NestJS container 안으로 옮겨 본다 |
| 2 | Phase 2 | NestJS가 같은 문제를 어디까지 흡수하는지 확인한다 | `nestjs/src/app.module.ts`, `nestjs/src/books/books.module.ts`, `nestjs/src/books/books.controller.ts`, `nestjs/src/books/books.service.ts` | NestJS로 오면 service까지 크게 달라질 것 같았다 | service는 in-memory CRUD를 유지하고, controller 등록과 의존성 주입과 404 전파만 decorator와 DI container로 옮겼다 | `COREPACK_ENABLE_AUTO_PIN=0 pnpm run build`, `COREPACK_ENABLE_AUTO_PIN=0 pnpm run test`, `COREPACK_ENABLE_AUTO_PIN=0 pnpm run test:e2e` (`nestjs/`) | unit 8개, e2e 8개 통과 | `@Controller("books")`, `throw new NotFoundException(...)` | NestJS는 CRUD 자체보다 route 선언과 예외 전파 보일러플레이트를 프레임워크 안으로 접어 넣는다 | 두 lane의 공통 계약과 빈칸을 비교한다 |
| 3 | Phase 3 | 두 구현이 정말 같은 계약을 통과하는지 고정한다 | `express/test/unit/book.service.test.ts`, `express/test/e2e/books.e2e.test.ts`, `nestjs/test/unit/books.service.test.ts`, `nestjs/test/e2e/books.e2e.test.ts` | 테스트가 통과하니 runtime guard도 어느 정도 들어갔을 거라고 오해하기 쉽다 | CRUD happy path와 404는 테스트가 고정하지만 payload validation은 따로 검증하지 않는다는 점을 코드와 테스트 모두에서 확인했다 | 위 명령 재실행 | Express 18개, Nest unit 8개, Nest e2e 8개 통과 | 테스트가 모두 list/create/get/update/delete와 404에 집중 | 이 lab의 공통 ground truth는 "둘 다 CRUD는 안정적이지만 validation은 아직 없다"이다 | invalid payload를 직접 넣어 확인한다 |
| 4 | Phase 4 | DTO가 실제 runtime validation으로 이어지는지 확인한다 | `express/src/types/book.ts`, `nestjs/src/books/dto/create-book.dto.ts`, `nestjs/src/main.ts` | 이름이 DTO이니 빈 제목 정도는 막을 거라 예상할 수 있다 | Express와 NestJS 빌드 결과물에 직접 POST를 보내 빈 문자열 제목도 `201`으로 받아들이는지 확인했다 | `node -e "const request=require('supertest'); const {createApp}=require('./dist/app.js'); ..."` (`express/`), `node -e "require('reflect-metadata'); ... request(app.getHttpServer()).post('/books').send({title:''}) ..."` (`nestjs/`) | 두 lane 모두 `201`과 생성된 body 반환 | Express DTO는 타입 별칭, Nest DTO는 plain class이고 `ValidationPipe` 부재 | validation은 framework 선택의 결과가 아니라 pipeline을 명시적으로 연결해야 생기는 규약이다 | `04-request-pipeline`에서 validation, error handling, response envelope로 넘어간다 |

## 근거 파일

- `core/03-rest-api-foundations/problem/README.md`
- `core/03-rest-api-foundations/README.md`
- `core/03-rest-api-foundations/express/src/app.ts`
- `core/03-rest-api-foundations/express/src/controllers/book.controller.ts`
- `core/03-rest-api-foundations/express/src/routes/book.router.ts`
- `core/03-rest-api-foundations/express/src/services/book.service.ts`
- `core/03-rest-api-foundations/express/test/unit/book.service.test.ts`
- `core/03-rest-api-foundations/express/test/e2e/books.e2e.test.ts`
- `core/03-rest-api-foundations/nestjs/src/app.module.ts`
- `core/03-rest-api-foundations/nestjs/src/books/books.controller.ts`
- `core/03-rest-api-foundations/nestjs/src/books/books.service.ts`
- `core/03-rest-api-foundations/nestjs/src/books/dto/create-book.dto.ts`
- `core/03-rest-api-foundations/nestjs/src/main.ts`
- `core/03-rest-api-foundations/nestjs/test/unit/books.service.test.ts`
- `core/03-rest-api-foundations/nestjs/test/e2e/books.e2e.test.ts`
