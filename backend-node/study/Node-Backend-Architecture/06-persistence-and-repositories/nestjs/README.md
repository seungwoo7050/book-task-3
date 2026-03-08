# NestJS Implementation

## 문제 범위

TypeORM repository를 사용해 CRUD API를 영속화한다.

## 실행

- install: `pnpm install`
- approve native build: `pnpm approve-builds`
- rebuild sqlite binding: `pnpm rebuild better-sqlite3`
- build: `pnpm run build`
- test: `pnpm run test`
- test-e2e: `pnpm run test:e2e`

## 현재 상태

- 상태: `verified`
- 원본: `legacy/04-database/nestjs-impl/solve/solution`
- 새 경로 검증: 완료

## 환경 제약

- 지원 환경: macOS, Ubuntu
- 런타임: Node.js 20+
- 패키지 매니저: pnpm 9+
- `better-sqlite3` native build 승인 필요
- 공통 가이드: [native-sqlite-recovery.md](../../docs/native-sqlite-recovery.md)

## 실패 시 복구 루트

- TypeORM 초기화 단계에서 `Could not locate the bindings file`가 나오면 sqlite native build가 빠진 것이다.
- `pnpm approve-builds`와 `pnpm rebuild better-sqlite3`를 먼저 실행한다.
- `pnpm approve-builds` 결과가 비어 있으면 `pnpm rebuild better-sqlite3`와 `pnpm run build`를 다시 실행해 binding 복구 여부를 먼저 확인한다.
