# 07 Auth Session JWT Series Map

`01-backend-core/07-auth-session-jwt`는 session login과 JWT login을 함께 구현해 인증 방식과 인가 경계를 비교하는 브리지 과제다.

## 이 시리즈가 복원하는 것

- 시작점: cookie session과 bearer JWT를 둘 다 경험해야 한다.
- 구현 축: session login, JWT login, role-based authorization 예제를 `solution/go`에 구현했다.
- 검증 축: 2026-03-07 기준 `go test ./...`가 통과했다.
- 글 수: 2편

## 읽는 순서

- [10-session-and-jwt-entrypoints.md](10-session-and-jwt-entrypoints.md)
- [20-auth-boundary-and-test-closure.md](20-auth-boundary-and-test-closure.md)

## 근거 기준

- 소스코드, README, docs, 테스트, CLI만 입력 근거로 사용했다.
- 기존 blog 초안과 `_legacy` 본문은 입력 근거로 사용하지 않았다.
