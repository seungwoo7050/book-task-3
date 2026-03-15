# Where Browser State Actually Lives

이 프로젝트를 다시 읽으면서 가장 중요하게 보였던 건 이벤트 개수보다 상태의 주소였다. 검색어, status filter, sort order, selected row, editing row, edited title, persisted board, URL query가 한 화면에 다 모이기 때문이다. 이걸 한 덩어리 상태처럼 설명하면 금방 흐려지는데, 코드는 오히려 이걸 꽤 선명하게 나눠 둔다.

## 먼저 URL에 남길 상태와 남기지 않을 상태를 잘라 냈다

핵심 분리는 [`vanilla/src/state.ts`](/Users/woopinbell/work/book-task-3/front-react/study/frontend-foundations/02-dom-state-and-events/vanilla/src/state.ts)에서 시작한다. `parseQuery()`와 `serializeQuery()`는 공유 가능한 query state만 다룬다.

```ts
export function serializeQuery(query: BoardQuery): string {
  const params = new URLSearchParams();

  if (query.search.trim()) {
    params.set("search", query.search.trim());
  }

  if (query.status !== "all") {
    params.set("status", query.status);
  }

  if (query.sort !== DEFAULT_QUERY.sort) {
    params.set("sort", query.sort);
  }
```

여기에는 search, status, sort만 있다. 선택된 row나 편집 draft는 URL에 남기지 않는다. 이 선택이 중요했던 이유는, URL은 공유 가능한 view state까지만 책임지고 나머지는 local state로 남긴다는 경계를 프로젝트 초반에 못 박기 때문이다.

`createInitialBoardState()`도 같은 철학을 따른다. persisted query가 있더라도 URL query가 최종 우선권을 가진다. 실제 test `prefers URL query over persisted query and resets hidden selection`가 바로 이 경계를 고정한다. 즉 이 board는 "지난번 내 상태"보다 "지금 브라우저 주소창이 말하는 상태"를 더 신뢰한다.

## rerender를 허용하되 selection과 focus는 다시 맞춘다

이 프로젝트가 흥미로운 이유는 상태 업데이트마다 DOM 전체를 다시 그리면서도 사용감이 크게 깨지지 않는다는 점이다. 그 중심에는 [`vanilla/src/app.ts`](/Users/woopinbell/work/book-task-3/front-react/study/frontend-foundations/02-dom-state-and-events/vanilla/src/app.ts)의 `render()`와 `reconcileSelection()`이 있다.

```ts
const render = (focusSelector?: string) => {
  state = reconcileSelection(state);
  container.innerHTML = getMarkup(state);
  syncUrl(state.query);
  savePersistedState(storage, state);
  ...
}
```

`reconcileSelection()`은 현재 query로 보이는 item 목록을 다시 계산해서, 숨겨진 selection은 지우고 보이는 첫 row를 새 selection으로 잡는다.

```ts
selectedId: hasSelectedItem ? state.selection.selectedId : visibleItems[0]?.id ?? null,
editingId: hasEditingItem ? state.selection.editingId : null,
```

이 조합이 좋은 이유는 두 가지다.

- filter가 바뀌어 기존 selected row가 사라지면 detail panel이 유령 상태가 되지 않는다.
- rerender 뒤에도 edit input이나 select button으로 focus를 다시 돌려 keyboard 흐름이 끊기지 않는다.

즉 이 프로젝트는 "DOM 전체 rerender는 나쁘다"라고 피하지 않고, rerender 뒤 어떤 것을 복원해야 하는지를 명시적으로 적는 쪽을 택했다.

## event delegation으로 row action을 한 곳에 모았다

행마다 listener를 붙이지 않고 root container에 `input`, `change`, `click`, `keydown` 네 종류만 건다. 특히 action button 처리는 delegated click 한 군데에 모여 있다.

```ts
container.addEventListener("click", (event) => {
  const target = (event.target as HTMLElement | null)?.closest<HTMLButtonElement>("[data-action]");
  ...
  if (action === "select") { ... }
  if (action === "edit") { ... }
  if (action === "cancel") { ... }
  if (action === "save") { ... }
});
```

이 구조 덕분에 list가 rerender돼도 listener를 다시 연결할 필요가 없다. `shell.test.ts`가 "delegated click으로 selection과 inline edit가 수행되는지"를 따로 잡는 이유도 여기에 있다. DOM이 바뀌어도 interaction wiring은 루트 하나에서 유지된다.

keyboard edit save도 비슷하다. `keydown`에서 edit input의 Enter를 가로채 저장으로 연결한다. 그래서 e2e가 실제로 `Tab -> Enter -> type -> Enter` 흐름을 통과시킬 수 있다.

## 마지막 검증은 상태 주소가 정말 유지되는지 브라우저에서 확인한다

이번 Todo에서 다시 돌린 검증은 아래 셋이다.

```bash
npm run build --workspace @front-react/dom-state-and-events
npm run test --workspace @front-react/dom-state-and-events
npm run e2e --workspace @front-react/dom-state-and-events
```

결과는 다음과 같았다.

- `vite build` 통과
- `vitest` 6개 테스트 통과
- `playwright` 2개 시나리오 통과

특히 e2e는 이 프로젝트의 핵심을 꽤 잘 드러낸다.

1. 검색어와 status filter를 바꿔 URL이 실제로 `search=Ops`, `status=open`을 담는지 확인한다.
2. row를 선택하고 edit로 들어가 제목을 바꾼다.
3. 저장 후 notice가 뜨는지 본다.
4. 페이지를 reload해서 query와 edited title이 localStorage에서 복원되는지 확인한다.

또 다른 시나리오는 keyboard-only로 `Select -> Edit -> Enter to save`를 끝까지 통과시킨다. 이 흐름이 중요한 이유는, 상태가 많아질수록 렌더링 로직보다 "어떤 상호작용이 rerender 뒤에도 이어지는가"가 더 중요해지기 때문이다.

## 그래서 이 프로젝트는 상태 라이브러리 입문이 아니라 경계 설정 연습에 가깝다

여기에는 React도 없고 reducer도 없고 server state도 없다. 대신 더 앞단의 질문을 붙잡는다. 브라우저 안에 이미 있는 주소창, localStorage, focus, DOM event를 각각 어디까지 믿고 어디서부터 직접 조합할 것인가.

이 프로젝트의 성과는 바로 그 경계를 코드를 통해 설명 가능하게 만든 데 있다. search/filter/sort는 URL로, board snapshot은 localStorage로, selection/editing은 local UI state로 남기고, rerender 뒤에는 selection과 focus를 다시 맞춘다. 다음 단계에서 async request가 들어오더라도, 이 경계가 먼저 서 있으면 복잡도는 훨씬 늦게 폭발한다.
