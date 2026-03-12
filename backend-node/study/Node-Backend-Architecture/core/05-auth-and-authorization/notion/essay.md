# JWT 인증과 RBAC 인가를 붙이면 달라지는 것

## 왜 파이프라인 다음에 auth인가

`04-request-pipeline`에서 validation, error handling, response shaping을 공통 규약으로 만들어 두었다. 인증도 결국 파이프라인의 한 단계 — "이 요청을 보낸 사람이 누구인가" — 이기 때문에, 파이프라인이 먼저 정리되어 있어야 auth를 깔끔하게 끼워 넣을 수 있다.

여기서는 JWT 토큰으로 인증하고, 토큰에 담긴 role로 인가(RBAC)를 처리한다. 같은 흐름을 Express의 미들웨어 체인과 NestJS의 Guard 체인으로 각각 구현한다.

## 인증 흐름: register → login → token → 보호된 리소스

### 회원가입 (register)

1. 클라이언트가 `POST /auth/register`에 username, password, role(선택)을 보낸다
2. 서버가 username 중복을 검사한다
3. `bcryptjs`로 비밀번호를 해싱한다 (salt rounds: 10)
4. UUID를 생성해서 사용자를 in-memory 저장소에 저장한다
5. 비밀번호를 제외한 사용자 정보를 응답한다

### 로그인 (login)

1. 클라이언트가 `POST /auth/login`에 username, password를 보낸다
2. 서버가 사용자를 찾고 `bcrypt.compare`로 비밀번호를 검증한다
3. 성공하면 JWT 토큰을 발급한다 (payload: sub, username, role / 만료: 1시간)
4. 토큰과 사용자 정보를 응답한다

### 보호된 리소스 접근

1. 클라이언트가 `Authorization: Bearer <token>` 헤더를 붙여서 보호된 엔드포인트에 요청한다
2. 미들웨어/Guard가 토큰을 검증하고 디코딩한다
3. 디코딩된 payload를 `req.user`(Express) 또는 실행 컨텍스트(NestJS)에 붙인다
4. 역할 검사가 필요한 엔드포인트에서 `role`을 확인한다

## bcrypt를 선택한 이유

비밀번호 해싱에 `bcryptjs`를 사용했다. native `bcrypt`와 달리 C++ 컴파일이 필요 없어서 설치가 간단하다. 성능 차이는 있지만 학습 단계에서는 설치 편의성이 우선이다.

salt rounds를 10으로 설정한 건, 학습용에서 충분히 안전하면서 테스트 속도가 너무 느려지지 않는 균형점이다.

## Express 레인: 미들웨어 체인으로 인증

### authMiddleware

모든 보호된 라우트 앞에 `authMiddleware`를 등록한다:

1. `Authorization` 헤더에서 `Bearer ` 접두사를 확인한다
2. 토큰을 `jwt.verify()`로 검증한다
3. 성공하면 디코딩된 payload를 `req.user`에 붙인다
4. 실패하면 `401 Unauthorized`를 반환한다

### requireRole 미들웨어

`requireRole("ADMIN")`처럼 허용 역할을 지정해서, `req.user.role`이 포함되지 않으면 `403 Forbidden`을 반환한다. `authMiddleware` 뒤에 체이닝해야 한다.

Express에서는 이 두 미들웨어의 순서가 중요하다. `auth → role → handler` 순서가 바뀌면 `req.user`가 없는 상태에서 role 검사를 하게 된다.

## NestJS 레인: Guard + Strategy + Decorator로 인증

### Passport + JWT Strategy

NestJS에서는 `@nestjs/passport`와 `passport-jwt`를 사용한다. `JwtStrategy`가 토큰을 검증하고 payload를 반환하면, `@nestjs/passport`의 `AuthGuard('jwt')`가 자동으로 실행 컨텍스트에 사용자 정보를 붙인다.

### RoleGuard와 @Roles 데코레이터

NestJS에서는 메타데이터 기반으로 역할을 검사한다:

1. `@Roles('ADMIN')` 데코레이터로 허용 역할을 컨트롤러 메서드에 선언한다
2. `RolesGuard`가 `Reflector`로 메타데이터를 읽고 현재 사용자의 role과 비교한다
3. 불일치하면 `ForbiddenException`을 던진다

Express에서 `requireRole("ADMIN")`으로 직접 지정했던 것을, NestJS에서는 데코레이터 + Guard + Reflector 조합으로 선언적으로 처리한다.

### @nestjs/jwt vs 직접 jwt.sign

NestJS 레인에서는 `@nestjs/jwt`의 `JwtService`를 사용한다. `JwtModule.register()`에서 secret과 signOptions를 설정하면, 서비스에서 `this.jwtService.sign(payload)`로 토큰을 발급한다. Express에서 `jwt.sign(payload, secret, { expiresIn })`으로 직접 호출하던 것의 DI 래퍼다.

## Express와 NestJS 인증 비교

| 관점 | Express | NestJS |
|------|---------|--------|
| 토큰 검증 | `jwt.verify()` 직접 호출 | Passport + JwtStrategy |
| 사용자 정보 전달 | `req.user` 직접 할당 | ExecutionContext에 자동 |
| 역할 검사 | `requireRole()` 미들웨어 | `@Roles()` + RolesGuard |
| 공개/보호 구분 | 미들웨어 등록 순서 | Guard 적용 범위 |
| JWT 발급 | `jsonwebtoken` 직접 사용 | `@nestjs/jwt` JwtService |
| 비밀키 관리 | `process.env.JWT_SECRET` | `JwtModule.register({ secret })` |

## 이 과제에서 만든 것이 이후에 쓰이는 곳

- **JWT 인증 패턴**: `09-platform-capstone`과 `10-shippable-backend-service`에서 그대로 사용된다
- **RBAC Guard**: `09`, `10`에서 Admin 전용 쓰기 엔드포인트에 동일하게 적용된다
- **bcrypt 해싱**: `10`에서 Postgres 저장소로 교체될 때도 해싱 로직은 동일하다
- **인증 테스트 패턴**: 토큰을 발급하고 → 보호된 엔드포인트에 보내고 → 응답을 검증하는 흐름이 이후 모든 E2E 테스트의 기본이 된다

이 과제는 "누가 이 요청을 보냈는가"를 시스템에 끼워 넣는 첫 경험이다. 다음 과제인 `06-persistence-and-repositories`에서는 "그 데이터를 어디에 저장하는가"로 넘어간다.
