# Verification Notes

## Command

```bash
cd study
npm run verify --workspace @front-react/hooks-and-events
```

## What Is Verified

- `state.test.ts`
  - state update 이후 rerender
  - hook count change invariant
- `effect.test.ts`
  - effect setup / cleanup ordering
  - unmount cleanup
- `events.test.ts`
  - delegated bubbling
  - `stopPropagation`
- `integration.test.ts`
  - event -> state update -> rerender -> effect 흐름

## Notes

- 이 runtime은 학습용 단일 root 모델이다.
- render/commit split은 이전 단계의 diff/patch helper를 그대로 사용한다.
