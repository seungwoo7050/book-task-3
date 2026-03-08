# 07-domain-events

- 상태: `verified`
- 구현 레인: `express/`, `nestjs/`
- legacy 출처: `legacy/05-event-system`

## 목표

도메인 이벤트로 side effect를 서비스 본문에서 분리하고,
성공 경로와 실패 경로의 이벤트 경계를 테스트로 고정한다.

## 현재 상태

원본 구현을 옮긴 뒤 새 경로에서 두 구현 모두 다시 검증했다.

## 실행 명령

- `express/`: `pnpm install && pnpm approve-builds && pnpm rebuild better-sqlite3 && pnpm run build && pnpm run test && pnpm run test:e2e`
- `nestjs/`: `pnpm install && pnpm approve-builds && pnpm rebuild better-sqlite3 && pnpm run build && pnpm run test && pnpm run test:e2e`

## 검증 상태

- `express/`: `pnpm run build && pnpm run test && pnpm run test:e2e`
- `nestjs/`: `pnpm run build && pnpm run test && pnpm run test:e2e`

## 설치 전 주의사항

이 프로젝트는 이벤트 예제를 SQLite 영속 계층 위에 올려 두었기 때문에
`better-sqlite3` native build 승인이 필요하다.
[공통 복구 가이드](../docs/native-sqlite-recovery.md)를 먼저 확인한다.

권장 순서:

1. `pnpm install`
2. `pnpm approve-builds`
3. `pnpm rebuild better-sqlite3`
4. `pnpm run build`
5. `pnpm run test`

## 실패 시 복구 루트

- sqlite binding 오류가 나면 DB 의존성부터 복구한다.
- 이벤트 테스트가 실패하면 발행 시점과 리스너 등록/정리 로직을 확인한다.
- `pnpm approve-builds`가 비어 있으면 승인 상태를 이미 통과한 경우가 있으므로 `pnpm rebuild better-sqlite3`를 먼저 다시 실행한다.
