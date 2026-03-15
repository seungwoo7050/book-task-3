# 02-render-pipeline 답안지

이 문서는 문제지를 다시 넘기지 않고도 해답을 재구성할 수 있도록, 실제 구현 파일과 테스트만 기준으로 정리한 답안지다.

## 한 줄 해답

시작 위치의 구현을 완성해 @front-react/vdom-foundations의 VNode 구조를 그대로 사용한다, render phase 동안 DOM mutation을 하면 안 된다, keyed/unkeyed child diff를 모두 설명할 수 있어야 한다를 한 흐름으로 설명하고 검증한다. 핵심은 `diffProps`와 `isEmptyPropsPatch`, `diffChildrenByIndex` 흐름을 구현하고 테스트를 통과시키는 것이다.

## 문제를 푸는 핵심 전략

- @front-react/vdom-foundations의 VNode 구조를 그대로 사용한다.
- render phase 동안 DOM mutation을 하면 안 된다.
- keyed/unkeyed child diff를 모두 설명할 수 있어야 한다.
- 첫 진입점은 `../study/react-internals/02-render-pipeline/ts/src/diff.ts`이고, 여기서 `diffProps`와 `isEmptyPropsPatch` 흐름을 먼저 붙잡은 뒤 나머지 파일로 확장한다.

## 코드 워크스루

- `../study/react-internals/02-render-pipeline/ts/src/diff.ts`: `diffProps`, `isEmptyPropsPatch`, `diffChildrenByIndex`, `diffChildrenByKey`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/react-internals/02-render-pipeline/ts/src/fiber.ts`: `reconcileChildren`, `performUnitOfWork`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/react-internals/02-render-pipeline/ts/src/index.ts`: 핵심 구현을 담는 파일이다.
- `../study/react-internals/02-render-pipeline/ts/src/patch.ts`: `createDomTree`, `applyPatchAt`, `applyPatches`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/react-internals/02-render-pipeline/ts/src/scheduler.ts`: `nextUnitOfWork`, `wipRoot`, `currentRoot`, `deletions`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/react-internals/02-render-pipeline/ts/tests/diff.test.ts`: `diffProps`, `returns changed and removed props`, `diffChildren`가 통과 조건과 회귀 포인트를 잠근다.
- `../study/react-internals/02-render-pipeline/ts/tests/patch.test.ts`: `applyPatches`, `creates and removes DOM nodes according to patches`가 통과 조건과 회귀 포인트를 잠근다.
- `../study/react-internals/02-render-pipeline/ts/tests/scheduler.test.ts`: `scheduler`, `does not mutate the DOM during the render phase`, `commits the tree when flushSync completes all work`가 통과 조건과 회귀 포인트를 잠근다.

## 정답을 재구성하는 절차

1. `../study/react-internals/02-render-pipeline/ts/src/diff.ts`를 먼저 열어 입력과 상태 전이의 기준점을 잡는다.
2. `diffProps` 등이 요구하는 순서대로 핵심 상태 전이와 예외 흐름을 채운다.
3. `cd study && npm run verify --workspace @front-react/render-pipeline`를 실행해 결과를 잠그고, 필요하면 남은 검증 명령까지 이어서 돌린다.

## 검증과 실패 포인트

```bash
cd study && npm run verify --workspace @front-react/render-pipeline
```

```bash
cd /Users/woopinbell/work/book-task-3/front-react/study/react-internals/02-render-pipeline && npm run test -- --run
```

```bash
cd /Users/woopinbell/work/book-task-3/front-react/study/react-internals/02-render-pipeline && npm run verify
```

- 상위 카탈로그나 보조 문서만 보고 구현을 추측하지 않고, 지금 열어 둔 source/test를 정답 근거로 고정한다.
- `diffProps`와 `returns changed and removed props`가 잠근 상태 전이와 입력 계약을 빼먹지 않는다.
- 완성 직전에만 한 번 돌리지 말고, 상태 전이를 건드릴 때마다 `cd study && npm run verify --workspace @front-react/render-pipeline`로 회귀를 조기에 잡는다.

## 소스 근거

- `../study/react-internals/02-render-pipeline/ts/src/diff.ts`
- `../study/react-internals/02-render-pipeline/ts/src/fiber.ts`
- `../study/react-internals/02-render-pipeline/ts/src/index.ts`
- `../study/react-internals/02-render-pipeline/ts/src/patch.ts`
- `../study/react-internals/02-render-pipeline/ts/src/scheduler.ts`
- `../study/react-internals/02-render-pipeline/ts/tests/diff.test.ts`
- `../study/react-internals/02-render-pipeline/ts/tests/patch.test.ts`
- `../study/react-internals/02-render-pipeline/ts/tests/scheduler.test.ts`
- `../study/react-internals/02-render-pipeline/tsconfig.json`
- `../study/react-internals/02-render-pipeline/package.json`
