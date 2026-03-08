# 09-platform-capstone

- 상태: `verified`
- 구현 레인: `nestjs/`
- legacy 출처: `legacy/06-platform-capstone`

## 목표

REST, pipeline, auth, persistence, events, production readiness를
단일 NestJS 서비스에서 통합하고 규약 일치를 검증한다.

## 현재 상태

문제 자료, 구현 코드, 개념 문서를 옮겨왔다.
새 경로에서 다시 빌드와 테스트를 완료했다.

## 실행 명령

- `nestjs/`: `pnpm install && pnpm approve-builds && pnpm rebuild better-sqlite3 && pnpm run build && pnpm run test && pnpm run test:e2e`

## 검증 상태

- `nestjs/`: `pnpm run build && pnpm run test && pnpm run test:e2e`

## 설치 전 주의사항

capstone은 `better-sqlite3`를 사용하므로 native build 승인 절차가 필요할 수 있다.
[공통 복구 가이드](../docs/native-sqlite-recovery.md)를 먼저 확인한다.

권장 순서:

1. `pnpm install`
2. `pnpm approve-builds`
3. `pnpm rebuild better-sqlite3`
4. `pnpm run build`
5. `pnpm run test`

## 실패 시 복구 루트

- sqlite binding 오류가 나면 DB 계층부터 복구한다.
- 테스트 중 `tsconfig.base.json` 경로 오류가 나면 `tsconfig.json`의 `extends` 경로부터 본다.
- `pnpm approve-builds`가 비어 있으면 이미 승인된 상태일 수 있으므로 `pnpm rebuild better-sqlite3`와 `pnpm run build`부터 다시 실행한다.
