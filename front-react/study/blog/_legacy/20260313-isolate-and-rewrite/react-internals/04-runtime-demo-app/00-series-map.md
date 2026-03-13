# Series Map — 04 Runtime Demo App

## 프로젝트 경계

- 트랙: `react-internals`
- 프로젝트 루트: `study/react-internals/04-runtime-demo-app`
- 독립 프로젝트 판정 근거: `README.md`, `problem/README.md`, `ts/README.md`, `npm run verify --workspace @front-react/runtime-demo-app`가 있고, shared runtime consumer app 소스와 tests가 독립 경계를 이룬다.
- 기존 blog 처리: `isolate-and-rewrite`, 기존 `study/blog/react-internals/04-runtime-demo-app`는 없어서 새로 만들었다.

## source of truth

- 포함: 프로젝트 README, `problem/README.md`, `problem/original/README.md`, `docs/README.md`, `ts/README.md`, `ts/src/app.ts`, `ts/src/data.ts`, `ts/tests/demo.test.ts`, `package.json`, `git log`, 2026-03-13 재검증 CLI
- 제외: `notion/**`, 이번 batch에서 생성한 `study/blog/**`

## chronology 복원 메모

- 2026-03-08 `46051f3`에서 consumer app 소스와 tests가 함께 들어왔고, 2026-03-12 `0e12fb8`에서 README/problem/docs wording이 shared runtime 소비 관점으로 다듬어졌다.
- chronology는 `consumer app scope -> debounced search + metrics -> verify` 순서로 재구성했다.
- 한 줄 답: 직접 만든 runtime을 import해 debounced search, load-more, render metrics를 보여 주는 consumer app이다.

## canonical CLI

```bash
cd study
npm run verify --workspace @front-react/runtime-demo-app
```

## series

1. [01-evidence-ledger.md](01-evidence-ledger.md)
2. [02-structure.md](02-structure.md)
3. [10-development-timeline.md](10-development-timeline.md)
