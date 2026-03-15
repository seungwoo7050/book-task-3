# 03-networked-ui-patterns-vanilla 답안지

이 문서는 문제지를 다시 넘기지 않고도 해답을 재구성할 수 있도록, 실제 구현 파일과 테스트만 기준으로 정리한 답안지다.

## 한 줄 해답

시작 위치의 구현을 완성해 실제 서버 대신 mock API를 사용한다, request race와 abort를 무시하지 않고 명시적으로 처리해야 한다, URL query parameter만으로 탐색 상태를 복원할 수 있어야 한다를 한 흐름으로 설명하고 검증한다. 핵심은 `buildUrlState`와 `syncUrl`, `getMarkup` 흐름을 구현하고 테스트를 통과시키는 것이다.

## 문제를 푸는 핵심 전략

- 실제 서버 대신 mock API를 사용한다.
- request race와 abort를 무시하지 않고 명시적으로 처리해야 한다.
- URL query parameter만으로 탐색 상태를 복원할 수 있어야 한다.
- 첫 진입점은 `../study/frontend-foundations/03-networked-ui-patterns/vanilla/src/app.ts`이고, 여기서 `buildUrlState`와 `syncUrl` 흐름을 먼저 붙잡은 뒤 나머지 파일로 확장한다.

## 코드 워크스루

- `../study/frontend-foundations/03-networked-ui-patterns/vanilla/src/app.ts`: `buildUrlState`, `syncUrl`, `getMarkup`, `mountDirectoryExplorer`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/frontend-foundations/03-networked-ui-patterns/vanilla/src/data.ts`: `DIRECTORY_ITEMS`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/frontend-foundations/03-networked-ui-patterns/vanilla/src/main.ts`: `container`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/frontend-foundations/03-networked-ui-patterns/vanilla/src/service.ts`: `wait`, `filterItems`, `explorerService`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/frontend-foundations/03-networked-ui-patterns/vanilla/src/state.ts`: `DEFAULT_QUERY`, `parseUrlState`, `serializeUrlState`, `createRequestTracker`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/frontend-foundations/03-networked-ui-patterns/vanilla/tests/explorer.spec.ts`: `updates query params and loads detail from the directory list`, `recovers from a simulated failure and keeps keyboard navigation viable`가 통과 조건과 회귀 포인트를 잠근다.
- `../study/frontend-foundations/03-networked-ui-patterns/vanilla/tests/explorer.test.ts`: `createMockService`, `mountDirectoryExplorer`, `syncs search to the URL and loads detail`가 통과 조건과 회귀 포인트를 잠근다.
- `../study/frontend-foundations/03-networked-ui-patterns/vanilla/tests/service.test.ts`: `explorerService`, `rejects with AbortError when list requests are aborted`, `tracks only the latest token for race-aware updates`가 통과 조건과 회귀 포인트를 잠근다.

## 정답을 재구성하는 절차

1. `../study/frontend-foundations/03-networked-ui-patterns/vanilla/src/app.ts`를 먼저 열어 입력과 상태 전이의 기준점을 잡는다.
2. `updates query params and loads detail from the directory list` 등이 요구하는 순서대로 핵심 상태 전이와 예외 흐름을 채운다.
3. `cd study && npm run verify --workspace @front-react/networked-ui-patterns`를 실행해 결과를 잠그고, 필요하면 남은 검증 명령까지 이어서 돌린다.

## 검증과 실패 포인트

```bash
cd study && npm run verify --workspace @front-react/networked-ui-patterns
```

- 상위 카탈로그나 보조 문서만 보고 구현을 추측하지 않고, 지금 열어 둔 source/test를 정답 근거로 고정한다.
- `updates query params and loads detail from the directory list`와 `recovers from a simulated failure and keeps keyboard navigation viable`가 잠근 상태 전이와 입력 계약을 빼먹지 않는다.
- 완성 직전에만 한 번 돌리지 말고, 상태 전이를 건드릴 때마다 `cd study && npm run verify --workspace @front-react/networked-ui-patterns`로 회귀를 조기에 잡는다.

## 소스 근거

- `../study/frontend-foundations/03-networked-ui-patterns/vanilla/src/app.ts`
- `../study/frontend-foundations/03-networked-ui-patterns/vanilla/src/data.ts`
- `../study/frontend-foundations/03-networked-ui-patterns/vanilla/src/main.ts`
- `../study/frontend-foundations/03-networked-ui-patterns/vanilla/src/service.ts`
- `../study/frontend-foundations/03-networked-ui-patterns/vanilla/src/state.ts`
- `../study/frontend-foundations/03-networked-ui-patterns/vanilla/tests/explorer.spec.ts`
- `../study/frontend-foundations/03-networked-ui-patterns/vanilla/tests/explorer.test.ts`
- `../study/frontend-foundations/03-networked-ui-patterns/vanilla/tests/service.test.ts`
