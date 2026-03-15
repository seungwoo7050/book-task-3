# 03-hooks-and-events 답안지

이 문서는 문제지를 다시 넘기지 않고도 해답을 재구성할 수 있도록, 실제 구현 파일과 테스트만 기준으로 정리한 답안지다.

## 한 줄 해답

시작 위치의 구현을 완성해 @front-react/render-pipeline의 diff/patch helper를 그대로 소비한다, hook order invariant를 지켜야 한다, delegated event는 runtime tree 메타데이터를 통해 처리해야 한다를 한 흐름으로 설명하고 검증한다. 핵심은 `currentRoot`와 `currentHookContext`, `normalizeChild` 흐름을 구현하고 테스트를 통과시키는 것이다.

## 문제를 푸는 핵심 전략

- @front-react/render-pipeline의 diff/patch helper를 그대로 소비한다.
- hook order invariant를 지켜야 한다.
- delegated event는 runtime tree 메타데이터를 통해 처리해야 한다.
- 첫 진입점은 `../study/react-internals/03-hooks-and-events/ts/src/index.ts`이고, 여기서 `currentRoot`와 `currentHookContext` 흐름을 먼저 붙잡은 뒤 나머지 파일로 확장한다.

## 코드 워크스루

- `../study/react-internals/03-hooks-and-events/ts/src/index.ts`: 핵심 구현을 담는 파일이다.
- `../study/react-internals/03-hooks-and-events/ts/src/runtime.ts`: `currentRoot`, `currentHookContext`, `normalizeChild`, `splitProps`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/react-internals/03-hooks-and-events/ts/src/types.ts`: 핵심 구현을 담는 파일이다.
- `../study/react-internals/03-hooks-and-events/ts/tests/effect.test.ts`: `useEffect`, `runs effects after commit and cleans them up before the next effect`, `runs cleanup when a component unmounts`가 통과 조건과 회귀 포인트를 잠근다.
- `../study/react-internals/03-hooks-and-events/ts/tests/events.test.ts`: `delegated events`, `bubbles delegated events through the runtime tree`, `supports stopPropagation on delegated events`가 통과 조건과 회귀 포인트를 잠근다.
- `../study/react-internals/03-hooks-and-events/ts/tests/integration.test.ts`: `runtime integration`, `keeps event updates and effect timing in one runtime flow`가 통과 조건과 회귀 포인트를 잠근다.
- `../study/react-internals/03-hooks-and-events/tsconfig.json`: 입력 fixture나 계약 데이터를 고정하는 근거 파일이다.
- `../study/react-internals/03-hooks-and-events/package.json`: 실행 명령과 검증 경로를 고정하는 설정 파일이다.

## 정답을 재구성하는 절차

1. `../study/react-internals/03-hooks-and-events/ts/src/index.ts`를 먼저 열어 입력과 상태 전이의 기준점을 잡는다.
2. `useEffect` 등이 요구하는 순서대로 핵심 상태 전이와 예외 흐름을 채운다.
3. `cd study && npm run verify --workspace @front-react/hooks-and-events`를 실행해 결과를 잠그고, 필요하면 남은 검증 명령까지 이어서 돌린다.

## 검증과 실패 포인트

```bash
cd study && npm run verify --workspace @front-react/hooks-and-events
```

```bash
cd /Users/woopinbell/work/book-task-3/front-react/study/react-internals/03-hooks-and-events && npm run test -- --run
```

```bash
cd /Users/woopinbell/work/book-task-3/front-react/study/react-internals/03-hooks-and-events && npm run verify
```

- 상위 카탈로그나 보조 문서만 보고 구현을 추측하지 않고, 지금 열어 둔 source/test를 정답 근거로 고정한다.
- `useEffect`와 `runs effects after commit and cleans them up before the next effect`가 잠근 상태 전이와 입력 계약을 빼먹지 않는다.
- 완성 직전에만 한 번 돌리지 말고, 상태 전이를 건드릴 때마다 `cd study && npm run verify --workspace @front-react/hooks-and-events`로 회귀를 조기에 잡는다.

## 소스 근거

- `../study/react-internals/03-hooks-and-events/ts/src/index.ts`
- `../study/react-internals/03-hooks-and-events/ts/src/runtime.ts`
- `../study/react-internals/03-hooks-and-events/ts/src/types.ts`
- `../study/react-internals/03-hooks-and-events/ts/tests/effect.test.ts`
- `../study/react-internals/03-hooks-and-events/ts/tests/events.test.ts`
- `../study/react-internals/03-hooks-and-events/ts/tests/integration.test.ts`
- `../study/react-internals/03-hooks-and-events/tsconfig.json`
- `../study/react-internals/03-hooks-and-events/package.json`
- `../study/react-internals/03-hooks-and-events/vitest.config.ts`
