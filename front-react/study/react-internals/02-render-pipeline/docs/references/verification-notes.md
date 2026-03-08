# Verification Notes

## Command

```bash
cd study
npm run verify --workspace @front-react/render-pipeline
```

## What Is Verified

- `diff.test.ts`
  - prop delta 계산
  - keyed / unkeyed child diff
  - type change 시 replace patch
- `patch.test.ts`
  - create / remove patch가 DOM 트리를 올바르게 반영하는지 확인
- `scheduler.test.ts`
  - render phase에서는 DOM mutation이 없는지 확인
  - `flushSync()`로 전체 commit이 끝나는지 확인
  - interrupted work 이후 commit 결과가 일관적인지 확인

## Notes

- scheduler는 학습용 cooperative work loop다.
- 실제 React의 priority model과 concurrency semantics 전체를 재현하지 않는다.
