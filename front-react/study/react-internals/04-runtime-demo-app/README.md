# 04 Runtime Demo App

상태: `verified`

## 무슨 문제인가

직접 만든 runtime이 정말 앱 수준 상호작용을 견딜 수 있는지 보려면 소비자 앱이 필요하다. 이 단계는 shared runtime을 그대로 import해 debounced search, load more, render metrics를 갖춘 demo app을 만드는 문제를 푼다.

## 왜 필요한가

internals 학습은 실제 기능 조합 위에서 한계와 tradeoff를 확인할 때 더 설득력 있다. 이 단계는 직접 만든 runtime이 어디까지 설명 가능하고 어디서 멈추는지 보여 주는 마감 단계다.

## 내가 만든 답

`@front-react/hooks-and-events`를 소비하는 demo app을 만들고, 검색/페이지네이션 상호작용과 render metrics를 함께 노출했다.

- 문제 정의: [problem/README.md](problem/README.md)
- 구현 상세: [ts/README.md](ts/README.md)
- 공개 문서: [docs/README.md](docs/README.md)

## 핵심 구현 포인트

- `ts/src/app.ts`에서 `useDebouncedValue`, visible window, metrics panel을 한 앱 흐름으로 묶는다.
- `ts/src/data.ts`에서 검색/카테고리 시나리오에 맞는 demo dataset을 제공한다.
- `ts/tests/demo.test.ts`로 debounce, load more, metrics 유지 동작을 통합 검증한다.

## 검증

```bash
cd study
npm run dev --workspace @front-react/runtime-demo-app
npm run test --workspace @front-react/runtime-demo-app
npm run typecheck --workspace @front-react/runtime-demo-app
npm run verify --workspace @front-react/runtime-demo-app
```

- 검증 기준일: 2026-03-08
- `vitest`: `demo.test.ts`로 debounce, pagination, metrics 갱신 확인
- `typecheck`: `@front-react/runtime-demo-app` 패키지 타입 검사 통과

## 읽기 순서

1. [problem/README.md](problem/README.md)
2. [ts/README.md](ts/README.md)
3. [docs/README.md](docs/README.md)

## 한계

- 실제 infinite scroll observer, 네트워크 계층, persistence는 없다.
- metrics는 학습용 관찰값이지 production profiler가 아니다.
- 제품형 UI 신호는 다음 트랙인 `frontend-portfolio`가 이어받는다.
