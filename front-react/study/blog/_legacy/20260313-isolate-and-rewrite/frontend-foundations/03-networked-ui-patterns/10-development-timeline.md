# 03 Networked UI Patterns development timeline

`03-networked-ui-patterns`는 vanilla 트랙의 마지막 단계답게 "화면을 그린다"보다 "요청 상태를 다룬다"에 더 무게가 실린다. `study/frontend-foundations/03-networked-ui-patterns`의 README, `service.ts`, `state.ts`, `app.ts`, 테스트, 그리고 2026-03-13 재검증 결과를 함께 놓고 보면 이 프로젝트의 핵심은 stale response를 실제로 무시하는 UI contract를 세우는 데 있다.

## 구현 순서 요약

1. README와 problem 문서로 loading/empty/error/retry/abort/stale response가 모두 public contract라는 점을 먼저 고정했다.
2. `state.ts`의 URL state와 request tracker, `app.ts`의 `loadList`/`loadDetail`를 따라 list/detail 요청을 분리하고 stale response를 막는 invariant를 읽었다.
3. 마지막에는 `npm run verify --workspace @front-react/networked-ui-patterns`로 service helper와 retry/navigation smoke를 함께 통과시켰다.

## 2026-03-08 / Phase 1 - async UI contract를 먼저 선언한다

- 당시 목표:
  mock API 예제가 아니라 request lifecycle 예제라는 점을 먼저 고정한다.
- 변경 단위:
  `README.md`, `problem/README.md`, `vanilla/README.md`, `package.json`
- 처음 가설:
  비동기 UI 프로젝트라고 하면 latency simulation에 눈이 먼저 가지만, README를 보니 핵심은 loading/empty/error/retry/abort와 navigation state를 한 화면에서 같이 설명하는 일이었다.
- 실제 진행:
  README와 problem 문서를 읽으며 포함/제외 범위를 먼저 고정했고, `git log --reverse --stat`로 mock service, state, app, tests가 한 세트로 landing된 사실을 확인했다.

CLI:

```bash
$ git log --reverse --stat -- study/frontend-foundations/03-networked-ui-patterns | sed -n '1,24p'
commit 46051f3e897f38aacdfce37bcd5119e61c79ebea
Date:   Sun Mar 8 19:03:24 2026 +0900

    A large commit

... vanilla/src/service.ts
... vanilla/src/state.ts
... vanilla/src/app.ts
... vanilla/tests/explorer.spec.ts
```

검증 신호:

- public surface가 이미 service helper, state helper, Playwright smoke를 함께 갖고 있어서, 이 프로젝트는 fetch helper 튜토리얼보다 훨씬 넓은 contract를 가진다는 점이 드러났다.

핵심 코드:

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

왜 이 코드가 중요했는가:

`createRequestTracker`는 이 프로젝트의 가장 중요한 invariant를 가장 짧게 보여 준다. 비동기 UI에서 중요한 건 요청을 보냈다는 사실이 아니라, 어떤 응답만 최신 state를 바꿀 수 있는가다. 이 한 함수가 그 판단 기준을 숫자 하나로 고정한다.

새로 배운 것:

- abort signal만으로는 stale response 문제를 다 닫지 못한다. 이미 도착한 응답까지 무시하려면 latest-token 같은 별도 기준이 필요하다.

다음:

- 실제 list/detail 로딩 루프가 이 invariant를 어떻게 쓰는지 본다.

## 2026-03-08 / Phase 2 - list/detail 요청을 분리하고 stale response를 무시한다

- 당시 목표:
  async state contract가 실제 UI 함수에서 어떻게 동작하는지 읽는다.
- 변경 단위:
  `vanilla/src/state.ts`, `vanilla/src/app.ts`
- 처음 가설:
  list와 detail 요청을 같은 loading flag로 처리하면 retry나 focus 복원이 금방 꼬일 거라고 봤다.
- 실제 진행:
  `rg -n`으로 `parseUrlState`, `serializeUrlState`, `createRequestTracker`, `loadDetail`, `loadList` 위치를 잡고, `loadList`가 list fetch와 selected item fallback을, `loadDetail`이 detail fetch와 abort/error 분기를 따로 가진다는 점을 중심으로 읽었다.

CLI:

