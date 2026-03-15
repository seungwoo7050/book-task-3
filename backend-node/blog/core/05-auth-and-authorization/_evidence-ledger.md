# 05-auth-and-authorization evidence ledger

이 lab의 path history도 `2026-03-12` 이관 커밋 한 번으로 압축돼 있어, chronology는 auth service, middleware/guard chain, e2e tests, 추가 재실행 CLI를 기준으로 다시 복원했다. 기존 blog 본문은 사실 근거로 사용하지 않았다.

| 순서 | 시간 표지 | 당시 목표 | 변경 단위 | 처음 가설 | 실제 조치 | CLI | 검증 신호 | 핵심 코드 앵커 | 새로 배운 것 | 다음 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Phase 1 | auth service에서 등록, 해시, JWT 발급을 고정한다 | `express/src/services/auth.service.ts`, `nestjs/src/auth/auth.service.ts`, `nestjs/src/auth/auth.module.ts`, `nestjs/src/auth/strategies/jwt.strategy.ts` | 인증 훅 포인트가 핵심이니 middleware/guard부터 보면 될 것 같았다 | 실제 출발점은 둘 다 auth service였고, 여기서 bcrypt hash와 `{ sub, username, role }` payload를 먼저 고정했다 | `COREPACK_ENABLE_AUTO_PIN=0 pnpm run build`, `COREPACK_ENABLE_AUTO_PIN=0 pnpm run test` (각 레인) | Express 9개, Nest 4개 테스트 통과 | `const token = jwt.sign(payload, JWT_SECRET, { expiresIn: "1h" })`, `this.jwtService.sign(payload)` | route 경계보다 먼저 중요한 것은 토큰에 어떤 claim을 넣고 어떤 secret으로 서명하는가다 | 이 claim을 요청 경계에서 읽어 `401`과 `403`을 갈라야 한다 |
| 2 | Phase 2 | 인증과 권한 검사를 다른 단계로 나눈다 | `express/src/middleware/auth.middleware.ts`, `express/src/middleware/role.middleware.ts`, `express/src/routes/book.router.ts`, `nestjs/src/auth/guards/jwt-auth.guard.ts`, `nestjs/src/auth/guards/roles.guard.ts`, `nestjs/src/books/books.controller.ts` | token만 검증하면 role 체크도 같은 자리에서 묶어도 될 것 같았다 | Express는 `authmiddleware -> requireRole("ADMIN")`, NestJS는 `JwtAuthGuard -> RolesGuard`로 순서를 분리해 `401`과 `403`의 의미 차이를 코드에 남겼다 | `node -e "const request=require('supertest'); const { createApp } = require('./dist/app.js'); ..."` (`express/`), `node -e "require('reflect-metadata'); ..."` (`nestjs/`) | Express는 `401 { error: ... }` / `403 { error: ... }`, NestJS는 기본 exception body로 `401`/`403` 반환 | `router.post("/", authmiddleware, requireRole("ADMIN"), ...)`, `@UseGuards(JwtAuthGuard, RolesGuard)` | 두 레인 모두 상태코드 경계는 지키지만, response 표면은 서로 다르고 이전 pipeline lab의 공통 envelope도 재사용하지 않는다 | role 경계는 통과하지만 validation은 어떤지 본다 |
| 3 | Phase 3 | 공개 route와 보호 route를 같은 흐름에서 검증한다 | `express/test/e2e/auth.e2e.test.ts`, `nestjs/test/e2e/auth.e2e.test.ts` | 로그인 성공만 확인해도 auth 설명은 충분할 것 같았다 | duplicate username, invalid credentials, unauthenticated write, non-admin write, public read를 같은 e2e 시나리오로 묶었다 | 위 테스트 명령 재실행 | Express 9개 시나리오, Nest 4개 시나리오 통과 | `GET /books`는 공개, `POST /books`는 admin 전용이라는 테스트 구성 | auth는 token 발급 자체보다 어떤 route가 공개이고 어떤 route가 보호되는지에서 더 선명해진다 | auth 입력 validation을 직접 찔러 본다 |
| 4 | Phase 4 | role 경계와 validation 공백을 분리해 본다 | `express/src/controllers/auth.controller.ts`, `nestjs/src/auth/dto/register.dto.ts`, `nestjs/src/auth/dto/login.dto.ts`, `nestjs/src/main.ts` | DTO 이름이 있으니 최소한 빈 credential 정도는 막을 거라고 생각하기 쉽다 | Express는 register body를 그대로 넘기고, NestJS는 validator decorator도 `ValidationPipe`도 없이 plain DTO만 사용한다는 점을 확인한 뒤 빈 문자열 등록을 직접 재실행했다 | `node -e "const request=require('supertest'); ... post('/auth/register').send({ username:'', password:'' }) ..."` (두 레인) | 두 레인 모두 `201`과 빈 `username` 등록 성공 | `export class RegisterDto { username!: string; password!: string; ... }` | 이 lab의 현재 강점은 role 경계이고, credential validation은 아직 마련되지 않았다 | `06-persistence-and-repositories`에서 이 경계를 유지한 채 저장 계층만 교체한다 |

## 근거 파일

- `core/05-auth-and-authorization/problem/README.md`
- `core/05-auth-and-authorization/README.md`
- `core/05-auth-and-authorization/express/src/app.ts`
- `core/05-auth-and-authorization/express/src/controllers/auth.controller.ts`
- `core/05-auth-and-authorization/express/src/services/auth.service.ts`
- `core/05-auth-and-authorization/express/src/middleware/auth.middleware.ts`
- `core/05-auth-and-authorization/express/src/middleware/role.middleware.ts`
- `core/05-auth-and-authorization/express/src/routes/book.router.ts`
- `core/05-auth-and-authorization/express/test/e2e/auth.e2e.test.ts`
- `core/05-auth-and-authorization/nestjs/src/main.ts`
- `core/05-auth-and-authorization/nestjs/src/auth/auth.module.ts`
- `core/05-auth-and-authorization/nestjs/src/auth/auth.controller.ts`
- `core/05-auth-and-authorization/nestjs/src/auth/auth.service.ts`
- `core/05-auth-and-authorization/nestjs/src/auth/dto/register.dto.ts`
- `core/05-auth-and-authorization/nestjs/src/auth/dto/login.dto.ts`
- `core/05-auth-and-authorization/nestjs/src/auth/guards/jwt-auth.guard.ts`
- `core/05-auth-and-authorization/nestjs/src/auth/guards/roles.guard.ts`
- `core/05-auth-and-authorization/nestjs/src/auth/strategies/jwt.strategy.ts`
- `core/05-auth-and-authorization/nestjs/src/books/books.controller.ts`
- `core/05-auth-and-authorization/nestjs/test/e2e/auth.e2e.test.ts`
