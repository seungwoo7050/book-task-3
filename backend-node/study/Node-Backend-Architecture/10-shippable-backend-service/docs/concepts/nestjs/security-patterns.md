# Security Patterns

## 인증

- 로그인 성공 시 JWT를 발급한다.
- payload는 `sub`, `username`, `role`을 포함한다.
- 관리자 쓰기 라우트는 `JwtAuthGuard`와 `RolesGuard`를 함께 사용한다.

## 인가

- `GET /books`, `GET /books/:id`는 public이다.
- `POST`, `PUT`, `DELETE /books`는 `ADMIN`만 허용한다.

## 로그인 throttling

- key는 `auth:login:<clientId>`다.
- 같은 clientId에서 60초 안에 5회 실패하면 `429`를 반환한다.
- 성공 로그인 시 실패 카운터를 제거한다.

## 제외한 것

- refresh token
- password reset
- multi-factor auth
- account lock 정책의 영속화
