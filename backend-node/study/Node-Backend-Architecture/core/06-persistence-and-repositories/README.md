# 06-persistence-and-repositories

- 그룹: `Core`
- 상태: `verified`
- 공개 답안 레인: `express/`, `nestjs/`
- 성격: 초기 원본 이관 + 재검증

## 한 줄 문제

in-memory 저장소를 SQLite 기반 영속 계층으로 교체하면서 raw SQL과 ORM, repository 패턴의 차이를 비교하는 문제다.

## 성공 기준

- API 계약을 유지한 채 저장 계층을 메모리에서 SQLite로 교체할 수 있다.
- raw SQL과 ORM, custom repository와 framework repository의 차이를 설명할 수 있다.
- 테스트 격리와 DB 초기화 전략을 재현할 수 있다.

## 내가 만든 답

- `express/`에서는 raw SQL 기반 repository 패턴을, `nestjs/`에서는 ORM 기반 영속 계층을 구현했다.
- native dependency가 필요한 `better-sqlite3` 복구 절차를 트랙 공통 문서로 분리했다.
- API 계층은 크게 바꾸지 않고 저장 전략만 교체해 경계 유지의 의미를 보여 준다.

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

- `07-domain-events`에서 영속 계층 위에 도메인 이벤트와 side effect 분리를 올린다.
- canonical problem statement는 [problem/README.md](problem/README.md)에서, 구현별 실행 메모는 [express/README.md](express/README.md), [nestjs/README.md](nestjs/README.md)에서 확인한다.
