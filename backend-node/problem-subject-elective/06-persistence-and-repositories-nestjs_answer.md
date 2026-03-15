# 06-persistence-and-repositories-nestjs 답안지

이 문서는 문제지를 다시 넘기지 않고도 해답을 재구성할 수 있도록, 실제 구현 파일과 테스트만 기준으로 정리한 답안지다.

## 한 줄 해답

시작 위치의 구현을 완성해 두 레인 모두 CRUD 계약을 유지한 채 저장 계층을 바꿀 것, better-sqlite3 설치와 복구 절차를 문서화할 것, unit/e2e 테스트로 저장 전략 교체 이후 동작을 검증할 것을 한 흐름으로 설명하고 검증한다. 핵심은 `AppModule`와 `BooksController`, `BooksModule` 흐름을 구현하고 테스트를 통과시키는 것이다.

## 문제를 푸는 핵심 전략

- 두 레인 모두 CRUD 계약을 유지한 채 저장 계층을 바꿀 것
- better-sqlite3 설치와 복구 절차를 문서화할 것
- unit/e2e 테스트로 저장 전략 교체 이후 동작을 검증할 것
- 첫 진입점은 `../study/Node-Backend-Architecture/core/06-persistence-and-repositories/nestjs/src/app.module.ts`이고, 여기서 `AppModule`와 `BooksController` 흐름을 먼저 붙잡은 뒤 나머지 파일로 확장한다.

## 코드 워크스루

- `../study/Node-Backend-Architecture/core/06-persistence-and-repositories/nestjs/src/app.module.ts`: `AppModule`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Node-Backend-Architecture/core/06-persistence-and-repositories/nestjs/src/books/books.controller.ts`: `BooksController`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Node-Backend-Architecture/core/06-persistence-and-repositories/nestjs/src/books/books.module.ts`: `BooksModule`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Node-Backend-Architecture/core/06-persistence-and-repositories/nestjs/src/books/books.service.ts`: `BooksService`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Node-Backend-Architecture/core/06-persistence-and-repositories/nestjs/src/books/dto/create-book.dto.ts`: `CreateBookDto`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Node-Backend-Architecture/core/06-persistence-and-repositories/nestjs/test/e2e/database.e2e.test.ts`: `Database E2E (NestJS)`, `should create a book and persist it`, `should list all books`가 통과 조건과 회귀 포인트를 잠근다.
- `../study/Node-Backend-Architecture/core/06-persistence-and-repositories/nestjs/test/unit/books.service.test.ts`: `BooksService (with TypeORM)`, `should create and find a book`, `should find all books`가 통과 조건과 회귀 포인트를 잠근다.
- `../study/Node-Backend-Architecture/core/06-persistence-and-repositories/problem/script/express/Makefile`: 실행 명령과 검증 경로를 고정하는 설정 파일이다.

## 정답을 재구성하는 절차

1. `../study/Node-Backend-Architecture/core/06-persistence-and-repositories/nestjs/src/app.module.ts`를 먼저 열어 입력과 상태 전이의 기준점을 잡는다.
2. `Database E2E (NestJS)` 등이 요구하는 순서대로 핵심 상태 전이와 예외 흐름을 채운다.
3. `cd /Users/woopinbell/work/book-task-3/backend-node/study/Node-Backend-Architecture/core/06-persistence-and-repositories/nestjs && npm run test -- --run`를 실행해 결과를 잠그고, 필요하면 남은 검증 명령까지 이어서 돌린다.

## 검증과 실패 포인트

```bash
cd /Users/woopinbell/work/book-task-3/backend-node/study/Node-Backend-Architecture/core/06-persistence-and-repositories/nestjs && npm run test -- --run
```

```bash
cd /Users/woopinbell/work/book-task-3/backend-node/study/Node-Backend-Architecture/core/06-persistence-and-repositories/nestjs && npm run test:e2e
```

- 상위 카탈로그나 보조 문서만 보고 구현을 추측하지 않고, 지금 열어 둔 source/test를 정답 근거로 고정한다.
- `Database E2E (NestJS)`와 `should create a book and persist it`가 잠근 상태 전이와 입력 계약을 빼먹지 않는다.
- 완성 직전에만 한 번 돌리지 말고, 상태 전이를 건드릴 때마다 `cd /Users/woopinbell/work/book-task-3/backend-node/study/Node-Backend-Architecture/core/06-persistence-and-repositories/nestjs && npm run test -- --run`로 회귀를 조기에 잡는다.

## 소스 근거

- `../study/Node-Backend-Architecture/core/06-persistence-and-repositories/nestjs/src/app.module.ts`
- `../study/Node-Backend-Architecture/core/06-persistence-and-repositories/nestjs/src/books/books.controller.ts`
- `../study/Node-Backend-Architecture/core/06-persistence-and-repositories/nestjs/src/books/books.module.ts`
- `../study/Node-Backend-Architecture/core/06-persistence-and-repositories/nestjs/src/books/books.service.ts`
- `../study/Node-Backend-Architecture/core/06-persistence-and-repositories/nestjs/src/books/dto/create-book.dto.ts`
- `../study/Node-Backend-Architecture/core/06-persistence-and-repositories/nestjs/test/e2e/database.e2e.test.ts`
- `../study/Node-Backend-Architecture/core/06-persistence-and-repositories/nestjs/test/unit/books.service.test.ts`
- `../study/Node-Backend-Architecture/core/06-persistence-and-repositories/problem/script/express/Makefile`
- `../study/Node-Backend-Architecture/core/06-persistence-and-repositories/problem/script/nestjs/Makefile`
- `../study/Node-Backend-Architecture/core/06-persistence-and-repositories/nestjs/nest-cli.json`