```bash
$ rg -n 'createRequestTracker|parseUrlState|serializeUrlState|loadDetail|loadList' \
  study/frontend-foundations/03-networked-ui-patterns/vanilla/src/state.ts \
  study/frontend-foundations/03-networked-ui-patterns/vanilla/src/app.ts
study/.../state.ts:8:export function parseUrlState(...)
study/.../state.ts:30:export function serializeUrlState(...)
study/.../state.ts:49:export function createRequestTracker()
study/.../app.ts:189:  const loadDetail = async (...)
study/.../app.ts:229:  const loadList = async (...)
```

검증 신호:

- URL state helper와 request tracker가 `state.ts`에, 실제 async orchestration이 `app.ts`에 분리돼 있어서 설명 경계가 또렷했다.
- `loadList`와 `loadDetail`를 분리한 구조 덕분에 loading/error/empty가 list와 detail에서 다르게 표현될 수 있다는 점이 드러났다.

핵심 코드:

```ts
const token = listTracker.next();
const items = await service.listDirectory({ ...state.query, simulateFailure: shouldFail }, listController.signal);
if (!listTracker.isLatest(token)) {
  return;
}
```

왜 이 코드가 중요했는가:

비동기 UI에서 가장 위험한 순간은 "이 응답이 늦게 도착했지만 이미 다른 요청이 진행 중"인 경우다. 이 짧은 블록은 stale response가 state를 덮어쓰지 못하게 막으면서, 사용자가 search나 category를 빠르게 바꿔도 화면이 한 박자 늦은 과거 상태로 돌아가지 않게 만든다.

새로 배운 것:

- async UI의 안정성은 거대한 상태 머신이 아니라, 어느 요청이 최신인지 끝까지 확인하는 작은 invariant에서 자주 나온다.

다음:

- verify 시나리오가 retry와 navigation을 실제로 닫는지 확인한다.

## 2026-03-13 / Phase 3 - verify로 retry와 navigation contract를 닫는다

- 당시 목표:
  service helper correctness와 화면 복구 흐름을 같은 verify 표면으로 묶는다.
- 변경 단위:
  `vanilla/tests/service.test.ts`, `vanilla/tests/explorer.test.ts`, `vanilla/tests/explorer.spec.ts`
- 처음 가설:
  unit test만 보면 request helper가 맞는지 정도만 알 수 있고, 실제 retry/navigation 흐름은 놓치게 된다고 봤다.
- 실제 진행:
  canonical verify를 다시 실행해 service + explorer unit test와 Playwright smoke를 모두 확보했다. 특히 두 E2E 시나리오 제목이 이 프로젝트의 요지를 거의 그대로 요약한다.

CLI:

```bash
$ cd study
$ npm run verify --workspace @front-react/networked-ui-patterns
✓ vanilla/tests/service.test.ts (2 tests)
✓ vanilla/tests/explorer.test.ts (2 tests)
Test Files  2 passed (2)
Tests  4 passed (4)
Running 2 tests using 1 worker
✓ updates query params and loads detail from the directory list
✓ recovers from a simulated failure and keeps keyboard navigation viable
2 passed (4.0s)
```

검증 신호:

- unit tests가 mock service와 explorer state logic을 닫았다.
- Playwright `2 passed`가 query-driven navigation, retry, keyboard viability까지 public contract에 포함된다는 점을 보여 줬다.

핵심 코드:

```ts
detailController?.abort();
detailController = new AbortController();
const token = detailTracker.next();
...
if ((error as Error).name === "AbortError" || !detailTracker.isLatest(token)) {
  return;
}
```

왜 이 코드가 중요했는가:

detail 요청은 list보다 더 쉽게 꼬인다. 사용자가 다른 항목을 바로 눌렀을 때 이전 detail 응답이 뒤늦게 도착하면, 화면은 금방 엉뚱한 항목을 보여 주게 된다. abort와 latest-token check를 같이 둔 이유가 바로 여기에 있고, 이 블록이 그 판단을 가장 직접적으로 보여 준다.

새로 배운 것:

- abort는 네트워크 비용을 줄여 주고, latest check는 state corruption을 막아 준다. async UI에서는 둘이 역할이 다르다.

다음:

- 실제 서버 캐시나 auth는 아직 없다. 다음 트랙 `react-internals`에서는 이 복잡한 상태를 컴포넌트 추상화와 렌더링 모델 쪽으로 옮겨 간다.

## 남은 경계

- 실제 서버 캐시, 인증, SSR은 없다.
- backoff policy와 real transport layer는 최소 범위만 다룬다.
- keyboard flow는 smoke 수준으로만 유지한다.
