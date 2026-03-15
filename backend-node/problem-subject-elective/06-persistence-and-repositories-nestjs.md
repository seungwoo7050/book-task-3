# 06-persistence-and-repositories-nestjs 문제지

## 왜 중요한가

Express 레인 NestJS 레인

## 목표

시작 위치의 구현을 완성해 두 레인 모두 CRUD 계약을 유지한 채 저장 계층을 바꿀 것, better-sqlite3 설치와 복구 절차를 문서화할 것, unit/e2e 테스트로 저장 전략 교체 이후 동작을 검증할 것을 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../study/Node-Backend-Architecture/core/06-persistence-and-repositories/nestjs/src/app.module.ts`
- `../study/Node-Backend-Architecture/core/06-persistence-and-repositories/nestjs/src/books/books.controller.ts`
- `../study/Node-Backend-Architecture/core/06-persistence-and-repositories/nestjs/src/books/books.module.ts`
- `../study/Node-Backend-Architecture/core/06-persistence-and-repositories/nestjs/src/books/books.service.ts`
- `../study/Node-Backend-Architecture/core/06-persistence-and-repositories/nestjs/test/e2e/database.e2e.test.ts`
- `../study/Node-Backend-Architecture/core/06-persistence-and-repositories/nestjs/test/unit/books.service.test.ts`
- `../study/Node-Backend-Architecture/core/06-persistence-and-repositories/problem/script/express/Makefile`
- `../study/Node-Backend-Architecture/core/06-persistence-and-repositories/problem/script/nestjs/Makefile`

## starter code / 입력 계약

- `../study/Node-Backend-Architecture/core/06-persistence-and-repositories/nestjs/src/app.module.ts`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- 두 레인 모두 CRUD 계약을 유지한 채 저장 계층을 바꿀 것
- better-sqlite3 설치와 복구 절차를 문서화할 것
- unit/e2e 테스트로 저장 전략 교체 이후 동작을 검증할 것

## 제외 범위

- `../study/Node-Backend-Architecture/core/06-persistence-and-repositories/problem/script/express/Makefile` 등 fixture나 trace를 읽지 않고 동작을 추측해서 구현하지 않는다.
- 같은 주제의 다른 runtime 구현을 섞어 읽지 않는다.

## 성공 체크리스트

- 핵심 흐름은 `AppModule`와 `BooksController`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `Database E2E (NestJS)`와 `should create a book and persist it`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../study/Node-Backend-Architecture/core/06-persistence-and-repositories/problem/script/express/Makefile` 등 fixture/trace 기준으로 결과를 대조했다.
- `cd /Users/woopinbell/work/book-task-3/backend-node/study/Node-Backend-Architecture/core/06-persistence-and-repositories/nestjs && npm run test -- --run`가 통과한다.

## 검증 방법

```bash
cd /Users/woopinbell/work/book-task-3/backend-node/study/Node-Backend-Architecture/core/06-persistence-and-repositories/nestjs && npm run test -- --run
```

```bash
cd /Users/woopinbell/work/book-task-3/backend-node/study/Node-Backend-Architecture/core/06-persistence-and-repositories/nestjs && npm run test:e2e
```

- Node 계열 lab는 의존성 설치(`npm install` 등)가 끝난 뒤 검증 명령을 실행한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`06-persistence-and-repositories-nestjs_answer.md`](06-persistence-and-repositories-nestjs_answer.md)에서 확인한다.
