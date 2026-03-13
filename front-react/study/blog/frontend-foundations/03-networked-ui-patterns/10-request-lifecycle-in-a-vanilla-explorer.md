# Request Lifecycle In A Vanilla Explorer

비동기 UI를 다룬다는 말은 흔히 loading spinner를 하나 더 붙이는 일처럼 들린다. 하지만 이 프로젝트를 읽다 보면 진짜 문제는 그보다 훨씬 앞에서 시작한다. 사용자가 검색어를 빠르게 바꾸고, 목록을 다시 읽어 오고, 상세 패널이 뒤늦게 응답하고, 한 번은 실패한 요청이 retry를 통해 회복될 때, 도대체 어떤 응답이 지금 화면을 바꿀 자격이 있는가.

이 질문은 프레임워크를 쓰느냐와 크게 상관이 없다. 오히려 vanilla explorer처럼 도구가 적을수록, request lifecycle을 직접 설계해야 한다는 사실이 더 선명하게 보인다. 이 프로젝트가 mock service를 직접 만든 이유도 여기에 있다. 네트워크를 추상적으로 설명하지 않고, 지연과 실패와 abort를 코드로 만들겠다는 선택이다.

그 덕분에 글의 흐름도 명확하다. 먼저 실패와 지연을 재현할 수 있는 service를 만들고, 그다음 "가장 마지막 요청만 화면을 바꿀 수 있다"는 invariant를 세우고, 마지막에 브라우저에서 retry와 query-driven navigation을 확인한다.

## 구현 순서를 먼저 짚으면

- `service.ts`에서 latency, failure, abort를 가진 deterministic service를 만들었다.
- `createRequestTracker()`와 `AbortController`를 같이 사용해 stale response를 걸러냈다.
- `npm run verify`로 retry, URL navigation, keyboard viability를 실제 브라우저에서 확인했다.

## 먼저 네트워크를 외부 환경이 아니라 코드로 만들었다

이 프로젝트에서 가장 좋은 선택은 `wait()`를 직접 구현한 일이었다. 이 함수는 timeout이 끝나기 전에 `AbortSignal`이 오면 즉시 `AbortError`를 던진다. 즉 네트워크는 더 이상 운에 맡긴 외부 세계가 아니라, 테스트 가능한 로컬 규칙이 된다.

```ts
function wait(ms: number, signal: AbortSignal): Promise<void> {
  return new Promise((resolve, reject) => {
    const timer = window.setTimeout(() => {
      signal.removeEventListener("abort", onAbort);
      resolve();
    }, ms);

    const onAbort = () => {
      window.clearTimeout(timer);
      reject(new DOMException("The operation was aborted.", "AbortError"));
    };
```

이 위에서 `listDirectory()`는 query 길이에 비례한 지연을 만들고, `simulateFailure`가 켜지면 명시적으로 에러를 던진다. 덕분에 loading, error, retry는 README의 문장으로만 남지 않고 실제 코드 경로가 된다.

`service.test.ts`가 가장 먼저 abort 시 `AbortError`를 확인하는 것도 같은 이유다. request lifecycle을 배우려면 무엇이 성공하는지보다 무엇이 중간에 취소되는지가 먼저 보여야 했다.

## abort만으로는 부족했고, latest-request invariant가 따로 필요했다

요청을 취소하는 것과, 늦게 도착한 응답이 state를 덮어쓰지 못하게 하는 것은 다른 문제다. 이 프로젝트가 `createRequestTracker()`를 따로 둔 이유가 바로 그것이다.

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

실제 `loadList()`는 새 요청이 시작될 때마다 이전 controller를 abort하고, 동시에 새 token을 발급한다. 응답이 돌아오면 `isLatest(token)`를 통과한 경우에만 state를 갱신한다.

```ts
const token = listTracker.next();
listController?.abort();
listController = new AbortController();

const items = await service.listDirectory(
  { ...state.query, simulateFailure: shouldFail },
  listController.signal,
);

if (!listTracker.isLatest(token)) {
  return;
}
```

여기서 배운 것은 abort와 stale-response 방지가 별개의 invariant라는 점이었다. abort는 불필요한 일을 멈추는 장치이고, request tracker는 늦게 도착한 값이 화면을 덮어쓰지 못하게 하는 장치다. 둘 중 하나만 있으면 race를 완전히 설명할 수 없다.

## 마지막에는 retry와 navigation을 브라우저에서 끝까지 밀어붙였다

이 프로젝트의 검증은 helper 함수 수준에서 끝나지 않는다. query string이 실제로 바뀌고, 목록과 상세가 분리된 상태로 움직이며, 실패 뒤에 retry가 가능해야만 request lifecycle이 제품처럼 읽힌다.

```bash
cd study
npm run verify --workspace @front-react/networked-ui-patterns
```

2026-03-13 replay 기준으로 `vitest`는 4개 테스트를, `playwright`는 2개 시나리오를 통과했다. 브라우저 시나리오는 단순히 데이터를 불러오는지 보는 것이 아니라, query params가 바뀌는지, detail이 목록과 함께 이동하는지, simulated failure 뒤 retry가 회복되는지를 함께 확인한다.

코드에서도 list와 detail이 같은 상태가 아니라는 점이 드러난다. list가 성공했더라도 detail은 다시 loading이 될 수 있고, 반대로 list가 실패하면 detail은 empty로 돌아간다. `docs/concepts/request-lifecycle.md`가 `loading`, `success`, `empty`, `error`를 하나의 불린으로 뭉개지 않는 이유도 바로 여기에 있다.

```ts
state = {
  ...state,
  listState: "error",
  errorMessage: error instanceof Error ? error.message : "Directory request failed.",
  items: [],
  currentItem: null,
  detailState: "empty",
  detailErrorMessage: null,
};
```

이 조각은 요청 실패를 "그냥 실패"로 남겨 두지 않는다. 무엇이 비어야 하고, 무엇이 다시 retry 가능 상태로 남아야 하는지까지 함께 정리한다.

## 무엇이 아직 남았는가

이 explorer는 아직 실제 서버 캐시나 인증, SSR을 다루지 않는다. 하지만 여기까지 와서 하나는 분명해진다. 비동기 UI의 핵심은 데이터를 가져오는 코드보다 어떤 응답이 지금의 화면에 속하는지를 결정하는 규칙이다.

다음 트랙이 React internals로 넘어가는 이유도 이 지점과 연결된다. 화면 상태를 더 정교하게 다루려면 결국 JSX, VDOM, diff, commit 같은 더 아래 계층까지 이해해야 하기 때문이다.
