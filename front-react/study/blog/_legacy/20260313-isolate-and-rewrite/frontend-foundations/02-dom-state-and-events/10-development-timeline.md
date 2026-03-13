# 02 DOM State And Events development timeline

`02-dom-state-and-events`를 다시 읽을 때 먼저 보이는 건 화면보다 state 경계다. `study/frontend-foundations/02-dom-state-and-events`의 README, `state.ts`, `app.ts`, 테스트, 재검증 CLI를 따라가면 이 프로젝트가 "task board UI"보다 "query/local state를 한 화면에서 어떻게 조율할 것인가"라는 질문에 더 가깝다는 점이 선명해진다.

## 구현 순서 요약

1. README와 `package.json`으로 URL query, localStorage, selection, inline edit를 모두 verify 대상에 포함한 독립 프로젝트라는 점을 먼저 고정했다.
2. `vanilla/src/state.ts`에서 query parsing/serialization과 persistence 규칙을 읽고, `app.ts`에서 이 state를 root delegation과 rerender로 연결했다.
3. 마지막에는 `npm run verify --workspace @front-react/dom-state-and-events`로 helper correctness와 keyboard interaction continuity를 함께 닫았다.

## 2026-03-08 / Phase 1 - state boundary를 먼저 고정한다

- 당시 목표:
  화면 요소보다 state 저장 위치와 복원 규칙을 먼저 정리한다.
- 변경 단위:
  `README.md`, `problem/README.md`, `vanilla/README.md`, `package.json`
- 처음 가설:
  selection이나 inline edit가 눈에 띄어서 interaction 예제로만 읽기 쉽지만, README를 보면 핵심은 `URL query state + local persistence + rerender` 조합이었다.
- 실제 진행:
  프로젝트 README와 problem 문서를 읽고, verify가 vitest와 Playwright를 모두 포함한다는 점을 먼저 확인했다. 그 다음 `git log --reverse --stat`로 `state.ts`, `app.ts`, `board.spec.ts`가 같은 큰 change-set에 들어왔다는 사실을 anchor로 삼았다.

CLI:

```bash
$ git log --reverse --stat -- study/frontend-foundations/02-dom-state-and-events | sed -n '1,24p'
commit 46051f3e897f38aacdfce37bcd5119e61c79ebea
Date:   Sun Mar 8 19:03:24 2026 +0900

    A large commit

... vanilla/src/app.ts
... vanilla/src/state.ts
... vanilla/tests/board.spec.ts
... playwright.config.ts
```

검증 신호:

- 공개 surface가 이미 `state.ts`와 Playwright smoke까지 포함하고 있어서, 이 프로젝트를 단순 DOM manipulation 예제로 축소하면 안 된다는 점이 분명했다.

핵심 코드:

```ts
export function serializeQuery(query: BoardQuery): string {
  const params = new URLSearchParams();
  if (query.search.trim()) params.set("search", query.search.trim());
  if (query.status !== "all") params.set("status", query.status);
  if (query.sort !== DEFAULT_QUERY.sort) params.set("sort", query.sort);
  return params.toString() ? `?${params.toString()}` : "";
}
```

왜 이 코드가 중요했는가:

`serializeQuery`를 먼저 보는 순간 이 프로젝트의 본론이 분명해진다. state는 메모리 안에만 있는 게 아니라 URL이라는 외부 표면에도 남아야 하고, 그래서 query state와 local state를 같은 방식으로 다루면 안 된다.

새로 배운 것:

- 브라우저 UI에서 state 설계는 저장 위치에 따라 달라진다. URL에 남겨야 하는 state는 공유와 복원이 우선이고, local edit state는 현재 interaction continuity가 우선이다.

다음:

- 이 state 경계가 실제 render loop와 selection reconciliation에 어떻게 들어가는지 본다.

## 2026-03-08 / Phase 2 - render loop와 event delegation으로 state를 계속 맞춘다

- 당시 목표:
  query/local state 모델이 실제 보드 상호작용으로 이어지는 경로를 찾는다.
- 변경 단위:
  `vanilla/src/state.ts`, `vanilla/src/app.ts`
- 처음 가설:
  매번 `innerHTML`로 다시 그리면 selection과 focus가 깨지기 쉬우니, reconcile 단계가 반드시 있을 거라고 봤다.
- 실제 진행:
  `rg -n`으로 `createInitialBoardState`, `reconcileSelection`, `mountBoard`, `savePersistedState` 위치를 다시 잡고, `mountBoard`의 `render -> syncUrl -> savePersistedState -> focus restore` 흐름을 중심으로 읽었다.

