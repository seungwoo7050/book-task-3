# 09-platform-capstone-nestjs 문제지

## 왜 중요한가

NestJS capstone 레인

## 목표

시작 위치의 구현을 완성해 auth, books, events, persistence, 운영성 규약이 한 서비스 안에서 함께 동작할 것, native SQLite 복구 절차를 포함해 재현 가능한 검증 명령을 남길 것, 단계별 학습 산출물이 capstone 안에서 어떻게 연결되는지 설명할 것을 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../study/Node-Backend-Architecture/applied/09-platform-capstone/nestjs/src/app.module.ts`
- `../study/Node-Backend-Architecture/applied/09-platform-capstone/nestjs/src/auth/auth.controller.ts`
- `../study/Node-Backend-Architecture/applied/09-platform-capstone/nestjs/src/auth/auth.module.ts`
- `../study/Node-Backend-Architecture/applied/09-platform-capstone/nestjs/src/auth/auth.service.ts`
- `../study/Node-Backend-Architecture/applied/09-platform-capstone/nestjs/test/e2e/capstone.e2e.test.ts`
- `../study/Node-Backend-Architecture/applied/09-platform-capstone/nestjs/test/unit/auth.service.test.ts`
- `../study/Node-Backend-Architecture/applied/09-platform-capstone/problem/script/nestjs/Makefile`
- `../study/Node-Backend-Architecture/applied/09-platform-capstone/nestjs/pnpm-lock.yaml`

## starter code / 입력 계약

- `../study/Node-Backend-Architecture/applied/09-platform-capstone/nestjs/src/app.module.ts`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- auth, books, events, persistence, 운영성 규약이 한 서비스 안에서 함께 동작할 것
- native SQLite 복구 절차를 포함해 재현 가능한 검증 명령을 남길 것
- 단계별 학습 산출물이 capstone 안에서 어떻게 연결되는지 설명할 것

## 제외 범위

- Postgres, Redis, Docker Compose를 포함한 제출용 패키징
- queue/worker 분리와 별도 비동기 프로세스 운영
- 실제 클라우드 배포와 운영 자동화

## 성공 체크리스트

- 핵심 흐름은 `AppModule`와 `AuthController`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `Platform Capstone E2E`와 `POST /auth/register — should register a new user`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../study/Node-Backend-Architecture/applied/09-platform-capstone/problem/script/nestjs/Makefile` 등 fixture/trace 기준으로 결과를 대조했다.
- `cd /Users/woopinbell/work/book-task-3/backend-node/study/Node-Backend-Architecture/applied/09-platform-capstone/nestjs && npm run test -- --run`가 통과한다.

## 검증 방법

```bash
cd /Users/woopinbell/work/book-task-3/backend-node/study/Node-Backend-Architecture/applied/09-platform-capstone/nestjs && npm run test -- --run
```

```bash
cd /Users/woopinbell/work/book-task-3/backend-node/study/Node-Backend-Architecture/applied/09-platform-capstone/nestjs && npm run test:e2e
```

- Node 계열 lab는 의존성 설치(`npm install` 등)가 끝난 뒤 검증 명령을 실행한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`09-platform-capstone-nestjs_answer.md`](09-platform-capstone-nestjs_answer.md)에서 확인한다.
