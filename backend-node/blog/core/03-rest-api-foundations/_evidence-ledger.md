# 03-rest-api-foundations evidence ledger

이 프로젝트의 path 단위 `git log`도 `2026-03-12` 한 번의 이관 커밋으로 묶여 있다. chronology는 `problem`, `express/`, `nestjs/`, 테스트, 실제 재검증 CLI를 따라 다시 복원한 것이다.

| 순서 | 시간 표지 | 당시 목표 | 변경 단위 | 처음 가설 | 실제 조치 | CLI | 검증 신호 | 핵심 코드 앵커 | 새로 배운 것 | 다음 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Phase 1 | 같은 Books CRUD를 Express의 수동 DI 위에 먼저 세운다 | `express/src/services/book.service.ts`, `express/src/routes/book.router.ts` | CRUD 예제니까 service와 route를 느슨하게 섞어도 괜찮아 보였다 | `BookService`를 순수 도메인 로직으로 두고 router는 controller 연결만 맡겼다 | `COREPACK_ENABLE_AUTO_PIN=0 pnpm run build && pnpm run test` (`express/`) | `Test Files 2 passed`, `Tests 18 passed` | `router.get("/", asyncHandler(controller.findAll))` | Express에서는 의존성을 누가 만들고 꽂는지가 코드 표면에 그대로 남는다 | 같은 문제를 NestJS DI로 옮겨 본다 |
| 2 | Phase 2 | 같은 CRUD를 NestJS container와 decorator로 다시 세운다 | `nestjs/src/books/books.service.ts`, `nestjs/src/books/books.controller.ts` | 프레임워크를 바꾸면 service 모양도 많이 달라질 것 같았다 | service 책임은 유지하고, route 정의와 예외 전파만 NestJS 방식으로 바꿨다 | `COREPACK_ENABLE_AUTO_PIN=0 pnpm run build && pnpm run test && pnpm run test:e2e` (`nestjs/`) | `Tests 8 passed`, `test:e2e 8 passed` | `@Controller("books")`, `throw new NotFoundException(...)` | NestJS의 차이는 CRUD 자체보다 HTTP 경계와 예외 처리 보일러플레이트를 프레임워크가 흡수한다는 데 있다 | 다음엔 CRUD보다 앞에 오는 공통 pipeline을 분리한다 |
| 3 | Phase 3 | 두 레인이 정말 같은 CRUD 계약을 통과하는지 묶어 본다 | `express/test/unit/book.service.test.ts`, `nestjs/test/e2e/books.e2e.test.ts` | 코드 모양만 비슷하면 비교도 충분하다고 보기 쉽다 | Express는 service unit, NestJS는 e2e까지 붙여 각 프레임워크에서 같은 문제를 어떻게 감싸는지 고정했다 | 위 명령 재실행 | Express 18개, Nest unit 8개 + e2e 8개 통과 | service test와 e2e test가 역할을 나눠 증명하는 구조 | 비교 학습은 설명문보다 같은 문제를 같은 계약으로 통과시키는 신호에서 더 선명해진다 | `04-request-pipeline`에서 공통 규약을 먼저 고정한다 |

## 근거 파일

- `core/03-rest-api-foundations/README.md`
- `core/03-rest-api-foundations/problem/README.md`
- `core/03-rest-api-foundations/express/src/services/book.service.ts`
- `core/03-rest-api-foundations/express/src/routes/book.router.ts`
- `core/03-rest-api-foundations/nestjs/src/books/books.service.ts`
- `core/03-rest-api-foundations/nestjs/src/books/books.controller.ts`
- `core/03-rest-api-foundations/express/test/unit/book.service.test.ts`
- `core/03-rest-api-foundations/nestjs/test/e2e/books.e2e.test.ts`
