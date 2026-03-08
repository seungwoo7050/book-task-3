# NestJS Implementation

## 문제 범위

하나의 NestJS 서비스에 auth, books, events, persistence, pipeline 구성을 통합한다.

## 실행

- install: `pnpm install`
- approve native build: `pnpm approve-builds`
- rebuild sqlite binding: `pnpm rebuild better-sqlite3`
- build: `pnpm run build`
- test: `pnpm run test`
- test-e2e: `pnpm run test:e2e`

## 현재 상태

- 상태: `verified`
- 원본: `legacy/06-platform-capstone/solve/solution`
- 새 경로 검증: 완료

## 환경 제약

- 지원 환경: macOS, Ubuntu
- 런타임: Node.js 20+
- 패키지 매니저: pnpm 9+
- `better-sqlite3` native build 승인 필요
- 공통 가이드: [native-sqlite-recovery.md](../../docs/native-sqlite-recovery.md)

## 실패 시 복구 루트

- sqlite binding 오류가 나면 `pnpm approve-builds`와 `pnpm rebuild better-sqlite3`를 먼저 실행한다.
- strict TypeScript 오류가 나면 entity와 DTO의 definite assignment, `tsconfig.base.json` 경로, `node:crypto` import 방식을 순서대로 확인한다.