CLI:

```bash
$ rg -n 'serializeQuery|createInitialBoardState|savePersistedState|reconcileSelection|mountBoard' \
  study/frontend-foundations/02-dom-state-and-events/vanilla/src/state.ts \
  study/frontend-foundations/02-dom-state-and-events/vanilla/src/app.ts
study/.../state.ts:44:export function serializeQuery(...)
study/.../state.ts:120:export function reconcileSelection(...)
study/.../state.ts:139:export function createInitialBoardState(...)
study/.../app.ts:146:export function mountBoard(...)
study/.../app.ts:153:    savePersistedState(storage, state);
```

검증 신호:

- `reconcileSelection`과 `savePersistedState`가 render 직전에/직후에 배치돼 있어서, 이 프로젝트가 single source of truth 없이 흩어진 handler들의 집합이 아니라는 점이 드러났다.

핵심 코드:

```ts
const render = (focusSelector?: string) => {
  state = reconcileSelection(state);
  container.innerHTML = getMarkup(state);
  syncUrl(state.query);
  savePersistedState(storage, state);
  const focusTarget = focusSelector
    ? container.querySelector<HTMLElement>(focusSelector)
    : null;
  focusTarget?.focus();
};
```

왜 이 코드가 중요했는가:

여기서 핵심은 rerender 자체가 아니라 rerender 전후에 무엇을 고정하느냐다. `reconcileSelection`으로 visible set과 selection을 맞추고, 바로 이어서 URL과 localStorage를 갱신한 뒤 focus를 복원하니, query change나 edit save가 일어나도 사용자의 흐름이 끊기지 않는다.

새로 배운 것:

- DOM 기반 UI라도 event delegation과 explicit focus restoration을 조합하면 rerender 중심 구조를 꽤 안정적으로 운영할 수 있다.

다음:

- 이 흐름이 query -> select -> edit -> save 시나리오를 실제로 통과하는지 본다.

## 2026-03-13 / Phase 3 - verify로 query와 keyboard 흐름을 닫는다

- 당시 목표:
  helper correctness와 interaction continuity를 같은 verify surface로 묶는다.
- 변경 단위:
  `vanilla/tests/state.test.ts`, `vanilla/tests/shell.test.ts`, `vanilla/tests/board.spec.ts`
- 처음 가설:
  unit test만으로는 query sync나 inline edit 이후 focus continuity를 충분히 설명하기 어렵다고 봤다.
- 실제 진행:
  canonical verify를 다시 실행해 vitest `6 passed`와 Playwright `2 passed`를 함께 확보했다. Playwright 시나리오 제목이 이 프로젝트의 핵심 경로를 그대로 보여 준다.

CLI:

```bash
$ cd study
$ npm run verify --workspace @front-react/dom-state-and-events
✓ vanilla/tests/state.test.ts (4 tests)
✓ vanilla/tests/shell.test.ts (2 tests)
Test Files  2 passed (2)
Tests  6 passed (6)
Running 2 tests using 1 worker
✓ syncs filters to URL and persists edits across reload
✓ supports keyboard selection and inline edit submission
2 passed (3.1s)
```

검증 신호:

- unit tests가 query serialization과 persistence helper를 닫았다.
- Playwright 제목만 봐도 URL sync, reload persistence, keyboard inline edit가 이 프로젝트의 public contract라는 점이 분명하다.

핵심 코드:

```ts
container.addEventListener("input", (event) => {
  const target = event.target as HTMLInputElement | null;
  if (target?.name === "search") {
    setQuery({ search: target.value }, "Search query synced to URL and storage.", "#searchInput");
  }
});
```

왜 이 코드가 중요했는가:

`input` handler 하나가 search box 값을 읽고, 그 결과를 URL/state/persistence/render/focus까지 연쇄시키는 출발점이 된다. 이 지점이 있어서 query state가 단순 필터 값이 아니라 공유 가능한 navigation state로 격상된다.

새로 배운 것:

- 브라우저 state 문제에서 중요한 건 "어디에 저장하느냐"뿐 아니라 "다시 그린 뒤 어떤 요소로 돌아오느냐"다. focus 복원이 없으면 keyboard flow는 금방 끊긴다.

다음:

- network request와 request race는 아직 없다. 다음 단계 `03-networked-ui-patterns`에서 비동기 상태 전이가 본격적으로 들어온다.

## 남은 경계

- 실제 network layer와 server cache는 없다.
- multi-select, drag and drop, schema migration은 다루지 않는다.
- URL/state sync는 board 한 화면 범위에 집중한다.
