# 05-auth-and-authorization

- 상태: `verified`
- 구현 레인: `express/`, `nestjs/`
- legacy 출처: `legacy/02-auth-guards`

## 목표

JWT 인증과 RBAC 인가를 Express middleware chain과 NestJS guard chain으로 비교한다.

## 현재 상태

원본 문제 자료, 구현 코드, 개념 문서를 옮겨온 뒤
새 경로에서 두 구현 모두 다시 검증했다.

## 실행 명령

- `express/`: `pnpm install && pnpm run build && pnpm run test`
- `nestjs/`: `pnpm install && pnpm run build && pnpm run test`

## 검증 상태

- `express/`: `pnpm run build && pnpm run test`
- `nestjs/`: `pnpm run build && pnpm run test`

## 실패 시 복구 루트

- `TS4053` 또는 exported type 오류가 나면 controller public API가 서비스 내부 타입을 직접 노출하는지 확인한다.
- JWT 테스트가 실패하면 `auth.service.ts`, guard 체인, 비밀키 기본값을 먼저 확인한다.
