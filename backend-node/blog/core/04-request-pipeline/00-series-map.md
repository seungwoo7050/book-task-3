# 04-request-pipeline series map

`03-rest-api-foundations`가 CRUD를 두 프레임워크로 비교하는 단계였다면, 이 프로젝트는 그보다 앞에 깔리는 공통 규약을 먼저 드러낸다. validation, error handling, logging, response envelope가 독립 계층으로 서야 이후 auth와 persistence도 덜 흔들린다.

처음 읽을 때는 Express middleware 쪽을 먼저 보는 편이 좋다. `validate`, `responseWrapper`, `errorHandler`가 어떤 순서로 붙는지 이해한 뒤 NestJS filter/interceptor로 넘어가면 "같은 규약을 다른 프레임워크가 어떻게 감싸는가"가 훨씬 잘 보인다.

## 이 글에서 볼 것

- validation을 route handler 밖으로 빼는 이유
- 성공/실패 응답의 표면을 통일하면 무엇이 쉬워지는지
- Express middleware 순서와 NestJS global pipeline이 어떻게 대응되는지

## source of truth

- `core/04-request-pipeline/README.md`
- `core/04-request-pipeline/problem/README.md`
- `core/04-request-pipeline/express/src/middleware/*`
- `core/04-request-pipeline/nestjs/src/common/*`
- `core/04-request-pipeline/express/test/e2e/pipeline.e2e.test.ts`
- `core/04-request-pipeline/nestjs/test/e2e/pipeline.e2e.test.ts`

## 구현 흐름 한눈에 보기

1. Express에서 validation을 middleware 단계로 분리한다.
2. success/error envelope를 공통 표면으로 고정한다.
3. NestJS에서는 global pipe/filter/interceptor 조합으로 같은 규약을 다시 세운다.

## 대표 검증

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run build && pnpm run test && pnpm run test:e2e
Tests       16 passed (16)
test:e2e    9 passed (9)
```

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run build && pnpm run test && pnpm run test:e2e
Tests       7 passed (7)
test:e2e    8 passed (8)
```

## 다음 프로젝트와의 연결

다음 장 `05-auth-and-authorization`은 여기서 만든 pipeline 위에 JWT와 RBAC를 올린다. 즉 요청 흐름이 먼저 안정돼 있어야 보안 규칙도 어디에 걸리는지 선명해진다.
