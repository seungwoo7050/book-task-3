# 06-persistence-and-repositories

- 상태: `verified`
- 구현 레인: `express/`, `nestjs/`
- legacy 출처: `legacy/04-database`

## 목표

in-memory 저장소를 SQLite 기반 영속 계층으로 교체하면서
API 계약을 유지하는 법을 학습한다.

## 핵심 비교 축

- raw SQL vs ORM
- custom repository vs framework repository
- 테스트 격리와 DB 초기화 전략

## 현재 상태

원본 문제 자료, 구현 코드, 개념 문서를 옮겨온 뒤
새 경로에서 두 구현 모두 다시 검증했다.

## 실행 명령

- `express/`: `pnpm install && pnpm approve-builds && pnpm rebuild better-sqlite3 && pnpm run build && pnpm run test && pnpm run test:e2e`
- `nestjs/`: `pnpm install && pnpm approve-builds && pnpm rebuild better-sqlite3 && pnpm run build && pnpm run test && pnpm run test:e2e`

## 검증 상태

새 경로에서 두 구현 모두 다시 검증했다.

- `express/`: `pnpm run build && pnpm run test && pnpm run test:e2e`
- `nestjs/`: `pnpm run build && pnpm run test && pnpm run test:e2e`

## 설치 전 주의사항

이 프로젝트는 `better-sqlite3`를 사용한다.
일부 환경에서는 `pnpm install` 뒤에 native build 승인이 필요하다.
[공통 복구 가이드](../docs/native-sqlite-recovery.md)를 먼저 확인한다.

권장 순서:

1. `pnpm install`
2. `pnpm approve-builds`
3. `pnpm rebuild better-sqlite3`
4. `pnpm run build`
5. `pnpm run test`

## 실패 시 복구 루트

- `Could not locate the bindings file`가 나오면 `better-sqlite3` native build가 승인되지 않은 것이다.
- `pnpm approve-builds` 후 `pnpm rebuild better-sqlite3`를 다시 실행한다.
- `pnpm approve-builds`에서 승인할 항목이 없으면 이미 승인된 상태일 수 있으므로 `pnpm rebuild better-sqlite3`부터 다시 실행한다.
