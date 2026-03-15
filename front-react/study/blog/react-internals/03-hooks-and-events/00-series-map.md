# 03 Hooks And Events

이 프로젝트의 핵심은 `useState`, `useEffect`, delegated event를 각각 흉내 냈다는 데 있지 않다. 더 중요한 건 세 가지를 같은 runtime loop 안에서 돌리면서, 상태 변경이 rerender와 effect timing, 그리고 이벤트 bubbling으로 어떻게 이어지는지를 한 규칙 집합으로 묶었다는 점이다. 이번 Todo에서는 hook slot index invariant, effect cleanup ordering, root-level delegation, single-root runtime 경계를 중심으로 다시 정리했다.

## 왜 이 순서로 읽는가

구현 중심이 거의 [`runtime.ts`](/Users/woopinbell/work/book-task-3/front-react/study/react-internals/03-hooks-and-events/ts/src/runtime.ts) 한 파일에 모여 있다. child normalization, function component execution, hook slot 저장, effect scheduling, DOM metadata 동기화, delegated dispatch가 모두 여기서 이어진다. 그래서 이 프로젝트도 `series map + 본문 1편` 구조가 가장 자연스럽다.

## 이번 재작성의 근거

- `react-internals/03-hooks-and-events/problem/README.md`
- `react-internals/03-hooks-and-events/docs/README.md`
- `react-internals/03-hooks-and-events/ts/README.md`
- `react-internals/03-hooks-and-events/ts/src/runtime.ts`
- `react-internals/03-hooks-and-events/ts/tests/state.test.ts`
- `react-internals/03-hooks-and-events/ts/tests/effect.test.ts`
- `react-internals/03-hooks-and-events/ts/tests/events.test.ts`
- `react-internals/03-hooks-and-events/ts/tests/integration.test.ts`

## 현재 검증 상태

```bash
npm run verify --workspace @front-react/hooks-and-events
```

- 2026-03-14 재실행 기준 `vitest` 7개 테스트 통과
- `tsc --noEmit` typecheck 통과
- verify 전체 통과

## 본문

- [10-hook-slots-effects-and-delegation-in-one-runtime.md](10-hook-slots-effects-and-delegation-in-one-runtime.md)
  - hook slot 저장, effect cleanup, delegated bubbling이 한 runtime에서 어떻게 이어지는지 따라간다.

## 이번에 명시적으로 남긴 경계

- hook identity는 call order index에 의존한다.
- runtime은 사실상 single root 모델이며 다른 container를 렌더하면 이전 root를 정리한다.
- delegated event는 `onClick` 같은 bubble-phase handler를 root listener 하나로 모으는 최소 모델이다. capture/options/full synthetic event semantics는 아직 없다.
- `useMemo`, `useReducer`, `context`, full synthetic event 호환성은 아직 없다.
