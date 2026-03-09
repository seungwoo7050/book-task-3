# 05-auth-and-authorization — 개발 타임라인

이 문서는 JWT 인증과 RBAC 인가를 Express와 NestJS에서 각각 구현한 전체 개발 과정을 순서대로 기록한다.

---

## 1단계: Express 레인 셋업

### 의존성 설치

```bash
cd express
pnpm init
pnpm add express bcryptjs jsonwebtoken
pnpm add -D typescript @types/express @types/bcryptjs @types/jsonwebtoken @types/node @types/supertest supertest ts-node vitest
```

이 과제에서 새로 추가된 런타임 의존성:
- `bcryptjs` (^2.4.3): 비밀번호 해싱 (pure JS, native 컴파일 불필요)
- `jsonwebtoken` (^9.0.0): JWT 토큰 발급과 검증

타입 정의도 함께 설치: `@types/bcryptjs`, `@types/jsonwebtoken`

---

## 2단계: Express 인증 서비스 구현

### AuthService (src/services/auth.service.ts)

1. in-memory `Map<string, User>` 저장소
2. `register()`: username 중복 검사 → `bcrypt.hash(password, 10)` → UUID 생성 → 저장 → 비밀번호 제외 응답
3. `login()`: 사용자 조회 → `bcrypt.compare()` → `jwt.sign(payload, secret, { expiresIn: "1h" })` → 토큰 + 사용자 정보 응답
4. JWT_SECRET은 `process.env.JWT_SECRET || "super-secret"`에서 읽는다

---

## 3단계: Express 미들웨어 구현

### authMiddleware (src/middleware/auth.middleware.ts)

1. `Authorization` 헤더에서 `Bearer ` 접두사 확인
2. `jwt.verify(token, JWT_SECRET)` 호출
3. 성공 → `req.user = decoded` → `next()`
4. 실패 → `401 Unauthorized`

### requireRole (src/middleware/role.middleware.ts)

1. 팩토리 함수: `requireRole(...allowedRoles)` → 미들웨어 반환
2. `req.user`가 없으면 401
3. `req.user.role`이 `allowedRoles`에 없으면 403
4. 통과하면 `next()`

### 라우트 조립

```
// 공개
POST /auth/register
POST /auth/login
GET /books

// 인증 필요
GET /books/:id  → authMiddleware → handler

// 인증 + 관리자만
POST /books     → authMiddleware → requireRole("ADMIN") → handler
PUT /books/:id  → authMiddleware → requireRole("ADMIN") → handler
DELETE /books/:id → authMiddleware → requireRole("ADMIN") → handler
```

---

## 4단계: NestJS 레인 셋업

### 의존성 설치

```bash
cd nestjs
pnpm init
pnpm add @nestjs/common @nestjs/core @nestjs/platform-express @nestjs/jwt @nestjs/passport bcryptjs passport passport-jwt reflect-metadata rxjs
pnpm add -D @nestjs/cli @nestjs/testing @types/bcryptjs @types/node @types/passport-jwt @types/supertest supertest typescript vitest
```

이 과제에서 새로 추가된 런타임 의존성:
- `@nestjs/jwt` (^10.2.0): NestJS JWT 모듈
- `@nestjs/passport` (^10.0.0): NestJS Passport 통합
- `passport` (^0.7.0): 인증 프레임워크
- `passport-jwt` (^4.0.0): JWT 전략

---

## 5단계: NestJS 인증 모듈 구현

### AuthModule 구성

```
src/auth/
├── auth.module.ts          ← JwtModule.register(), PassportModule import
├── auth.controller.ts      ← POST /auth/register, POST /auth/login
├── auth.service.ts         ← bcrypt 해싱, JWT 발급
├── strategies/
│   └── jwt.strategy.ts     ← Passport JwtStrategy
├── guards/
│   └── roles.guard.ts      ← RBAC Guard
├── decorators/
│   └── roles.decorator.ts  ← @Roles() 커스텀 데코레이터
└── dto/
    ├── register.dto.ts
    └── login.dto.ts
```

### JwtStrategy

`PassportStrategy(Strategy)`를 상속. `ExtractJwt.fromAuthHeaderAsBearerToken()`으로 토큰 추출. `validate(payload)`에서 `{ userId, username, role }`을 반환하면 자동으로 request에 붙는다.

### @Roles 데코레이터와 RolesGuard

`@SetMetadata('roles', roles)`로 메타데이터를 설정하고, `RolesGuard`가 `Reflector`로 읽어서 현재 사용자의 role과 비교한다.

---

## 6단계: 테스트

### Express 테스트 흐름

1. register로 사용자 생성
2. login으로 토큰 발급
3. 토큰 없이 보호된 엔드포인트 → 401 확인
4. 토큰으로 접근 → 200 확인
5. USER 역할로 ADMIN 전용 엔드포인트 → 403 확인
6. ADMIN 역할로 접근 → 성공 확인

### NestJS 테스트 흐름

동일한 시나리오를 `@nestjs/testing`의 `Test.createTestingModule`로 구성하고 `supertest`로 검증.

---

## 7단계: 빌드와 검증

### Express

```bash
cd express
pnpm install
pnpm run build
pnpm run test
```

### NestJS

```bash
cd nestjs
pnpm install
pnpm run build
pnpm run test
```

### curl 수동 검증

```bash
# 사용자 등록
curl -X POST http://localhost:3000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"pass123","role":"ADMIN"}'

# 로그인
curl -X POST http://localhost:3000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"pass123"}'
# → token을 복사

# 보호된 엔드포인트 접근
curl -X POST http://localhost:3000/books \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"title":"Auth Book","author":"Alice","publishedYear":2026}'

# 토큰 없이 접근 → 401
curl http://localhost:3000/books/1
```

---

## 프로젝트 파일 구조 최종 상태

```
05-auth-and-authorization/
├── README.md
├── docs/
├── express/
│   ├── package.json
│   ├── src/
│   │   ├── app.ts, main.ts
│   │   ├── controllers/
│   │   ├── services/{auth.service.ts, book.service.ts}
│   │   ├── middleware/{auth.middleware.ts, role.middleware.ts}
│   │   ├── routes/
│   │   ├── types/
│   │   └── utils/
│   └── test/
├── nestjs/
│   ├── package.json, nest-cli.json
│   ├── src/
│   │   ├── app.module.ts, main.ts
│   │   ├── auth/{module, controller, service, strategies/, guards/, decorators/, dto/}
│   │   └── books/
│   └── test/
└── problem/
```

---

## 사용한 도구 요약

| 도구 | 용도 |
|------|------|
| bcryptjs | 비밀번호 해싱 (salt rounds: 10) |
| jsonwebtoken | Express에서 JWT 발급/검증 |
| @nestjs/jwt | NestJS JWT 모듈 |
| passport + passport-jwt | NestJS 인증 전략 |
| @nestjs/passport | NestJS-Passport 통합 |
| supertest | 인증 흐름 E2E 테스트 |
| curl | 토큰 발급 → 보호 엔드포인트 접근 수동 검증 |
