# react-internals blog

`react-internals`는 JSX -> VDOM -> render pipeline -> hooks/events -> consumer app 흐름을 네 단계로 압축한 트랙이다. 이 blog 레이어는 commit 단위보다 개념 경계가 더 크게 묶여 있는 경로를 `problem`, `ts/src`, `ts/tests`, typecheck/verify 출력으로 다시 읽는다.

## 이 레이어가 쓰는 근거

- 프로젝트 README, `problem/README.md`, `ts/README.md`, `docs/README.md`
- `ts/src/*`, `ts/tests/*`, `package.json`, `vitest.config.ts`, `tsconfig.json`
- `git log --reverse --stat -- study/react-internals/<project>`
- 2026-03-13 재실행한 `npm run verify --workspace ...`

## 프로젝트 목록

| 프로젝트 | 최종 blog | evidence ledger | structure |
| --- | --- | --- | --- |
| VDOM Foundations | [01-vdom-foundations/10-development-timeline.md](01-vdom-foundations/10-development-timeline.md) | [01-evidence-ledger.md](01-vdom-foundations/01-evidence-ledger.md) | [02-structure.md](01-vdom-foundations/02-structure.md) |
| Render Pipeline | [02-render-pipeline/10-development-timeline.md](02-render-pipeline/10-development-timeline.md) | [01-evidence-ledger.md](02-render-pipeline/01-evidence-ledger.md) | [02-structure.md](02-render-pipeline/02-structure.md) |
| Hooks and Events | [03-hooks-and-events/10-development-timeline.md](03-hooks-and-events/10-development-timeline.md) | [01-evidence-ledger.md](03-hooks-and-events/01-evidence-ledger.md) | [02-structure.md](03-hooks-and-events/02-structure.md) |
| Runtime Demo App | [04-runtime-demo-app/10-development-timeline.md](04-runtime-demo-app/10-development-timeline.md) | [01-evidence-ledger.md](04-runtime-demo-app/01-evidence-ledger.md) | [02-structure.md](04-runtime-demo-app/02-structure.md) |
