# 05-auth-and-authorization evidence ledger

근거는 [`README.md`](../../../study/Node-Backend-Architecture/core/05-auth-and-authorization/README.md), [`express/src/middleware/auth.middleware.ts`](../../../study/Node-Backend-Architecture/core/05-auth-and-authorization/express/src/middleware/auth.middleware.ts), [`express/src/middleware/role.middleware.ts`](../../../study/Node-Backend-Architecture/core/05-auth-and-authorization/express/src/middleware/role.middleware.ts), [`nestjs/src/auth/auth.service.ts`](../../../study/Node-Backend-Architecture/core/05-auth-and-authorization/nestjs/src/auth/auth.service.ts), [`nestjs/src/auth/guards/roles.guard.ts`](../../../study/Node-Backend-Architecture/core/05-auth-and-authorization/nestjs/src/auth/guards/roles.guard.ts), 두 레인의 e2e 출력이다.

## Phase 1

- 순서: 1
- 시간 표지: Phase 1
- 당시 목표: Express pipeline 위에 JWT 인증과 role 검사 middleware를 올린다.
- 변경 단위: `express/src/middleware/auth.middleware.ts`, `express/src/middleware/role.middleware.ts`, `express/src/services/auth.service.ts`
- 처음 가설: auth 규칙은 새 API를 만드는 일이 아니라 기존 pipeline 어디에서 `401`과 `403`을 갈라낼지 정하는 일이다.
- 실제 조치: JWT를 검증해 `req.user`를 붙이는 `authmiddleware()`와 허용 role을 검사하는 `requireRole()`을 만들었다.
- CLI: `COREPACK_ENABLE_AUTO_PIN=0 pnpm run build`, `COREPACK_ENABLE_AUTO_PIN=0 pnpm run test`
- 검증 신호: `✓ test/e2e/auth.e2e.test.ts (9 tests)`, `Tests 9 passed (9)`
- 핵심 코드 앵커: `authmiddleware()`, `requireRole()`
- 새로 배운 것: 인증과 인가는 한 번에 설명되지만 실제 코드에서는 "사용자를 붙이는 단계"와 "권한을 검사하는 단계"가 분리돼야 한다.
- 다음: 같은 규칙을 Nest guard chain으로 옮긴다.

## Phase 2

- 순서: 2
- 시간 표지: Phase 2
- 당시 목표: NestJS에서 JWT 발급과 guard chain을 controller 밖으로 분리한다.
- 변경 단위: `nestjs/src/auth/auth.service.ts`, `nestjs/src/auth/guards/*`, `nestjs/src/auth/strategies/jwt.strategy.ts`
- 처음 가설: NestJS에서는 middleware보다 `JwtAuthGuard`와 `RolesGuard`가 더 자연스럽게 역할을 나눌 것이다.
- 실제 조치: `AuthService`가 register/login과 token 발급을 담당하고, `RolesGuard`가 decorator metadata를 읽어 role을 검사하게 했다.
- CLI: `COREPACK_ENABLE_AUTO_PIN=0 pnpm run build`, `COREPACK_ENABLE_AUTO_PIN=0 pnpm run test`
- 검증 신호: `✓ test/e2e/auth.e2e.test.ts (4 tests)`, `Tests 4 passed (4)`
- 핵심 코드 앵커: `AuthService.login()`, `RolesGuard.canActivate()`
- 새로 배운 것: NestJS에서는 "누가 보호됐는가"가 guard 선언과 decorator에 더 가깝고, service는 자격 증명 검증 자체에 집중한다.
- 다음: 401/403/public route 경계를 e2e로 고정한다.

## Phase 3

- 순서: 3
- 시간 표지: Phase 3
- 당시 목표: register/login/protected/public 경계를 실제 요청으로 검증한다.
- 변경 단위: `express/test/e2e/auth.e2e.test.ts`, `nestjs/test/e2e/auth.e2e.test.ts`
- 처음 가설: auth 프로젝트는 unit보다 e2e가 더 많은 사실을 말해 준다.
- 실제 조치: register -> login -> protected POST /books, unauthenticated 401, non-admin 403, public GET /books를 모두 테스트에 넣었다.
- CLI: `pnpm run test`
- 검증 신호: Express 9 tests, Nest 4 tests 모두 통과했고 Nest는 `register, login, access protected route` 한 시나리오를 명시적으로 확인했다.
- 핵심 코드 앵커: `auth.e2e.test.ts`
- 새로 배운 것: 보안 기초의 핵심은 JWT를 발급하는 법보다 "공개 경로, 인증 필요 경로, 권한 필요 경로"를 다르게 설명하는 것이다.
- 다음: `06-persistence-and-repositories`에서 이 계약을 유지한 채 저장 계층만 바꾼다.
