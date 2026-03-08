# NestJS Implementation

## 문제 범위

Passport JWT와 Guard 조합으로 인증과 인가를 구현한다.

## 실행

- install: `pnpm install`
- build: `pnpm run build`
- test: `pnpm run test`

## 현재 상태

- 상태: `verified`
- 원본: `legacy/02-auth-guards/nestjs-impl/solve/solution`
- 새 경로 검증: 완료

## 실패 시 복구 루트

- `TS4053`가 다시 나오면 public controller method가 서비스 내부 타입을 직접 반환하는지 확인한다.
- Guard 동작이 깨지면 `JwtAuthGuard`, `RolesGuard`, `@Roles()` 순서를 먼저 본다.
