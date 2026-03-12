# 07-domain-events

- 그룹: `Core`
- 상태: `verified`
- 공개 답안 레인: `express/`, `nestjs/`
- 성격: 초기 원본 이관 + 재검증

## 한 줄 문제

도메인 이벤트로 side effect를 서비스 본문에서 분리하고 성공/실패 경계를 테스트로 고정하는 이벤트 설계 문제다.

## 성공 기준

- 서비스 본문과 side effect를 도메인 이벤트 경계로 분리할 수 있다.
- 성공 경로에서만 발행되는 이벤트와 실패 시 발행되지 않는 이벤트를 테스트로 고정할 수 있다.
- Express와 NestJS에서 이벤트 리스너 등록 방식을 비교할 수 있다.

## 내가 만든 답

- 두 레인 모두 persistence 위에 이벤트 발행/구독 계층을 추가했다.
- 이벤트 발행 시점과 listener 정리 시점을 테스트로 묶어 부수효과의 경계를 드러냈다.
- SQLite native build 복구 절차는 공통 문서로 분리해 구현 README는 흐름만 남겼다.

## 제공 자료

- `problem/README.md`와 starter code
- `express/`
- `nestjs/`
- `docs/`
- `notion/`
- `../../docs/native-sqlite-recovery.md`

## 실행과 검증

### Express 레인
- 작업 디렉터리: `express/`
- install: `pnpm install && pnpm approve-builds && pnpm rebuild better-sqlite3`
- verify: `pnpm run build && pnpm run test && pnpm run test:e2e`
- run: `pnpm run dev`

### NestJS 레인
- 작업 디렉터리: `nestjs/`
- install: `pnpm install && pnpm approve-builds && pnpm rebuild better-sqlite3`
- verify: `pnpm run build && pnpm run test && pnpm run test:e2e`
- run: `pnpm run start:dev`

## 왜 다음 단계로 이어지는가

- `08-production-readiness`에서 기능 구현을 넘어 운영성 규약을 붙인다.
- canonical problem statement는 [problem/README.md](problem/README.md)에서, 구현별 실행 메모는 [express/README.md](express/README.md), [nestjs/README.md](nestjs/README.md)에서 확인한다.
