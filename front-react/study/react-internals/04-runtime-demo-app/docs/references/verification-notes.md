# Verification Notes

## Command

```bash
cd study
npm run verify --workspace @front-react/runtime-demo-app
```

## What Is Verified

- debounced search가 timer cleanup 이후 최신 query만 반영하는지
- load more interaction이 visible window와 metrics를 같이 갱신하는지
- render metrics panel이 여러 상호작용 뒤에도 유지되는지

## Notes

- 이 단계의 검증은 학습용 integration에 집중한다.
- runtime 자체의 correctness는 `03-hooks-and-events` 검증 체인에 의존한다.
