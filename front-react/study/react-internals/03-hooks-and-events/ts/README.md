# TypeScript 구현

상태: `verified`

## 이 구현이 답하는 범위

- function component hook slots
- `useState` and `useEffect`
- cleanup lifecycle
- root event delegation
- runtime integration tests

## 핵심 파일

- `src/runtime.ts`: hook slot 저장, effect cleanup, delegated event, runtime render
- `src/index.ts`: runtime public API export
- `tests/`: state, effect, event, integration 검증

## 실행과 검증

```bash
cd study
npm run test --workspace @front-react/hooks-and-events
npm run typecheck --workspace @front-react/hooks-and-events
npm run verify --workspace @front-react/hooks-and-events
```

## 현재 한계

- `useMemo`, `useReducer`, `context`는 없다.
- synthetic event 전체 호환성은 없다.
- React의 scheduler / concurrent semantics 전체를 복제하지 않는다.
