# TypeScript 구현

상태: `verified`

## 이 구현이 답하는 범위

- tree diff and patch calculation
- keyed/unkeyed child diff
- render vs commit split
- cooperative work loop와 `flushSync`
- pipeline ordering tests

## 핵심 파일

- `src/diff.ts`: prop delta와 child diff
- `src/patch.ts`: DOM patch 적용 순서
- `src/scheduler.ts`: render phase, interrupted work, commit 시점

## 실행과 검증

```bash
cd study
npm run test --workspace @front-react/render-pipeline
npm run typecheck --workspace @front-react/render-pipeline
npm run verify --workspace @front-react/render-pipeline
```

## 현재 한계

- function component와 hook state는 아직 없다.
- event delegation은 아직 없다.
- 실제 React의 우선순위/lanes 모델은 다루지 않는다.
