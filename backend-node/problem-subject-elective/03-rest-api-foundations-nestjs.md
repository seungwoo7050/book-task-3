# 03-rest-api-foundations-nestjs 문제지

## 왜 중요한가

Express 레인 NestJS 레인

## 목표

시작 위치의 구현을 완성해 두 레인 모두 GET/POST/PUT/DELETE /books 계약을 구현할 것, service가 HTTP 세부사항에 의존하지 않게 분리할 것, 두 레인의 테스트와 실행 명령이 README에 명시될 것을 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../study/Node-Backend-Architecture/core/03-rest-api-foundations/problem/code/express/src/controllers/book.controller.ts`
- `../study/Node-Backend-Architecture/core/03-rest-api-foundations/problem/code/express/src/main.ts`
- `../study/Node-Backend-Architecture/core/03-rest-api-foundations/nestjs/src/app.module.ts`
- `../study/Node-Backend-Architecture/core/03-rest-api-foundations/nestjs/src/books/books.controller.ts`
- `../study/Node-Backend-Architecture/core/03-rest-api-foundations/nestjs/src/books/books.module.ts`
- `../study/Node-Backend-Architecture/core/03-rest-api-foundations/nestjs/src/books/books.service.ts`
- `../study/Node-Backend-Architecture/core/03-rest-api-foundations/nestjs/test/e2e/books.e2e.test.ts`
- `../study/Node-Backend-Architecture/core/03-rest-api-foundations/nestjs/test/unit/books.service.test.ts`

## starter code / 입력 계약

- ../study/Node-Backend-Architecture/core/03-rest-api-foundations/problem/code/express/src/controllers/book.controller.ts에서 starter 코드와 입력 경계를 잡는다.
- ../study/Node-Backend-Architecture/core/03-rest-api-foundations/problem/code/express/src/main.ts에서 starter 코드와 입력 경계를 잡는다.
- ../study/Node-Backend-Architecture/core/03-rest-api-foundations/problem/code/express/src/routes/book.router.ts에서 starter 코드와 입력 경계를 잡는다.

## 핵심 요구사항

- 두 레인 모두 GET/POST/PUT/DELETE /books 계약을 구현할 것
- service가 HTTP 세부사항에 의존하지 않게 분리할 것
- 두 레인의 테스트와 실행 명령이 README에 명시될 것

## 제외 범위

- `../study/Node-Backend-Architecture/core/03-rest-api-foundations/problem/code/express/src/controllers/book.controller.ts` starter skeleton을 정답 구현으로 착각하지 않는다.
- `../study/Node-Backend-Architecture/core/03-rest-api-foundations/problem/script/express/Makefile` 등 fixture나 trace를 읽지 않고 동작을 추측해서 구현하지 않는다.
- 같은 주제의 다른 runtime 구현을 섞어 읽지 않는다.

## 성공 체크리스트

- `../study/Node-Backend-Architecture/core/03-rest-api-foundations/problem/code/express/src/controllers/book.controller.ts`의 빈 확장 지점을 실제 구현으로 채웠다.
- 핵심 흐름은 `AppModule`와 `BooksController`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `Books API (E2E)`와 `GET /books`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../study/Node-Backend-Architecture/core/03-rest-api-foundations/problem/script/express/Makefile` 등 fixture/trace 기준으로 결과를 대조했다.

## 검증 방법

```bash
cd /Users/woopinbell/work/book-task-3/backend-node/study/Node-Backend-Architecture/core/03-rest-api-foundations/nestjs && npm run test -- --run
```

```bash
cd /Users/woopinbell/work/book-task-3/backend-node/study/Node-Backend-Architecture/core/03-rest-api-foundations/nestjs && npm run test:e2e
```

- Node 계열 lab는 의존성 설치(`npm install` 등)가 끝난 뒤 검증 명령을 실행한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`03-rest-api-foundations-nestjs_answer.md`](03-rest-api-foundations-nestjs_answer.md)에서 확인한다.
