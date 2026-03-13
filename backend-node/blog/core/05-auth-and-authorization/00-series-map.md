# 05-auth-and-authorization series map

이 프로젝트에서는 `request pipeline` 위에 JWT 인증과 RBAC 인가가 올라온다. 중요한 건 "로그인이 된다"는 사실보다, 인증되지 않은 요청과 권한 없는 요청을 어디서, 어떻게 다르게 끊어 내는가다.

처음 읽을 때는 auth service를 먼저 보는 편이 좋다. register/login이 어떤 규칙으로 서는지 본 뒤 middleware나 guard로 넘어가야 `401`과 `403`의 경계가 자연스럽게 읽힌다.

## 이 글에서 볼 것

- password hashing과 JWT 발급이 왜 service 안에서 먼저 정리되는지
- Express의 middleware chain과 NestJS의 guard chain이 어떤 역할 분리를 가지는지
- public `GET /books`와 protected `POST /books`가 함께 있어야 보안 규칙이 왜 선명해지는지

## source of truth

- `core/05-auth-and-authorization/README.md`
- `core/05-auth-and-authorization/problem/README.md`
- `core/05-auth-and-authorization/express/src/*`
- `core/05-auth-and-authorization/nestjs/src/*`
- `core/05-auth-and-authorization/express/test/e2e/auth.e2e.test.ts`
- `core/05-auth-and-authorization/nestjs/test/e2e/auth.e2e.test.ts`

## 구현 흐름 한눈에 보기

1. auth service에서 register/login, bcrypt hashing, JWT 발급을 먼저 만든다.
2. Express는 middleware chain으로, NestJS는 guard chain으로 authentication과 authorization을 분리한다.
3. duplicate username, invalid credentials, unauthenticated write, forbidden write, public read를 e2e로 묶는다.

## 대표 검증

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run build && pnpm run test
Tests       9 passed (9)
Duration    1.57s
```

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run build && pnpm run test
Tests       4 passed (4)
Duration    1.05s
```

## 다음 프로젝트와의 연결

다음 장 `06-persistence-and-repositories`에서는 지금 만든 API 계약과 보안 경계를 그대로 둔 채, 저장 계층만 in-memory에서 SQLite로 교체한다.
