# TypeScript Implementation

상태: `verified`

구현 범위:

- tree diff and patch calculation
- keyed/unkeyed child diff
- render vs commit split
- cooperative work loop와 `flushSync`
- pipeline ordering tests

## Build Command

```bash
cd study/react-internals/02-render-pipeline
npm install
```

## Test Command

```bash
cd study
npm run verify --workspace @front-react/render-pipeline
```

## Known Gaps

- function component와 hook state는 아직 없다
- event delegation은 아직 없다
- 실제 React의 우선순위/lanes 모델은 다루지 않는다

이 단계는 `01-vdom-foundations`의 VNode 구조를 유지하면서 업데이트 파이프라인을 분리하는 것이 핵심이다.
