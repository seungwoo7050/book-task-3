# 07-domain-events-nestjs 문제지

## 왜 중요한가

Express 레인 NestJS 레인

## 목표

시작 위치의 구현을 완성해 도메인 이벤트와 리스너를 명시적으로 분리할 것, 성공/실패 경로의 이벤트 발행 여부를 테스트할 것, native SQLite 의존성을 포함한 재현 절차를 문서화할 것을 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../study/Node-Backend-Architecture/core/07-domain-events/nestjs/src/app.module.ts`
- `../study/Node-Backend-Architecture/core/07-domain-events/nestjs/src/books/books.controller.ts`
- `../study/Node-Backend-Architecture/core/07-domain-events/nestjs/src/books/books.module.ts`
- `../study/Node-Backend-Architecture/core/07-domain-events/nestjs/src/books/books.service.ts`
- `../study/Node-Backend-Architecture/core/07-domain-events/nestjs/test/e2e/events.e2e.test.ts`
- `../study/Node-Backend-Architecture/core/07-domain-events/nestjs/test/unit/book-event.listener.test.ts`
- `../study/Node-Backend-Architecture/core/07-domain-events/problem/script/express/Makefile`
- `../study/Node-Backend-Architecture/core/07-domain-events/problem/script/nestjs/Makefile`

## starter code / 입력 계약

- `../study/Node-Backend-Architecture/core/07-domain-events/nestjs/src/app.module.ts`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- 도메인 이벤트와 리스너를 명시적으로 분리할 것
- 성공/실패 경로의 이벤트 발행 여부를 테스트할 것
- native SQLite 의존성을 포함한 재현 절차를 문서화할 것

## 제외 범위

- `../study/Node-Backend-Architecture/core/07-domain-events/problem/script/express/Makefile` 등 fixture나 trace를 읽지 않고 동작을 추측해서 구현하지 않는다.
- 같은 주제의 다른 runtime 구현을 섞어 읽지 않는다.

## 성공 체크리스트

- 핵심 흐름은 `AppModule`와 `BooksController`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `Events E2E`와 `should emit book.created event on POST /books`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../study/Node-Backend-Architecture/core/07-domain-events/problem/script/express/Makefile` 등 fixture/trace 기준으로 결과를 대조했다.
- `cd /Users/woopinbell/work/book-task-3/backend-node/study/Node-Backend-Architecture/core/07-domain-events/nestjs && npm run test -- --run`가 통과한다.

## 검증 방법

```bash
cd /Users/woopinbell/work/book-task-3/backend-node/study/Node-Backend-Architecture/core/07-domain-events/nestjs && npm run test -- --run
```

```bash
cd /Users/woopinbell/work/book-task-3/backend-node/study/Node-Backend-Architecture/core/07-domain-events/nestjs && npm run test:e2e
```

- Node 계열 lab는 의존성 설치(`npm install` 등)가 끝난 뒤 검증 명령을 실행한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`07-domain-events-nestjs_answer.md`](07-domain-events-nestjs_answer.md)에서 확인한다.
