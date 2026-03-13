# Where Browser State Actually Lives

브라우저에서 상태를 다룬다는 말을 막연하게 받아들이고 있으면, 작은 보드 UI 하나만 만들어도 금방 길을 잃는다. 검색어는 URL에 남겨야 할 것 같고, 현재 선택한 행은 localStorage에 저장하고 싶고, 편집 중인 input은 메모리에만 두는 편이 자연스럽다. 문제는 이 셋을 모두 "state"라고 부르는 순간 어디까지가 공유 가능한 문맥이고 어디까지가 개인 작업 문맥인지 흐려진다는 데 있다.

이 프로젝트는 바로 그 모호함을 정리하는 단계다. search, status, sort, row selection, inline edit, local persistence, reload 이후 복원까지 전부 넣어 놓고도 코드가 무너지지 않는 이유는, 시작부터 상태의 저장 위치와 우선순위를 명시했기 때문이다.

여기서 제일 흥미로운 점은 이벤트 처리 방식도 그 결정에 종속된다는 사실이다. DOM이 자주 다시 그려지는 구조라면, 개별 행에 listener를 붙이는 것보다 root-level delegation과 focus 복원이 더 중요한 문제로 올라온다.

## 구현 순서를 먼저 짚으면

- 먼저 `state.ts`에서 URL query, persisted state, ephemeral selection의 경계를 고정했다.
- 그 위에 `app.ts`의 root-level `input`, `change`, `click`, `keydown` delegation을 얹었다.
- 마지막에는 `npm run verify`로 reload 이후 복원과 keyboard save가 실제 브라우저에서 이어지는지 확인했다.

## 이 보드가 먼저 풀어야 했던 건 렌더링이 아니라 우선순위였다

`createInitialBoardState()`는 이 프로젝트의 핵심 규칙을 가장 짧게 보여 주는 함수다. persisted query가 있더라도 현재 URL query가 마지막에 덮어쓰고, selection은 현재 보이는 목록을 기준으로 다시 정리된다.

```ts
export function createInitialBoardState(locationSearch: string, storage: Storage): BoardState {
  const persisted = loadPersistedState(storage);
  const query = {
    ...DEFAULT_QUERY,
    ...(persisted?.query ?? {}),
    ...parseQuery(locationSearch),
  };
  const items = cloneItems(persisted?.items ?? DEFAULT_ITEMS);
  return reconcileSelection({ ... });
}
```

이 순서가 없으면 링크로 들어왔을 때 오래된 저장 상태가 현재 view를 덮어쓰거나, 반대로 reload 이후에 사용자가 보던 문맥이 너무 많이 사라진다. `docs/concepts/state-and-url-boundaries.md`가 URL state, local persisted state, ephemeral UI state를 굳이 따로 설명하는 이유도 여기에 있다.

여기서 새로 배운 건 state 관리가 값의 개수보다 우선순위의 문제라는 점이었다. search와 sort는 공유와 재진입을 위해 URL에 남겨야 하지만, `editingId` 같은 값은 현재 화면 문맥이 끝나는 순간 사라져도 괜찮다.

## DOM이 자주 바뀌는 화면에서는 delegation이 더 현실적이었다

이 보드는 상태가 바뀔 때마다 `render()`가 DOM을 다시 그리는 구조를 택했다. 그 대신 `render()` 안에서 URL sync, persistence, focus 복원을 같이 처리해 사용자의 위치를 놓치지 않도록 했다.

```ts
const render = (focusSelector?: string) => {
  state = reconcileSelection(state);
  container.innerHTML = getMarkup(state);
  syncUrl(state.query);
  savePersistedState(storage, state);

  if (focusSelector) {
    container.querySelector<HTMLElement>(focusSelector)?.focus();
  }
};
```

이 선택 때문에 이벤트도 자연스럽게 루트로 모였다. 실제 코드를 보면 `click`과 `keydown`가 모두 `[data-action]`이나 `[data-edit-id]` 기준으로 동작한다. 개별 row에 listener를 붙이는 대신, 어떤 액션이 일어났는지와 그 뒤에 어디로 focus를 돌려보낼지를 한 곳에서 관리한다.

```ts
container.addEventListener("click", (event) => {
  const target = (event.target as HTMLElement | null)?.closest<HTMLButtonElement>("[data-action]");
  if (!target) {
    return;
  }
  if (target.dataset.action === "edit") {
    setEditing(target.dataset.id!, `Editing ${target.dataset.id}.`);
  }
});
```

이 방식이 좋았던 이유는 rerender-friendly 했기 때문이다. DOM이 자주 갈아끼워지는 화면에서는 event delegation이 단순한 최적화가 아니라 구조 보존 장치가 된다. 상태가 바뀌어도 이벤트 루프는 흔들리지 않고, focus만 명시적으로 복원해 주면 keyboard path도 같이 살아남는다.

## 마지막 검증은 reload와 keyboard path를 브라우저에서 증명하는 일이었다

이 프로젝트는 helper 함수 단위 테스트만으로는 충분하지 않다. URL과 localStorage의 우선순위는 결국 새로고침과 실제 input 흐름 위에서 드러나기 때문이다.

```bash
cd study
npm run verify --workspace @front-react/dom-state-and-events
```

2026-03-13 replay 기준으로 `vitest`는 6개 테스트를, `playwright`는 2개 시나리오를 통과했다. E2E가 다루는 핵심은 query sync, row 선택, inline edit, save 이후 복원이다. 특히 keyboard-only 경로가 별도 시나리오로 남아 있다는 점이 중요했다. 이 보드는 마우스로만 쓰는 도구가 아니라, rerender 뒤에도 현재 위치를 잃지 않는 화면이어야 했기 때문이다.

코드도 그 사실을 잘 보여 준다. Enter 저장 경로는 click 저장 경로와 같은 state transition을 공유한다. 즉 키보드 사용자라고 해서 다른 로직을 타지 않는다.

```ts
if (event.key === "Enter" && target instanceof HTMLInputElement && target.matches("[data-edit-id]")) {
  event.preventDefault();
  const nextTitle = target.value.trim();
  state = {
    ...state,
    items: updateItemTitle(state.items, itemId, nextTitle),
    selection: { selectedId: itemId, editingId: null },
  };
  render();
}
```

이 작은 통합 덕분에 keyboard path는 마우스 path의 예외 처리로 밀려나지 않았다. 둘 다 같은 보드 상태를 바꾸고, 같은 복원 규칙을 따라간다.

## 무엇이 아직 남았는가

이 프로젝트는 네트워크를 다루지 않는다. 그래서 아직 loading, error, retry, abort, stale response 같은 비동기 상태는 등장하지 않는다. 하지만 오히려 그 덕분에 하나는 분명해졌다. 브라우저 상태는 한 덩어리가 아니라 URL, persistence, ephemeral UI라는 서로 다른 책임을 가진 층으로 나뉜다.

다음 질문은 그 위에 비동기 요청이 들어오면 어떤 층이 추가되느냐는 것이다. `03-networked-ui-patterns`는 바로 그 지점, 즉 request lifecycle이 화면 상태와 충돌하기 시작하는 순간을 다룬다.
