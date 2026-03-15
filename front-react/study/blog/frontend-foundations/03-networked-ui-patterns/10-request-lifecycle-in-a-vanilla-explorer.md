# Request Lifecycle In A Vanilla Explorer

이 프로젝트를 다시 읽을 때 가장 먼저 정리해야 했던 건 "비동기 데이터 불러오기"가 아니라 "어느 요청 결과를 믿을 것인가"였다. 검색어를 바꾸고, category를 바꾸고, 항목을 열고, 실패를 일부러 주입하고, retry까지 하려면 loading 화면 자체보다 stale response와 navigation state가 더 큰 문제가 되기 때문이다.

## list와 detail을 아예 다른 비동기 상태로 나눴다

[`vanilla/src/app.ts`](/Users/woopinbell/work/book-task-3/front-react/study/frontend-foundations/03-networked-ui-patterns/vanilla/src/app.ts)는 상태를 꽤 노골적으로 나눈다.

- `listState`
- `detailState`
- `items`
- `currentItem`
- `errorMessage`
- `detailErrorMessage`
- `selectedId`
- `simulateFailureNext`

이 분리가 중요한 이유는 list 실패와 detail 실패가 같은 화면에서 일어나더라도 UI 의미가 다르기 때문이다. list가 실패하면 전체 directory panel이 retry UI로 바뀌고, detail이 실패하면 현재 선택된 item의 detail panel만 retry 대상이 된다. 비슷해 보이는 로딩 화면 둘을 분리해 둔 덕분에, 실패가 어디서 났는지 사용자와 코드가 동시에 잃지 않는다.

## stale response 보호는 `AbortController`와 token 두 겹으로 잡았다

이 project의 진짜 중심은 [`vanilla/src/state.ts`](/Users/woopinbell/work/book-task-3/front-react/study/frontend-foundations/03-networked-ui-patterns/vanilla/src/state.ts)의 `createRequestTracker()`와 [`vanilla/src/app.ts`](/Users/woopinbell/work/book-task-3/front-react/study/frontend-foundations/03-networked-ui-patterns/vanilla/src/app.ts)의 `loadList`/`loadDetail` 조합이다.

```ts
export function createRequestTracker() {
  let token = 0;

  return {
    next() {
      token += 1;
      return token;
    },
    isLatest(nextToken: number) {
      return nextToken === token;
    },
  };
}
```

`loadList()`는 새 요청을 시작할 때 이전 controller를 abort하고, 새 token을 발급한다.

```ts
listController?.abort();
listController = new AbortController();
const token = listTracker.next();
```

그리고 응답이 돌아오면 두 가지를 확인한다.

- abort된 요청인가
- 최신 token인가

```ts
if ((error as Error).name === "AbortError" || !listTracker.isLatest(token)) {
  return;
}
```

이 구조가 좋은 이유는 mock API라도 request race가 현실적으로 모델링되기 때문이다. 사용자가 검색어를 빠르게 바꾸거나 category를 연속으로 바꾸면, 늦게 끝난 옛 요청 결과가 화면을 덮어쓰지 않는다.

## query navigation은 "선택된 item도 URL로 복원 가능해야 한다"는 전제를 따른다

이 프로젝트는 search/category뿐 아니라 selected item도 URL에 넣는다. `buildUrlState()`가 그것을 보여 준다.

```ts
function buildUrlState(state: ExplorerState): ExplorerUrlState {
  return {
    ...state.query,
    item: state.selectedId,
  };
}
```

그래서 e2e 첫 시나리오가 `search=policy`와 `item=doc-102`를 같이 확인한다. 이건 단순한 편의가 아니라, 탐색 상태를 주소창만으로 복원할 수 있어야 한다는 요구를 코드로 고정한 것이다.

mock service [`vanilla/src/service.ts`](/Users/woopinbell/work/book-task-3/front-react/study/frontend-foundations/03-networked-ui-patterns/vanilla/src/service.ts)도 그 질문에 맞춰 설계돼 있다.

- list는 `140 + query.search.length * 25` ms 지연
- detail은 90 ms 지연
- `simulateFailure`가 켜지면 list 요청은 명시적으로 실패
- abort 시 `AbortError` 반환

즉 서버처럼 보이는 UX를 만들되, 실패와 race를 일부러 관찰 가능한 형태로 압축해 둔 셈이다.

## retry와 keyboard 흐름이 실제 브라우저에서도 이어진다

이번 Todo에서 다시 돌린 검증은 아래 셋이다.

```bash
npm run build --workspace @front-react/networked-ui-patterns
npm run test --workspace @front-react/networked-ui-patterns
npm run e2e --workspace @front-react/networked-ui-patterns
```

결과는 다음과 같았다.

- `vite build` 통과
- `vitest` 4개 테스트 통과
- `playwright` 2개 시나리오 통과

테스트가 고정하는 핵심은 세 가지다.

1. abort된 list request는 실제로 `AbortError`를 내야 한다.
2. request tracker는 최신 token만 유효하게 봐야 한다.
3. 브라우저에서는 `query update -> open item`과 `simulate failure -> retry -> keyboard open` 흐름이 끝까지 이어져야 한다.

특히 두 번째 Playwright 시나리오는 의미가 크다. 실패를 일부러 주입하고 retry로 복구한 뒤, keyboard `Tab`과 `Enter`만으로 결과 항목을 열어 detail panel까지 도달하는지 본다. 이건 retry UI가 단순히 에러 메시지 옆 버튼이 아니라, 실패 이후에도 탐색 흐름을 다시 잇는 surface여야 한다는 걸 보여 준다.

## 그래서 이 프로젝트는 fetch 예제가 아니라 async UI 규칙 연습에 가깝다

여기에는 실제 서버도 없고 캐시도 없고 인증도 없다. 하지만 비동기 UI가 흔들리는 핵심 지점은 이미 다 들어 있다. loading, empty, error, retry, abort, stale response, URL navigation이 한 화면에서 서로 엮이기 때문이다.

이 프로젝트의 성과는 그 복잡도를 프레임워크 없이도 설명 가능한 규칙으로 나눠 놓은 데 있다. list/detail 상태는 분리하고, 요청은 abort와 token으로 보호하고, selection은 URL에 남기며, retry 뒤에도 keyboard 흐름을 유지한다. 다음에 React나 data-fetching library를 써도, 실제로 무엇을 대신 맡기게 되는지 설명할 수 있는 이유가 바로 여기서 생긴다.
