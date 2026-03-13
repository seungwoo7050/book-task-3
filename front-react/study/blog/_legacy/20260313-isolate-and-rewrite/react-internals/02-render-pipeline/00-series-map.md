# Series Map — 02 Render Pipeline

## 프로젝트 경계

- 트랙: `react-internals`
- 프로젝트 루트: `study/react-internals/02-render-pipeline`
- 독립 프로젝트 판정 근거: `README.md`, `problem/README.md`, `ts/README.md`, `npm run verify --workspace @front-react/render-pipeline`가 있고, diff/patch/scheduler 소스와 tests가 독립 경계를 이룬다.
- 기존 blog 처리: `isolate-and-rewrite`, 기존 `study/blog/react-internals/02-render-pipeline`는 없어서 새로 생성했다.

## source of truth

- 포함: 프로젝트 README, `problem/README.md`, `problem/original/README.md`, `docs/README.md`, `ts/README.md`, `ts/src/diff.ts`, `ts/src/patch.ts`, `ts/src/scheduler.ts`, `ts/tests/*`, `package.json`, `git log`, 2026-03-13 재검증 CLI
- 제외: `notion/**`, 이번 batch에서 생성한 `study/blog/**`

## chronology 복원 메모

- `46051f3`에서 diff/patch/scheduler와 tests가 한 번에 landing했고, `0e12fb8`에서 README/problem/docs가 render-vs-commit 언어로 정리됐다.
- chronology는 `diff scope -> patch ordering -> work loop/commit split -> verify` 순서로 읽는 편이 실제 코드 구조와 맞는다.
- 한 줄 답: 최소 DOM 변경 계산과 render/commit 분리를 구현한 fiber-like render pipeline 패키지다.

## canonical CLI

```bash
cd study
npm run verify --workspace @front-react/render-pipeline
```

## series

1. [01-evidence-ledger.md](01-evidence-ledger.md)
2. [02-structure.md](02-structure.md)
3. [10-development-timeline.md](10-development-timeline.md)
