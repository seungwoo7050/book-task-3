# 05-auth-and-authorization series map

이 lab의 표면적인 주제는 JWT와 RBAC다. 하지만 소스를 다시 따라가 보니 더 중요한 질문은 따로 있었다. "누가 토큰을 만들고, 누가 그 토큰을 해석하고, 누가 role을 보고 마지막으로 통과 여부를 결정하는가"다. 즉 핵심은 로그인 기능 자체보다 `401`과 `403`이 어디서 갈라지는지에 있다.

이번 재검토에서는 또 하나의 사실이 분명해졌다. README는 이전 request pipeline 위에 auth를 올린다고 말하지만, 실제 구현은 그 pipeline의 표준 success/error envelope나 validation 규약을 거의 재사용하지 않는다. 대신 인증과 권한 경계에만 집중한 별도 실험에 가깝다.

## 이 글에서 볼 것

- bcrypt hashing과 JWT claim 구성이 왜 auth service에서 먼저 고정되는지
- Express는 `authmiddleware -> requireRole("ADMIN")`로, NestJS는 `JwtAuthGuard -> RolesGuard`로 어떻게 `401`과 `403`을 분리하는지
- 두 레인 모두 role 경계는 세웠지만, auth 입력 validation과 표준 response envelope는 아직 느슨하다는 현재 상태

## source of truth

- `core/05-auth-and-authorization/problem/README.md`
- `core/05-auth-and-authorization/README.md`
- `core/05-auth-and-authorization/express/src/app.ts`
- `core/05-auth-and-authorization/express/src/services/auth.service.ts`
- `core/05-auth-and-authorization/express/src/middleware/auth.middleware.ts`
- `core/05-auth-and-authorization/express/src/middleware/role.middleware.ts`
- `core/05-auth-and-authorization/express/src/routes/book.router.ts`
- `core/05-auth-and-authorization/express/test/e2e/auth.e2e.test.ts`
- `core/05-auth-and-authorization/nestjs/src/auth/auth.module.ts`
- `core/05-auth-and-authorization/nestjs/src/auth/auth.service.ts`
- `core/05-auth-and-authorization/nestjs/src/auth/guards/jwt-auth.guard.ts`
- `core/05-auth-and-authorization/nestjs/src/auth/guards/roles.guard.ts`
- `core/05-auth-and-authorization/nestjs/src/auth/strategies/jwt.strategy.ts`
- `core/05-auth-and-authorization/nestjs/src/books/books.controller.ts`
- `core/05-auth-and-authorization/nestjs/test/e2e/auth.e2e.test.ts`

## 구현 흐름 한눈에 보기

1. auth service에서 사용자 등록, 비밀번호 해시, JWT 발급 payload를 고정한다.
2. Express는 middleware chain으로 token 유무와 role 허용 여부를 순차 검사한다.
3. NestJS는 Passport JWT strategy와 guard chain으로 같은 경계를 다시 세운다.
4. 다만 두 레인 모두 이전 lab의 공통 response envelope를 유지하지 않고, auth 입력 검증도 비어 있어 빈 `username/password` 등록이 실제로 성공한다.

## 대표 검증

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run build
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test
Test Files  1 passed (1)
Tests       9 passed (9)
```

```bash
$ node -e "const request=require('supertest'); const { createApp } = require('./dist/app.js'); ... "
{"unauth":{"status":401,"body":{"error":"Authentication required"}},"forbidden":{"status":403,"body":{"error":"Insufficient permissions"}}}
```

```bash
$ node -e "const request=require('supertest'); const { createApp } = require('./dist/app.js'); request(createApp()).post('/auth/register').send({ username:'', password:'' }) ..."
201 { id: '...', username: '', role: 'USER' }
```

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run build
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test
Test Files  1 passed (1)
Tests       4 passed (4)
```

```bash
$ node -e "require('reflect-metadata'); ... request(app.getHttpServer()).post('/books') ..."
{"unauth":{"status":401,"body":{"message":"Unauthorized","statusCode":401}},"forbidden":{"status":403,"body":{"message":"Insufficient permissions","error":"Forbidden","statusCode":403}}}
```

```bash
$ node -e "require('reflect-metadata'); ... request(app.getHttpServer()).post('/auth/register').send({ username:'', password:'' }) ..."
201 { id: '...', username: '', role: 'USER' }
```

## 다음 프로젝트와의 연결

다음 `06-persistence-and-repositories`는 여기서 세운 공개/보호 route 경계를 유지한 채 저장 계층만 바꾸는 단계다. 그래서 이 lab은 auth의 완성본이라기보다, 이후 feature들이 기대할 수 있는 최소한의 인증/인가 경계선을 먼저 긋는 단계로 보는 편이 맞다.
