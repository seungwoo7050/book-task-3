# 05-auth-and-authorization development timeline

request pipeline이 정리된 다음에야 auth가 들어온다는 점이 이 프로젝트의 핵심이다. 인증과 인가는 새 기능처럼 보이지만, 실제로는 기존 `/books` 경로의 의미를 다시 정의하는 작업에 더 가깝다. 누가 public인지, 누가 token이 필요한지, 누가 admin이어야 하는지를 코드로 분해해야 한다.

## 구현 순서 요약

- Express에서 JWT 인증 middleware와 role middleware를 pipeline 위에 얹는다.
- NestJS에서 auth service, JWT strategy, guard chain으로 같은 규칙을 재구성한다.
- e2e로 register/login/public/401/403 경계를 고정한다.

## Phase 1

- 당시 목표: Express 쪽에서 authentication과 authorization을 서로 다른 middleware로 나눈다.
- 변경 단위: `express/src/middleware/auth.middleware.ts`, `express/src/middleware/role.middleware.ts`
- 처음 가설: 인증과 인가를 한 middleware에 섞으면 왜 401과 403이 다른지 설명하기 어려워진다.
- 실제 진행: `authmiddleware()`는 `Authorization: Bearer ...`를 읽고 JWT를 검증해 `req.user`를 붙이고, `requireRole()`은 role만 검사한다.

CLI:

```bash
$ cd express
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run build
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test
✓ test/e2e/auth.e2e.test.ts (9 tests)
Tests 9 passed (9)
```

검증 신호:

- register/login이 성공하면 token을 돌려준다.
- 토큰이 없으면 `401`, USER role로 관리자 경로를 두드리면 `403`이 나온다.

핵심 코드:

```ts
if (!req.user) {
  res.status(401).json({ error: "Authentication required" });
  return;
}

if (!allowedRoles.includes(req.user.role)) {
  res.status(403).json({ error: "Insufficient permissions" });
  return;
}
```

왜 이 코드가 중요했는가:

이 두 분기가 바로 auth 프로젝트의 본론이다. 인증 실패와 권한 실패가 다른 이유를 코드가 가장 짧게 보여 준다.

새로 배운 것:

- 보안 규칙을 이해한다는 건 JWT 라이브러리 사용법보다도 `401`과 `403`를 다른 단계로 나누는 감각을 갖는 일이다.

## Phase 2

- 당시 목표: NestJS에서 같은 규칙을 guard chain과 auth service로 분리한다.
- 변경 단위: `nestjs/src/auth/auth.service.ts`, `nestjs/src/auth/guards/roles.guard.ts`
- 처음 가설: NestJS는 middleware보다 guard와 decorator metadata가 role 검사에 더 잘 맞을 것이다.
- 실제 진행: `AuthService`는 user store와 bcrypt, JWT 발급을 담당하고, `RolesGuard`는 `@Roles()` metadata와 `request.user.role`을 비교한다.

CLI:

```bash
$ cd ../nestjs
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run build
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test
✓ test/e2e/auth.e2e.test.ts (4 tests)
Tests 4 passed (4)
```

검증 신호:

- Nest e2e는 `register -> login -> protected POST /books`를 한 흐름에서 검증한다.
- public `GET /books`, unauthenticated `401`, non-admin `403`도 각각 닫힌다.

핵심 코드:

```ts
const payload = { sub: user.id, username: user.username, role: user.role };
const token = this.jwtService.sign(payload);
```

왜 이 코드가 중요했는가:

JWT 자체는 단순해 보여도 여기서 role이 payload 안으로 들어가야 이후 `RolesGuard`가 route-level 권한 검사를 할 수 있다. 인증과 인가가 여기서 다시 연결된다.

새로 배운 것:

- NestJS에서는 service가 자격 증명 검증을, guard가 route 접근 판정을 맡는 식으로 역할이 더 선명하게 갈린다.

## Phase 3

- 당시 목표: 보안 규칙이 실제 HTTP 경계에서 기대한 대로 작동하는지 확인한다.
- 변경 단위: `express/test/e2e/auth.e2e.test.ts`, `nestjs/test/e2e/auth.e2e.test.ts`
- 처음 가설: auth는 unit보다 e2e가 더 중요하다. 토큰 발급, 헤더 전달, guard 실행은 다 같이 돌아가야 의미가 있기 때문이다.
- 실제 진행: register, duplicate username, login, protected POST /books, public GET /books, unauthenticated/unauthorized path를 모두 시나리오에 넣었다.

CLI:

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test
Express: Tests 9 passed (9)
NestJS: Tests 4 passed (4)
```

검증 신호:

- Express는 더 잘게 쪼갠 9개 시나리오로, NestJS는 핵심 흐름 중심 4개 시나리오로 같은 경계를 확인한다.
- 두 레인 모두 admin만 POST /books를 통과한다.

핵심 코드:

```ts
await request(app.getHttpServer())
  .post("/books")
  .set("Authorization", `Bearer ${loginRes.body.token}`)
  .send({ title: "Test", author: "A", publishedYear: 2023, genre: "F", price: 10 })
  .expect(201);
```

왜 이 코드가 중요했는가:

보안 규칙은 결국 route가 닫히느냐 열리느냐로 드러난다. 이 한 줄이 service 내부가 아니라 HTTP 경계에서 auth가 실제로 작동한다는 증거다.

새로 배운 것:

- public/private/admin 경계를 테스트 이름으로도 읽히게 만들면 이후 capstone에서 권한 규칙을 훨씬 덜 잊는다.

다음:

- [`../06-persistence-and-repositories/00-series-map.md`](../06-persistence-and-repositories/00-series-map.md)에서 이 계약을 유지한 채 저장 계층만 SQLite로 교체한다.
