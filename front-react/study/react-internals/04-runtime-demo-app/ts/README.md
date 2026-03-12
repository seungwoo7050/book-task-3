# TypeScript 구현

상태: `verified`

## 이 구현이 답하는 범위

- shared runtime consumer app
- debounced search and load-more pagination demo
- render metrics
- integration scenario tests

## 핵심 파일

- `src/app.ts`: debounced search, visible window, metrics panel
- `src/data.ts`: demo dataset
- `tests/demo.test.ts`: debounce, pagination, metrics 검증

## 실행과 검증

```bash
cd study
npm run dev --workspace @front-react/runtime-demo-app
npm run verify --workspace @front-react/runtime-demo-app
```

## 현재 한계

- 실제 infinite scroll observer는 없다.
- metrics는 학습용 관찰값이지 production profiler가 아니다.
- 네트워크 계층이나 데이터 persistence는 없다.
