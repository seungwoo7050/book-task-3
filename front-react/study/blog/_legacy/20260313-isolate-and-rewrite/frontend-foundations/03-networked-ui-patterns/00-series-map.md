# Series Map — 03 Networked UI Patterns

## 프로젝트 경계

- 트랙: `frontend-foundations`
- 프로젝트 루트: `study/frontend-foundations/03-networked-ui-patterns`
- 독립 프로젝트 판정 근거: `README.md`, `problem/README.md`, `vanilla/README.md`, `npm run verify --workspace @front-react/networked-ui-patterns`가 있고, mock service/state/app/tests가 독립 경계로 정리되어 있다.
- 기존 blog 처리: `isolate-and-rewrite`, 기존 `study/blog/frontend-foundations/03-networked-ui-patterns`는 없어서 새로 생성했다.

## source of truth

- 포함: 프로젝트 README, `problem/README.md`, `docs/README.md`, `vanilla/README.md`, `vanilla/src/service.ts`, `vanilla/src/state.ts`, `vanilla/src/app.ts`, `vanilla/tests/*`, `package.json`, `git log`, 2026-03-13 재검증 CLI
- 제외: `notion/**`, 이번에 생성한 `study/blog/**`

## chronology 복원 메모

- 2026-03-08 `46051f3`에서 mock service, request tracker, explorer UI, tests가 함께 들어왔고, 2026-03-12 `0e12fb8`에서 README와 problem/docs contract가 정리됐다.
- core chronology는 `URL state + request tracker -> list/detail load split -> verify` 순서로 복원하는 편이 코드와 테스트 모두에 잘 맞는다.
- 한 줄 답: loading/empty/error/retry/abort/stale response를 explorer UI 하나에서 다루는 vanilla 비동기 상태 실습이다.

## canonical CLI

```bash
cd study
npm run verify --workspace @front-react/networked-ui-patterns
```

## series

1. [01-evidence-ledger.md](01-evidence-ledger.md)
2. [02-structure.md](02-structure.md)
3. [10-development-timeline.md](10-development-timeline.md)
