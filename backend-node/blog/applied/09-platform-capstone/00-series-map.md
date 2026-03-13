# 09-platform-capstone series map

이 프로젝트는 지금까지 나눠서 만들던 REST, pipeline, auth, persistence, events, 운영 규약을 하나의 NestJS 서비스에 모으는 통합판이다. 핵심은 기능을 더 많이 넣는 것이 아니라, 이전 단계에서 세워 둔 invariant가 한 앱 안에서도 그대로 살아남는지 보는 데 있다.

처음 읽을 때는 `AuthService`와 `BooksService`를 먼저 본 뒤, `HttpExceptionFilter`와 `LoggingInterceptor`, 그리고 e2e 테스트로 내려가는 편이 좋다. 이렇게 읽으면 모듈 조합과 공통 규약, 실제 사용자 흐름이 한 줄로 이어진다.

## 이 글에서 볼 것

- auth, books, events가 한 앱으로 묶여도 각자 책임을 유지하는지
- 공통 error/logging contract가 통합 과정에서 어떻게 다시 고정되는지
- 관리자/일반 사용자/public read 흐름이 왜 capstone의 핵심 검증이 되는지

## source of truth

- `applied/09-platform-capstone/README.md`
- `applied/09-platform-capstone/problem/README.md`
- `applied/09-platform-capstone/nestjs/src/auth/*`
- `applied/09-platform-capstone/nestjs/src/books/*`
- `applied/09-platform-capstone/nestjs/src/common/*`
- `applied/09-platform-capstone/nestjs/src/events/*`
- `applied/09-platform-capstone/nestjs/test/unit/auth.service.test.ts`
- `applied/09-platform-capstone/nestjs/test/e2e/capstone.e2e.test.ts`

## 구현 흐름 한눈에 보기

1. auth/books/events/persistence를 한 앱 안에 조합한다.
2. exception filter, logging interceptor, event listener로 공통 규약을 다시 맞춘다.
3. register/login/admin CRUD/public read/regular user forbidden을 e2e로 묶는다.

## 대표 검증

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run build && pnpm run test && pnpm run test:e2e
Tests       10 passed (10)
test:e2e    12 passed (12)
```

## 다음 프로젝트와의 연결

다음 장 `10-shippable-backend-service`는 이 capstone을 Postgres, Redis, Swagger, Docker Compose까지 갖춘 제출용 서비스 표면으로 다시 패키징한다.
