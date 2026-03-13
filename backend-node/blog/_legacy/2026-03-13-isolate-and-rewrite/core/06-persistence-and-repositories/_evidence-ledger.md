# 06-persistence-and-repositories evidence ledger

근거는 [`README.md`](../../../study/Node-Backend-Architecture/core/06-persistence-and-repositories/README.md), [`express/src/database/init.ts`](../../../study/Node-Backend-Architecture/core/06-persistence-and-repositories/express/src/database/init.ts), [`express/src/repositories/book.repository.ts`](../../../study/Node-Backend-Architecture/core/06-persistence-and-repositories/express/src/repositories/book.repository.ts), [`express/test/e2e/database.e2e.test.ts`](../../../study/Node-Backend-Architecture/core/06-persistence-and-repositories/express/test/e2e/database.e2e.test.ts), [`nestjs/src/books/books.service.ts`](../../../study/Node-Backend-Architecture/core/06-persistence-and-repositories/nestjs/src/books/books.service.ts), [`nestjs/test/e2e/database.e2e.test.ts`](../../../study/Node-Backend-Architecture/core/06-persistence-and-repositories/nestjs/test/e2e/database.e2e.test.ts), 실제 검증 출력이다.

## Phase 1

- 순서: 1
- 시간 표지: Phase 1
- 당시 목표: Express 레인에서 메모리 저장소를 raw SQL repository로 교체한다.
- 변경 단위: `express/src/database/init.ts`, `express/src/repositories/book.repository.ts`
- 처음 가설: API 계층을 거의 건드리지 않고 저장 전략만 바꾸려면 repository boundary가 먼저 필요하다.
- 실제 조치: `initDatabase()`가 SQLite schema를 만들고, `BookRepository`가 `SELECT/INSERT/UPDATE/DELETE`를 직접 수행하게 했다.
- CLI: `COREPACK_ENABLE_AUTO_PIN=0 pnpm run build`, `COREPACK_ENABLE_AUTO_PIN=0 pnpm run test`, `COREPACK_ENABLE_AUTO_PIN=0 pnpm run test:e2e`
- 검증 신호: unit `Tests 7 passed (7)`, e2e `Tests 6 passed (6)`
- 핵심 코드 앵커: `initDatabase()`, `BookRepository.create()`
- 새로 배운 것: persistence 교체의 핵심은 DB를 쓰는 법보다 "API 계층이 저장 방식 변경을 얼마나 덜 느끼는가"였다.
- 다음: NestJS 레인에서 같은 교체를 ORM과 repository injection으로 다시 푼다.

## Phase 2

- 순서: 2
- 시간 표지: Phase 2
- 당시 목표: NestJS에서 TypeORM으로 같은 Books contract를 유지한다.
- 변경 단위: `nestjs/src/books/books.service.ts`, `nestjs/test/e2e/database.e2e.test.ts`
- 처음 가설: Express raw SQL과 달리 NestJS는 repository injection과 entity 선언이 저장 계층의 중심이 될 것이다.
- 실제 조치: `@InjectRepository(Book)`로 `Repository<Book>`를 주입하고 CRUD를 async ORM 호출로 바꿨다.
- CLI: `COREPACK_ENABLE_AUTO_PIN=0 pnpm run build`, `COREPACK_ENABLE_AUTO_PIN=0 pnpm run test`, `COREPACK_ENABLE_AUTO_PIN=0 pnpm run test:e2e`
- 검증 신호: unit `Tests 5 passed (5)`, e2e `Tests 6 passed (6)`
- 핵심 코드 앵커: `BooksService.findAll()`, `BooksService.create()`
- 새로 배운 것: 같은 persistence 문제라도 Express는 SQL과 schema가, NestJS는 entity와 repository injection이 중심축이었다.
- 다음: DB를 직접 들여다보는 검증과 API 재검증을 함께 본다.

## Phase 3

- 순서: 3
- 시간 표지: Phase 3
- 당시 목표: DB 교체 뒤에도 API 계약과 실패 경계가 유지되는지 확인한다.
- 변경 단위: `express/test/e2e/database.e2e.test.ts`, `nestjs/test/e2e/database.e2e.test.ts`
- 처음 가설: persistence 프로젝트는 API 응답만 보면 부족하고, 실제 DB row까지 확인해야 교체가 끝난다.
- 실제 조치: Express e2e는 `SELECT * FROM books WHERE id = ?`로 row를 직접 확인하고, Nest e2e는 생성 후 재조회와 삭제 후 404를 검증했다.
- CLI: `pnpm run test:e2e`
- 검증 신호: Express 로그에 `POST ... 201`, `DELETE ... 204`, `GET ... 404`, 두 레인 모두 6개 e2e 통과
- 핵심 코드 앵커: `database.e2e.test.ts`
- 새로 배운 것: 저장 계층 교체는 "DB를 쓴다"보다 "API contract는 그대로인데 내부 상태만 영속화된다"는 걸 보여 주는 일이다.
- 다음: `07-domain-events`에서 저장 이후 side effect를 서비스 바깥으로 밀어낸다.
