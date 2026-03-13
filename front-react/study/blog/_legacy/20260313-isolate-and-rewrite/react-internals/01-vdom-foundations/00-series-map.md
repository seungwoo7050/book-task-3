# Series Map — 01 VDOM Foundations

## 프로젝트 경계

- 트랙: `react-internals`
- 프로젝트 루트: `study/react-internals/01-vdom-foundations`
- 독립 프로젝트 판정 근거: 자체 `README.md`, `problem/README.md`, `ts/README.md`, `npm run verify --workspace @front-react/vdom-foundations`가 있고, `ts/src/*`와 `ts/tests/*`가 다른 프로젝트와 분리된 패키지 경계를 가진다.
- 기존 blog 처리: `isolate-and-rewrite`, 기존 `study/blog/react-internals/01-vdom-foundations`는 없어서 새로 만들었다.

## source of truth

- 포함: 프로젝트 README, `problem/README.md`, `problem/original/README.md`, `docs/README.md`, `ts/README.md`, `ts/src/element.ts`, `ts/src/dom-utils.ts`, `ts/tests/*`, `package.json`, `git log`, 2026-03-13 재검증 CLI
- 제외: `notion/**`, 이번 batch에서 생성한 `study/blog/**`

## chronology 복원 메모

- `46051f3`(2026-03-08)에서 adapted problem surface, TypeScript 구현, tests가 함께 landing했고, `0e12fb8`(2026-03-12)에서 README/problem/docs 표현이 정리됐다.
- VDOM foundational code는 `VNode shape -> DOM reflection -> package contract -> verify` 순서로 읽는 편이 실제 구현 의도와 잘 맞는다.
- 한 줄 답: JSX-like 호출을 `VNode`와 DOM reflection으로 바꾸는 최소 Virtual DOM 패키지다.

## canonical CLI

```bash
cd study
npm run verify --workspace @front-react/vdom-foundations
```

## series

1. [01-evidence-ledger.md](01-evidence-ledger.md)
2. [02-structure.md](02-structure.md)
3. [10-development-timeline.md](10-development-timeline.md)
