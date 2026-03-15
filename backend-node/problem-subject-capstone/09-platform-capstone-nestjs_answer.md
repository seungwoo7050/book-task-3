# 09-platform-capstone-nestjs 답안지

이 문서는 문제지를 다시 넘기지 않고도 해답을 재구성할 수 있도록, 실제 구현 파일과 테스트만 기준으로 정리한 답안지다.

## 한 줄 해답

시작 위치의 구현을 완성해 auth, books, events, persistence, 운영성 규약이 한 서비스 안에서 함께 동작할 것, native SQLite 복구 절차를 포함해 재현 가능한 검증 명령을 남길 것, 단계별 학습 산출물이 capstone 안에서 어떻게 연결되는지 설명할 것을 한 흐름으로 설명하고 검증한다. 핵심은 `AppModule`와 `AuthController`, `AuthModule` 흐름을 구현하고 테스트를 통과시키는 것이다.

## 문제를 푸는 핵심 전략

- auth, books, events, persistence, 운영성 규약이 한 서비스 안에서 함께 동작할 것
- native SQLite 복구 절차를 포함해 재현 가능한 검증 명령을 남길 것
- 단계별 학습 산출물이 capstone 안에서 어떻게 연결되는지 설명할 것
- 첫 진입점은 `../study/Node-Backend-Architecture/applied/09-platform-capstone/nestjs/src/app.module.ts`이고, 여기서 `AppModule`와 `AuthController` 흐름을 먼저 붙잡은 뒤 나머지 파일로 확장한다.

## 코드 워크스루

- `../study/Node-Backend-Architecture/applied/09-platform-capstone/nestjs/src/app.module.ts`: `AppModule`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Node-Backend-Architecture/applied/09-platform-capstone/nestjs/src/auth/auth.controller.ts`: `AuthController`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Node-Backend-Architecture/applied/09-platform-capstone/nestjs/src/auth/auth.module.ts`: `AuthModule`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Node-Backend-Architecture/applied/09-platform-capstone/nestjs/src/auth/auth.service.ts`: `AuthService`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Node-Backend-Architecture/applied/09-platform-capstone/nestjs/src/auth/decorators/current-user.decorator.ts`: `CurrentUser`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Node-Backend-Architecture/applied/09-platform-capstone/nestjs/test/e2e/capstone.e2e.test.ts`: `Platform Capstone E2E`, `POST /auth/register — should register a new user`, `POST /auth/register — should reject duplicate username`가 통과 조건과 회귀 포인트를 잠근다.
- `../study/Node-Backend-Architecture/applied/09-platform-capstone/nestjs/test/unit/auth.service.test.ts`: `AuthService`, `should register a new user and emit event`, `should throw ConflictException if user exists`가 통과 조건과 회귀 포인트를 잠근다.
- `../study/Node-Backend-Architecture/applied/09-platform-capstone/nestjs/test/unit/books.service.test.ts`: `mockBook`, `BooksService`, `should create a book and emit event`가 통과 조건과 회귀 포인트를 잠근다.

## 정답을 재구성하는 절차

1. `../study/Node-Backend-Architecture/applied/09-platform-capstone/nestjs/src/app.module.ts`를 먼저 열어 입력과 상태 전이의 기준점을 잡는다.
2. `Platform Capstone E2E` 등이 요구하는 순서대로 핵심 상태 전이와 예외 흐름을 채운다.
3. `cd /Users/woopinbell/work/book-task-3/backend-node/study/Node-Backend-Architecture/applied/09-platform-capstone/nestjs && npm run test -- --run`를 실행해 결과를 잠그고, 필요하면 남은 검증 명령까지 이어서 돌린다.

## 검증과 실패 포인트

```bash
cd /Users/woopinbell/work/book-task-3/backend-node/study/Node-Backend-Architecture/applied/09-platform-capstone/nestjs && npm run test -- --run
```

```bash
cd /Users/woopinbell/work/book-task-3/backend-node/study/Node-Backend-Architecture/applied/09-platform-capstone/nestjs && npm run test:e2e
```

- 상위 카탈로그나 보조 문서만 보고 구현을 추측하지 않고, 지금 열어 둔 source/test를 정답 근거로 고정한다.
- `Platform Capstone E2E`와 `POST /auth/register — should register a new user`가 잠근 상태 전이와 입력 계약을 빼먹지 않는다.
- 완성 직전에만 한 번 돌리지 말고, 상태 전이를 건드릴 때마다 `cd /Users/woopinbell/work/book-task-3/backend-node/study/Node-Backend-Architecture/applied/09-platform-capstone/nestjs && npm run test -- --run`로 회귀를 조기에 잡는다.

## 소스 근거

- `../study/Node-Backend-Architecture/applied/09-platform-capstone/nestjs/src/app.module.ts`
- `../study/Node-Backend-Architecture/applied/09-platform-capstone/nestjs/src/auth/auth.controller.ts`
- `../study/Node-Backend-Architecture/applied/09-platform-capstone/nestjs/src/auth/auth.module.ts`
- `../study/Node-Backend-Architecture/applied/09-platform-capstone/nestjs/src/auth/auth.service.ts`
- `../study/Node-Backend-Architecture/applied/09-platform-capstone/nestjs/src/auth/decorators/current-user.decorator.ts`
- `../study/Node-Backend-Architecture/applied/09-platform-capstone/nestjs/test/e2e/capstone.e2e.test.ts`
- `../study/Node-Backend-Architecture/applied/09-platform-capstone/nestjs/test/unit/auth.service.test.ts`
- `../study/Node-Backend-Architecture/applied/09-platform-capstone/nestjs/test/unit/books.service.test.ts`
- `../study/Node-Backend-Architecture/applied/09-platform-capstone/problem/script/nestjs/Makefile`
- `../study/Node-Backend-Architecture/applied/09-platform-capstone/nestjs/pnpm-lock.yaml`
