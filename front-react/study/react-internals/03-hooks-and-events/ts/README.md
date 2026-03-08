# TypeScript Implementation

상태: `verified`

구현 범위:

- function component hook slots
- `useState` and `useEffect`
- cleanup lifecycle
- root event delegation
- runtime integration tests

## Build Command

```bash
cd study/react-internals/03-hooks-and-events
npm install
```

## Test Command

```bash
cd study
npm run verify --workspace @front-react/hooks-and-events
```

## Known Gaps

- `useMemo`, `useReducer`, `context`는 없다
- synthetic event 전체 호환성은 없다
- React의 scheduler / concurrent semantics 전체를 복제하지 않는다
