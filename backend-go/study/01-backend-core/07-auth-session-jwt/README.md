# 07 Auth Session JWT

## 한 줄 요약

session login과 JWT login을 함께 구현해 인증 방식과 인가 경계를 비교하는 브리지 과제다.

## 이 프로젝트가 푸는 문제

- cookie session과 bearer JWT를 둘 다 경험해야 한다.
- 비밀번호 저장, 보호 리소스 접근, 401/403 구분을 손으로 구현해야 한다.
- authentication과 authorization을 분리해 설명할 수 있어야 한다.

## 내가 만든 답

- session login, JWT login, role-based authorization 예제를 `solution/go`에 구현했다.
- 비밀번호는 해시로 저장하고 보호 리소스에서 인증/인가 실패를 구분한다.
- refresh token과 외부 user store는 의도적으로 제외해 핵심 비교만 남겼다.

## 핵심 설계 선택

- session과 JWT를 같은 프로젝트에 두어 저장 위치와 검증 흐름 차이를 직접 비교하게 했다.
- 권한 실패와 인증 실패를 응답 코드로 분리해 이후 RBAC 과제로 이어지게 했다.

## 검증

- `cd solution/go && go run ./cmd/server`
- `cd solution/go && go test ./...`

## 제외 범위

- refresh token
- 외부 사용자 저장소

## 읽는 순서

1. [problem/README.md](problem/README.md)에서 canonical 문제 정의와 성공 기준을 읽는다.
2. [solution/README.md](solution/README.md)에서 구현 범위와 검증 진입점을 확인한다.
3. [docs/README.md](docs/README.md)에서 개념 설명과 참고 문서를 따라간다.
4. [notion/README.md](notion/README.md)에서 접근 로그, 디버그 기록, 회고를 확인한다.

## 상태

- 상태: `verified`
- 제공 자료와 provenance: `study`에서 새로 추가한 브리지 과제
