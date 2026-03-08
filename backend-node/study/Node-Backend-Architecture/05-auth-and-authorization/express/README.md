# Express Implementation

## 문제 범위

JWT와 role middleware를 사용해 보호된 CRUD API를 구현한다.

## 실행

- install: `pnpm install`
- build: `pnpm run build`
- test: `pnpm run test`

## 현재 상태

- 상태: `verified`
- 원본: `legacy/02-auth-guards/express-impl/solve/solution`
- 새 경로 검증: 완료

## 실패 시 복구 루트

- `jsonwebtoken` 관련 실패가 나면 토큰 생성과 검증 시 사용하는 secret이 일치하는지 확인한다.
- 비밀번호 검증 실패가 나면 `bcryptjs` 해시 생성과 비교 시점을 먼저 본다.
