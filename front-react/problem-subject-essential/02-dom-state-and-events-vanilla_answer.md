# 02-dom-state-and-events-vanilla 답안지

이 문서는 문제지를 다시 넘기지 않고도 해답을 재구성할 수 있도록, 실제 구현 파일과 테스트만 기준으로 정리한 답안지다.

## 한 줄 해답

시작 위치의 구현을 완성해 React 없이 vanilla DOM에서 상태와 이벤트를 직접 관리한다, query state와 local UI state의 경계를 분리해야 한다, rerender 뒤에도 핵심 keyboard 흐름이 유지되어야 한다를 한 흐름으로 설명하고 검증한다. 핵심은 `syncUrl`와 `getSelectedItem`, `getMarkup` 흐름을 구현하고 테스트를 통과시키는 것이다.

## 문제를 푸는 핵심 전략

- React 없이 vanilla DOM에서 상태와 이벤트를 직접 관리한다.
- query state와 local UI state의 경계를 분리해야 한다.
- rerender 뒤에도 핵심 keyboard 흐름이 유지되어야 한다.
- 첫 진입점은 `../study/frontend-foundations/02-dom-state-and-events/vanilla/src/app.ts`이고, 여기서 `syncUrl`와 `getSelectedItem` 흐름을 먼저 붙잡은 뒤 나머지 파일로 확장한다.

## 코드 워크스루

- `../study/frontend-foundations/02-dom-state-and-events/vanilla/src/app.ts`: `syncUrl`, `getSelectedItem`, `getMarkup`, `mountBoard`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/frontend-foundations/02-dom-state-and-events/vanilla/src/data.ts`: `DEFAULT_ITEMS`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/frontend-foundations/02-dom-state-and-events/vanilla/src/main.ts`: `container`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/frontend-foundations/02-dom-state-and-events/vanilla/src/state.ts`: `STORAGE_KEY`, `DEFAULT_QUERY`, `cloneItems`, `parseQuery`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/frontend-foundations/02-dom-state-and-events/vanilla/src/types.ts`: 핵심 구현을 담는 파일이다.
- `../study/frontend-foundations/02-dom-state-and-events/vanilla/tests/board.spec.ts`: `syncs filters to URL and persists edits across reload`, `supports keyboard selection and inline edit submission`가 통과 조건과 회귀 포인트를 잠근다.
- `../study/frontend-foundations/02-dom-state-and-events/vanilla/tests/shell.test.ts`: `mountBoard`, `syncs search and filters to the URL`, `uses delegated click actions for selection and editing`가 통과 조건과 회귀 포인트를 잠근다.
- `../study/frontend-foundations/02-dom-state-and-events/vanilla/tests/state.test.ts`: `query helpers`, `parses known query values`, `serializes only meaningful values`가 통과 조건과 회귀 포인트를 잠근다.

## 정답을 재구성하는 절차

1. `../study/frontend-foundations/02-dom-state-and-events/vanilla/src/app.ts`를 먼저 열어 입력과 상태 전이의 기준점을 잡는다.
2. `syncs filters to URL and persists edits across reload` 등이 요구하는 순서대로 핵심 상태 전이와 예외 흐름을 채운다.
3. `cd study && npm run verify --workspace @front-react/dom-state-and-events`를 실행해 결과를 잠그고, 필요하면 남은 검증 명령까지 이어서 돌린다.

## 검증과 실패 포인트

```bash
cd study && npm run verify --workspace @front-react/dom-state-and-events
```

- 상위 카탈로그나 보조 문서만 보고 구현을 추측하지 않고, 지금 열어 둔 source/test를 정답 근거로 고정한다.
- `syncs filters to URL and persists edits across reload`와 `supports keyboard selection and inline edit submission`가 잠근 상태 전이와 입력 계약을 빼먹지 않는다.
- 완성 직전에만 한 번 돌리지 말고, 상태 전이를 건드릴 때마다 `cd study && npm run verify --workspace @front-react/dom-state-and-events`로 회귀를 조기에 잡는다.

## 소스 근거

- `../study/frontend-foundations/02-dom-state-and-events/vanilla/src/app.ts`
- `../study/frontend-foundations/02-dom-state-and-events/vanilla/src/data.ts`
- `../study/frontend-foundations/02-dom-state-and-events/vanilla/src/main.ts`
- `../study/frontend-foundations/02-dom-state-and-events/vanilla/src/state.ts`
- `../study/frontend-foundations/02-dom-state-and-events/vanilla/src/types.ts`
- `../study/frontend-foundations/02-dom-state-and-events/vanilla/tests/board.spec.ts`
- `../study/frontend-foundations/02-dom-state-and-events/vanilla/tests/shell.test.ts`
- `../study/frontend-foundations/02-dom-state-and-events/vanilla/tests/state.test.ts`
