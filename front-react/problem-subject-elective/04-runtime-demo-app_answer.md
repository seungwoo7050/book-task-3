# 04-runtime-demo-app 답안지

이 문서는 문제지를 다시 넘기지 않고도 해답을 재구성할 수 있도록, 실제 구현 파일과 테스트만 기준으로 정리한 답안지다.

## 한 줄 해답

시작 위치의 구현을 완성해 runtime 코드를 복사하지 않고 @front-react/hooks-and-events를 직접 소비해야 한다, debounced search와 pagination이 같은 UI에서 함께 동작해야 한다, metrics는 학습용 관찰값으로만 다루고 production profiler처럼 주장하지 않는다를 한 흐름으로 설명하고 검증한다. 핵심은 `PAGE_SIZE`와 `DEBOUNCE_MS`, `useDebouncedValue` 흐름을 구현하고 테스트를 통과시키는 것이다.

## 문제를 푸는 핵심 전략

- runtime 코드를 복사하지 않고 @front-react/hooks-and-events를 직접 소비해야 한다.
- debounced search와 pagination이 같은 UI에서 함께 동작해야 한다.
- metrics는 학습용 관찰값으로만 다루고 production profiler처럼 주장하지 않는다.
- 첫 진입점은 `../study/react-internals/04-runtime-demo-app/ts/src/app.ts`이고, 여기서 `PAGE_SIZE`와 `DEBOUNCE_MS` 흐름을 먼저 붙잡은 뒤 나머지 파일로 확장한다.

## 코드 워크스루

- `../study/react-internals/04-runtime-demo-app/ts/src/app.ts`: `PAGE_SIZE`, `DEBOUNCE_MS`, `useDebouncedValue`, `updateMetrics`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/react-internals/04-runtime-demo-app/ts/src/data.ts`: `DEMO_ITEMS`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/react-internals/04-runtime-demo-app/ts/src/main.ts`: `container`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/react-internals/04-runtime-demo-app/ts/tests/demo.test.ts`: `runtime demo app`, `filters results after the debounce window and updates metrics`, `loads the next page of results and updates visible metrics`가 통과 조건과 회귀 포인트를 잠근다.
- `../study/react-internals/04-runtime-demo-app/tsconfig.json`: 입력 fixture나 계약 데이터를 고정하는 근거 파일이다.
- `../study/react-internals/04-runtime-demo-app/package.json`: 실행 명령과 검증 경로를 고정하는 설정 파일이다.
- `../study/react-internals/04-runtime-demo-app/vite.config.ts`: 실행 명령과 검증 경로를 고정하는 설정 파일이다.
- `PAGE_SIZE` 구현은 `runtime demo app` 등이 잠근 입력 계약과 상태 전이를 그대로 만족해야 한다.

## 정답을 재구성하는 절차

1. `../study/react-internals/04-runtime-demo-app/ts/src/app.ts`를 먼저 열어 입력과 상태 전이의 기준점을 잡는다.
2. `runtime demo app` 등이 요구하는 순서대로 핵심 상태 전이와 예외 흐름을 채운다.
3. `cd study && npm run verify --workspace @front-react/runtime-demo-app`를 실행해 결과를 잠그고, 필요하면 남은 검증 명령까지 이어서 돌린다.

## 검증과 실패 포인트

```bash
cd study && npm run verify --workspace @front-react/runtime-demo-app
```

```bash
cd /Users/woopinbell/work/book-task-3/front-react/study/react-internals/04-runtime-demo-app && npm run test -- --run
```

```bash
cd /Users/woopinbell/work/book-task-3/front-react/study/react-internals/04-runtime-demo-app && npm run verify
```

- 상위 카탈로그나 보조 문서만 보고 구현을 추측하지 않고, 지금 열어 둔 source/test를 정답 근거로 고정한다.
- `runtime demo app`와 `filters results after the debounce window and updates metrics`가 잠근 상태 전이와 입력 계약을 빼먹지 않는다.
- 완성 직전에만 한 번 돌리지 말고, 상태 전이를 건드릴 때마다 `cd study && npm run verify --workspace @front-react/runtime-demo-app`로 회귀를 조기에 잡는다.

## 소스 근거

- `../study/react-internals/04-runtime-demo-app/ts/src/app.ts`
- `../study/react-internals/04-runtime-demo-app/ts/src/data.ts`
- `../study/react-internals/04-runtime-demo-app/ts/src/main.ts`
- `../study/react-internals/04-runtime-demo-app/ts/tests/demo.test.ts`
- `../study/react-internals/04-runtime-demo-app/tsconfig.json`
- `../study/react-internals/04-runtime-demo-app/package.json`
- `../study/react-internals/04-runtime-demo-app/vite.config.ts`
