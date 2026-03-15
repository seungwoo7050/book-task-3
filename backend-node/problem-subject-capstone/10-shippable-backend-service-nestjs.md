# 10-shippable-backend-service-nestjs 문제지

## 왜 중요한가

NestJS 포트폴리오 레인

## 목표

시작 위치의 구현을 완성해 Postgres migration과 Redis 의존성을 포함한 로컬 실행 흐름을 제공할 것, Swagger, health endpoint, auth/books API를 한 서비스 표면으로 설명할 것, 학습용 capstone과 제출용 서비스의 차이를 문서화할 것을 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../study/Node-Backend-Architecture/applied/10-shippable-backend-service/nestjs/src/app.bootstrap.ts`
- `../study/Node-Backend-Architecture/applied/10-shippable-backend-service/nestjs/src/app.module.ts`
- `../study/Node-Backend-Architecture/applied/10-shippable-backend-service/nestjs/src/auth/auth-rate-limit.service.ts`
- `../study/Node-Backend-Architecture/applied/10-shippable-backend-service/nestjs/src/auth/auth.controller.ts`
- `../study/Node-Backend-Architecture/applied/10-shippable-backend-service/nestjs/test/e2e/capstone.e2e.test.ts`
- `../study/Node-Backend-Architecture/applied/10-shippable-backend-service/nestjs/test/unit/auth.service.test.ts`
- `../study/Node-Backend-Architecture/applied/10-shippable-backend-service/problem/script/nestjs/Makefile`
- `../study/Node-Backend-Architecture/applied/10-shippable-backend-service/nestjs/ci/github-actions.yml`

## starter code / 입력 계약

- `../study/Node-Backend-Architecture/applied/10-shippable-backend-service/nestjs/src/app.bootstrap.ts`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- Postgres migration과 Redis 의존성을 포함한 로컬 실행 흐름을 제공할 것
- Swagger, health endpoint, auth/books API를 한 서비스 표면으로 설명할 것
- 학습용 capstone과 제출용 서비스의 차이를 문서화할 것

## 제외 범위

- 별도 queue/worker 프로세스와 이벤트 브로커 운영
- MSA 분리와 서비스 간 네트워크 통신
- 실제 클라우드 배포와 외부 SaaS 연동

## 성공 체크리스트

- 핵심 흐름은 `configureApp`와 `AppModule`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `Shippable Backend Service E2E`와 `GET /health/live should return 200`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../study/Node-Backend-Architecture/applied/10-shippable-backend-service/problem/script/nestjs/Makefile` 등 fixture/trace 기준으로 결과를 대조했다.
- `cd /Users/woopinbell/work/book-task-3/backend-node/study/Node-Backend-Architecture/applied/10-shippable-backend-service/nestjs && npm run test -- --run`가 통과한다.

## 검증 방법

```bash
cd /Users/woopinbell/work/book-task-3/backend-node/study/Node-Backend-Architecture/applied/10-shippable-backend-service/nestjs && npm run test -- --run
```

```bash
cd /Users/woopinbell/work/book-task-3/backend-node/study/Node-Backend-Architecture/applied/10-shippable-backend-service/nestjs && npm run test:e2e
```

- Node 계열 lab는 의존성 설치(`npm install` 등)가 끝난 뒤 검증 명령을 실행한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`10-shippable-backend-service-nestjs_answer.md`](10-shippable-backend-service-nestjs_answer.md)에서 확인한다.
