# 03-rest-api-foundations-nestjs 답안지

이 문서는 문제지를 다시 넘기지 않고도 해답을 재구성할 수 있도록, 실제 구현 파일과 테스트만 기준으로 정리한 답안지다.

## 한 줄 해답

시작 위치의 구현을 완성해 두 레인 모두 GET/POST/PUT/DELETE /books 계약을 구현할 것, service가 HTTP 세부사항에 의존하지 않게 분리할 것, 두 레인의 테스트와 실행 명령이 README에 명시될 것을 한 흐름으로 설명하고 검증한다. 핵심은 `AppModule`와 `BooksController`, `BooksModule` 흐름을 구현하고 테스트를 통과시키는 것이다.

## 문제를 푸는 핵심 전략

- 두 레인 모두 GET/POST/PUT/DELETE /books 계약을 구현할 것
- service가 HTTP 세부사항에 의존하지 않게 분리할 것
- 두 레인의 테스트와 실행 명령이 README에 명시될 것
- 첫 진입점은 `../study/Node-Backend-Architecture/core/03-rest-api-foundations/nestjs/src/app.module.ts`이고, 여기서 `AppModule`와 `BooksController` 흐름을 먼저 붙잡은 뒤 나머지 파일로 확장한다.

## 코드 워크스루

- `../study/Node-Backend-Architecture/core/03-rest-api-foundations/nestjs/src/app.module.ts`: `AppModule`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Node-Backend-Architecture/core/03-rest-api-foundations/nestjs/src/books/books.controller.ts`: `BooksController`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Node-Backend-Architecture/core/03-rest-api-foundations/nestjs/src/books/books.module.ts`: `BooksModule`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Node-Backend-Architecture/core/03-rest-api-foundations/nestjs/src/books/books.service.ts`: `BooksService`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Node-Backend-Architecture/core/03-rest-api-foundations/nestjs/src/books/dto/create-book.dto.ts`: `CreateBookDto`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Node-Backend-Architecture/core/03-rest-api-foundations/problem/code/express/src/controllers/book.controller.ts`: `BookController`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Node-Backend-Architecture/core/03-rest-api-foundations/problem/code/express/src/main.ts`: `app`, `PORT`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Node-Backend-Architecture/core/03-rest-api-foundations/nestjs/test/e2e/books.e2e.test.ts`: `Books API (E2E)`, `GET /books`, `should return an empty array initially`가 통과 조건과 회귀 포인트를 잠근다.

## 정답을 재구성하는 절차

1. `../study/Node-Backend-Architecture/core/03-rest-api-foundations/problem/code/express/src/controllers/book.controller.ts`와 `../study/Node-Backend-Architecture/core/03-rest-api-foundations/nestjs/src/app.module.ts`를 나란히 열어 먼저 바뀌는 경계를 잡는다.
2. `Books API (E2E)` 등이 요구하는 순서대로 핵심 상태 전이와 예외 흐름을 채운다.
3. `cd /Users/woopinbell/work/book-task-3/backend-node/study/Node-Backend-Architecture/core/03-rest-api-foundations/nestjs && npm run test -- --run`를 실행해 결과를 잠그고, 필요하면 남은 검증 명령까지 이어서 돌린다.

## 검증과 실패 포인트

```bash
cd /Users/woopinbell/work/book-task-3/backend-node/study/Node-Backend-Architecture/core/03-rest-api-foundations/nestjs && npm run test -- --run
```

```bash
cd /Users/woopinbell/work/book-task-3/backend-node/study/Node-Backend-Architecture/core/03-rest-api-foundations/nestjs && npm run test:e2e
```

- `../study/Node-Backend-Architecture/core/03-rest-api-foundations/problem/code/express/src/controllers/book.controller.ts` starter skeleton의 빈칸을 그대로 정답으로 착각하지 않는다.
- `Books API (E2E)`와 `GET /books`가 잠근 상태 전이와 입력 계약을 빼먹지 않는다.
- 완성 직전에만 한 번 돌리지 말고, 상태 전이를 건드릴 때마다 `cd /Users/woopinbell/work/book-task-3/backend-node/study/Node-Backend-Architecture/core/03-rest-api-foundations/nestjs && npm run test -- --run`로 회귀를 조기에 잡는다.

## 소스 근거

- `../study/Node-Backend-Architecture/core/03-rest-api-foundations/nestjs/src/app.module.ts`
- `../study/Node-Backend-Architecture/core/03-rest-api-foundations/nestjs/src/books/books.controller.ts`
- `../study/Node-Backend-Architecture/core/03-rest-api-foundations/nestjs/src/books/books.module.ts`
- `../study/Node-Backend-Architecture/core/03-rest-api-foundations/nestjs/src/books/books.service.ts`
- `../study/Node-Backend-Architecture/core/03-rest-api-foundations/nestjs/src/books/dto/create-book.dto.ts`
- `../study/Node-Backend-Architecture/core/03-rest-api-foundations/problem/code/express/src/controllers/book.controller.ts`
- `../study/Node-Backend-Architecture/core/03-rest-api-foundations/problem/code/express/src/main.ts`
- `../study/Node-Backend-Architecture/core/03-rest-api-foundations/nestjs/test/e2e/books.e2e.test.ts`
- `../study/Node-Backend-Architecture/core/03-rest-api-foundations/nestjs/test/unit/books.service.test.ts`
- `../study/Node-Backend-Architecture/core/03-rest-api-foundations/problem/script/express/Makefile`
