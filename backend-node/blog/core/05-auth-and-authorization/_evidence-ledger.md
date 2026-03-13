# 05-auth-and-authorization evidence ledger

이 프로젝트의 git path history도 `2026-03-12` 이관 커밋 하나로만 보인다. chronology는 auth service, middleware/guard, e2e tests, 재검증 CLI를 기준으로 다시 세웠다.

| 순서 | 시간 표지 | 당시 목표 | 변경 단위 | 처음 가설 | 실제 조치 | CLI | 검증 신호 | 핵심 코드 앵커 | 새로 배운 것 | 다음 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Phase 1 | register/login과 JWT 발급을 service 경계에 올린다 | `express/src/services/auth.service.ts`, `nestjs/src/auth/auth.service.ts` | 보안 실습이면 middleware나 guard부터 떠올리기 쉽다 | bcrypt hashing, duplicate username, JWT 발급을 auth service 안에 모았다 | `COREPACK_ENABLE_AUTO_PIN=0 pnpm run build && pnpm run test` (`express/`) | `Tests 9 passed` | `const token = jwt.sign(payload, JWT_SECRET, { expiresIn: "1h" })` | 인증은 보호된 route보다 먼저, 어떤 credential을 발급하고 검증할지에서 시작한다 | 이 token을 요청 경계에서 해석해야 한다 |
| 2 | Phase 2 | authentication과 authorization을 다른 단계로 나눈다 | `express/src/middleware/auth.middleware.ts`, `role.middleware.ts`, `nestjs/src/auth/guards/roles.guard.ts` | token 검증이 끝나면 권한 검사도 같은 자리에서 같이 처리해도 될 것 같았다 | Express는 `authMiddleware -> requireRole`, NestJS는 `JwtAuthGuard -> RolesGuard`로 `401`과 `403`를 갈랐다 | `COREPACK_ENABLE_AUTO_PIN=0 pnpm run build && pnpm run test` (`nestjs/`) | `Tests 4 passed` | `if (!allowedRoles.includes(req.user.role)) { ... 403 ... }` | authentication과 authorization은 실패 의미가 다르기 때문에 코드 경계도 갈라져야 한다 | public route와 protected route를 함께 확인해야 한다 |
| 3 | Phase 3 | 공개/보호 route를 한 흐름에서 묶어 검증한다 | `express/test/e2e/auth.e2e.test.ts`, `nestjs/test/e2e/auth.e2e.test.ts` | 로그인 성공만 보면 보안 기능도 충분히 설명된 것처럼 느껴질 수 있다 | duplicate username, invalid credentials, unauthenticated write, forbidden write, public read를 같은 e2e 흐름에 넣었다 | 위 명령 재실행 | Express 9개, Nest 4개 시나리오 통과 | public GET `/books`와 protected POST `/books`가 같은 파일 안에 있는 테스트 구성 | 보안 규칙은 token 발급 자체보다 어떤 route가 어떤 status code로 막히는지에서 더 선명하다 | 다음 프로젝트에서 이 API 계약을 유지한 채 저장 계층만 교체한다 |

## 근거 파일

- `core/05-auth-and-authorization/README.md`
- `core/05-auth-and-authorization/problem/README.md`
- `core/05-auth-and-authorization/express/src/services/auth.service.ts`
- `core/05-auth-and-authorization/express/src/middleware/auth.middleware.ts`
- `core/05-auth-and-authorization/express/src/middleware/role.middleware.ts`
- `core/05-auth-and-authorization/nestjs/src/auth/auth.service.ts`
- `core/05-auth-and-authorization/nestjs/src/auth/guards/roles.guard.ts`
- `core/05-auth-and-authorization/express/test/e2e/auth.e2e.test.ts`
- `core/05-auth-and-authorization/nestjs/test/e2e/auth.e2e.test.ts`
