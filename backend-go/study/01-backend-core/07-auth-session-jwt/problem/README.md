# 문제 정의

세션 로그인과 JWT 로그인을 모두 제공하는 작은 인증 서버를 만든다.

## 성공 기준

- 비밀번호는 평문으로 저장하지 않는다.
- 세션 로그인 후 보호 리소스 접근이 가능해야 한다.
- JWT 로그인 후 보호 리소스 접근이 가능해야 한다.
- 권한 부족은 `403`, 인증 실패는 `401`을 반환한다.

## 제공 자료와 출처

- `study`에서 새로 설계한 브리지 과제다.
- 이 문서가 공개용 canonical 문제 정의다.
- 공개 구현은 [`solution/README.md`](../solution/README.md)와 `solution/go`에 둔다.

## 검증 기준

- `cd solution/go && go run ./cmd/server`
- `cd solution/go && go test ./...`

## 제외 범위

- refresh token rotation
- 외부 IdP 연동
