# Series Map — 03 Hooks And Events

## 프로젝트 경계

- 트랙: `react-internals`
- 프로젝트 루트: `study/react-internals/03-hooks-and-events`
- 독립 프로젝트 판정 근거: `README.md`, `problem/README.md`, `ts/README.md`, `npm run verify --workspace @front-react/hooks-and-events`가 있고, runtime 소스와 state/effect/event tests가 하나의 패키지 경계를 이룬다.
- 기존 blog 처리: `isolate-and-rewrite`, 기존 `study/blog/react-internals/03-hooks-and-events`는 없어서 새로 만들었다.

## source of truth

- 포함: 프로젝트 README, `problem/README.md`, `problem/original/README.md`, `docs/README.md`, `ts/README.md`, `ts/src/runtime.ts`, `ts/tests/*`, `package.json`, `git log`, 2026-03-13 재검증 CLI
- 제외: `notion/**`, 이번 batch에서 생성한 `study/blog/**`

## chronology 복원 메모

- 2026-03-08 `46051f3`가 runtime과 tests를 한 번에 넣었고, 2026-03-12 `0e12fb8`가 public docs 표현을 정리했다.
- 이 프로젝트는 한 파일(`runtime.ts`)에 많은 판단이 압축돼 있어, `runtime metadata -> delegated event -> hook slot/effect timing -> verify` 순서로 읽는 편이 좋다.
- 한 줄 답: `useState`, `useEffect`, delegated event를 하나의 runtime loop로 묶은 학습용 runtime 패키지다.

## canonical CLI

```bash
cd study
npm run verify --workspace @front-react/hooks-and-events
```

## series

1. [01-evidence-ledger.md](01-evidence-ledger.md)
2. [02-structure.md](02-structure.md)
3. [10-development-timeline.md](10-development-timeline.md)
