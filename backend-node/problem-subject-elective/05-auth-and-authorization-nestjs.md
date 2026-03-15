# 05-auth-and-authorization-nestjs 문제지

## 왜 중요한가

Express 레인 NestJS 레인

## 목표

시작 위치의 구현을 완성해 로그인과 보호된 쓰기 경로를 구현할 것, 과 403을 테스트에서 구분할 것, Express와 NestJS 각각의 인증 훅 포인트를 설명할 것을 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../study/Node-Backend-Architecture/core/05-auth-and-authorization/problem/code/express/src/middleware/auth.middleware.ts`
- `../study/Node-Backend-Architecture/core/05-auth-and-authorization/problem/code/express/src/middleware/role.middleware.ts`
- `../study/Node-Backend-Architecture/core/05-auth-and-authorization/nestjs/src/app.module.ts`
- `../study/Node-Backend-Architecture/core/05-auth-and-authorization/nestjs/src/auth/auth.controller.ts`
- `../study/Node-Backend-Architecture/core/05-auth-and-authorization/nestjs/src/auth/auth.module.ts`
- `../study/Node-Backend-Architecture/core/05-auth-and-authorization/nestjs/src/auth/auth.service.ts`
- `../study/Node-Backend-Architecture/core/05-auth-and-authorization/nestjs/test/e2e/auth.e2e.test.ts`
- `../study/Node-Backend-Architecture/core/05-auth-and-authorization/problem/script/express/Makefile`

## starter code / 입력 계약

- ../study/Node-Backend-Architecture/core/05-auth-and-authorization/problem/code/express/src/middleware/auth.middleware.ts에서 starter 코드와 입력 경계를 잡는다.
- ../study/Node-Backend-Architecture/core/05-auth-and-authorization/problem/code/express/src/middleware/role.middleware.ts에서 starter 코드와 입력 경계를 잡는다.

## 핵심 요구사항

- 로그인과 보호된 쓰기 경로를 구현할 것
- 과 403을 테스트에서 구분할 것
- Express와 NestJS 각각의 인증 훅 포인트를 설명할 것

## 제외 범위

- `../study/Node-Backend-Architecture/core/05-auth-and-authorization/problem/code/express/src/middleware/auth.middleware.ts` starter skeleton을 정답 구현으로 착각하지 않는다.
- `../study/Node-Backend-Architecture/core/05-auth-and-authorization/problem/script/express/Makefile` 등 fixture나 trace를 읽지 않고 동작을 추측해서 구현하지 않는다.
- 같은 주제의 다른 runtime 구현을 섞어 읽지 않는다.

## 성공 체크리스트

- `../study/Node-Backend-Architecture/core/05-auth-and-authorization/problem/code/express/src/middleware/auth.middleware.ts`의 빈 확장 지점을 실제 구현으로 채웠다.
- 핵심 흐름은 `AppModule`와 `AuthController`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `Auth & Books (E2E)`와 `should register, login, and access protected route`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../study/Node-Backend-Architecture/core/05-auth-and-authorization/problem/script/express/Makefile` 등 fixture/trace 기준으로 결과를 대조했다.

## 검증 방법

```bash
cd /Users/woopinbell/work/book-task-3/backend-node/study/Node-Backend-Architecture/core/05-auth-and-authorization/nestjs && npm run test -- --run
```

- Node 계열 lab는 의존성 설치(`npm install` 등)가 끝난 뒤 검증 명령을 실행한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`05-auth-and-authorization-nestjs_answer.md`](05-auth-and-authorization-nestjs_answer.md)에서 확인한다.
