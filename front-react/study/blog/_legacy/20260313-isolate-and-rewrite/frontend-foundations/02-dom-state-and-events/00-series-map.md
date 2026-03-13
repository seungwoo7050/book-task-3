# Series Map — 02 DOM State And Events

## 프로젝트 경계

- 트랙: `frontend-foundations`
- 프로젝트 루트: `study/frontend-foundations/02-dom-state-and-events`
- 독립 프로젝트 판정 근거: `README.md`, `problem/README.md`, `vanilla/README.md`, `npm run verify --workspace @front-react/dom-state-and-events`가 있고, state/event 소스와 테스트가 별도 경계로 정리돼 있다.
- 기존 blog 처리: `isolate-and-rewrite`, 기존 `study/blog/frontend-foundations/02-dom-state-and-events`는 없어서 새로 생성했다.

## source of truth

- 포함: 프로젝트 README, `problem/README.md`, `docs/README.md`, `vanilla/README.md`, `vanilla/src/app.ts`, `vanilla/src/state.ts`, `vanilla/tests/*`, `package.json`, `git log`, 2026-03-13 재검증 CLI
- 제외: `notion/**`, 이번 batch에서 생성한 `study/blog/**`

## chronology 복원 메모

- `46051f3`(2026-03-08)에서 state helper, board UI, tests가 함께 들어왔고, `0e12fb8`(2026-03-12)에서 README/problem/docs contract가 정리됐다.
- 세부 순서는 commit보다 코드를 따라 보는 편이 더 정확해서, `query/persistence helper -> render loop + event delegation -> verify` 순서로 재구성했다.
- 한 줄 답: URL query, localStorage, selection, inline edit를 한 보드 안에서 동기화하는 vanilla state orchestration 프로젝트다.

## canonical CLI

```bash
cd study
npm run verify --workspace @front-react/dom-state-and-events
```

## series

1. [01-evidence-ledger.md](01-evidence-ledger.md)
2. [02-structure.md](02-structure.md)
3. [10-development-timeline.md](10-development-timeline.md)
