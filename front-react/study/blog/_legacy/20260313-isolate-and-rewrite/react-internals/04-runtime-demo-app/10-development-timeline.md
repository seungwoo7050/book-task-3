# 04 Runtime Demo App development timeline

`04-runtime-demo-app`은 internals 트랙의 최종 시험장에 가깝다. `study/react-internals/04-runtime-demo-app`의 README, `ts/src/app.ts`, `ts/src/data.ts`, `ts/tests/demo.test.ts`, 그리고 2026-03-13 재검증 결과를 같이 놓고 보면 이 앱의 핵심은 "runtime이 실제 앱처럼 보이는 상호작용을 어디까지 버티는가"를 보여 주는 데 있다.

## 구현 순서 요약

1. README와 problem 문서로 shared runtime consumer app이라는 범위를 먼저 고정했다.
2. `useDebouncedValue`, `updateMetrics`, `DemoApp`을 따라 search, pagination, metrics를 한 render loop에 묶었다.
3. 마지막에는 `npm run verify --workspace @front-react/runtime-demo-app`로 debounce/pagination/metrics 시나리오를 다시 통과시켰다.

## 2026-03-08 / Phase 1 - consumer app이라는 범위를 먼저 고정한다

- 당시 목표:
  이 단계가 새 runtime 구현이 아니라, 기존 runtime을 import해 쓰는 app 단계라는 점을 먼저 분명히 한다.
- 변경 단위:
  `README.md`, `problem/README.md`, `docs/README.md`, `ts/README.md`
- 처음 가설:
  demo app이라서 visual layer가 본론일 것 같지만, README는 runtime code를 복사하지 않고 shared package를 소비한다는 점을 더 강조하고 있었다.
- 실제 진행:
  README와 problem 문서를 읽어 consumer app, debounced search, load more, metrics panel이 이 단계의 public contract라는 점을 먼저 고정했다.

CLI:

```bash
$ git log --reverse --stat -- study/react-internals/04-runtime-demo-app | sed -n '1,24p'
commit 46051f3e897f38aacdfce37bcd5119e61c79ebea
Date:   Sun Mar 8 19:03:24 2026 +0900

    A large commit

... ts/src/app.ts
... ts/src/data.ts
... ts/tests/demo.test.ts
```

검증 신호:

- source tree가 app source, data, integration-style test를 같이 가져서 showcase보다 contract-driven demo에 가깝다는 점이 보였다.

핵심 코드:

```ts
function useDebouncedValue<T>(value: T, delayMs: number): T {
  const [debounced, setDebounced] = useState(value);
  useEffect(() => {
    const timeoutId = window.setTimeout(() => {
      setDebounced(value);
    }, delayMs);
    return () => {
      window.clearTimeout(timeoutId);
    };
  }, [value, delayMs]);
  return debounced;
}
```

왜 이 코드가 중요했는가:

consumer app에서 가장 먼저 드러나는 runtime signal은 debounce다. `useState`와 `useEffect`가 실제 interaction에 쓰일 수 있다는 사실을 가장 짧게 보여 주고, 동시에 cleanup timing이 실제 user input에 어떤 의미를 갖는지도 드러낸다.

새로 배운 것:

- internals 단계에서 만든 hook runtime이 의미 있으려면, 이렇게 실제 input delay와 cleanup으로 번역되는 순간이 필요하다.

다음:

- metrics panel이 이 runtime을 어떻게 관찰 가능하게 만드는지 본다.

## 2026-03-08 / Phase 2 - search, pagination, metrics를 한 loop에 묶는다

- 당시 목표:
  demo app이 단순 검색창이 아니라 runtime behavior를 관찰하는 앱이 되게 만든다.
- 변경 단위:
  `ts/src/app.ts`, `ts/src/data.ts`
- 처음 가설:
  search와 pagination만 있어도 충분해 보였지만, README를 보면 metrics panel이 "학습용 관찰값"으로 함께 있어야 runtime 한계를 설명할 수 있었다.
- 실제 진행:
  `rg -n`으로 `useDebouncedValue`, `updateMetrics`, `DemoApp` 위치를 잡고, render count/commit time이 언제 갱신되는지와 visible window가 언제 리셋되는지를 같이 읽었다.

CLI:

```bash
$ rg -n 'useDebouncedValue|updateMetrics|DemoApp|mountRuntimeDemo' \
  study/react-internals/04-runtime-demo-app/ts/src/app.ts
app.ts:23:function useDebouncedValue<T>(value: T, delayMs: number): T
app.ts:39:function updateMetrics(
app.ts:56:function DemoApp()
app.ts:192:export function mountRuntimeDemo(container: HTMLElement): void
```

검증 신호:

- debounce, metrics, mount entrypoint가 한 파일 안에서 이어져 있어 consumer app의 핵심 흐름이 분명했다.

핵심 코드:

```ts
useEffect(() => {
  updateMetrics(
    setMetrics,
    renderStartedAt,
    visibleItems.length,
    filteredItems.length,
    normalizedQuery || "all",
  );
}, [normalizedQuery, visibleItems.length, filteredItems.length]);
```

왜 이 코드가 중요했는가:

metrics panel이 중요한 이유는 runtime을 profiler처럼 과장하려고 해서가 아니다. search와 pagination이 실제로 rerender를 만들고 있다는 사실을 관찰 가능한 값으로 남겨 줘서, 이 consumer app이 단순 showcase가 아니라 runtime 실험대가 되게 만든다.

새로 배운 것:

- consumer app 단계에서는 기능 데모와 runtime observability가 같이 움직여야 "무엇을 만들었다"보다 "이 runtime이 어디까지 버티는가"를 설명할 수 있다.

다음:

- verify로 debounce/pagination/metrics 시나리오를 현재 시점에 다시 닫는다.

## 2026-03-13 / Phase 3 - verify로 consumer app contract를 닫는다

- 당시 목표:
  demo app이 설명용 문구가 아니라 실제 테스트 가능한 consumer라는 점을 확인한다.
- 변경 단위:
  `ts/tests/demo.test.ts`, `tsconfig.json`
- 처음 가설:
  visual app이라서 수동 시연이 먼저일 것 같지만, 현재 범위는 integration-style test와 typecheck만으로 충분히 닫힌다고 봤다.
- 실제 진행:
  canonical verify를 다시 실행해 `3 passed`와 `tsc --noEmit` 통과를 확보했다.

CLI:

```bash
$ cd study
$ npm run verify --workspace @front-react/runtime-demo-app
✓ ts/tests/demo.test.ts (3 tests)
Test Files  1 passed (1)
Tests  3 passed (3)
> tsc --noEmit
```

검증 신호:

- test file 하나가 debounce, load more, metrics라는 consumer app 핵심 시나리오를 모두 닫고 있었다.
- typecheck 통과가 shared runtime import surface가 여전히 일관된다는 점을 보여 줬다.

핵심 코드:

```ts
const visibleItems = filteredItems.slice(0, visibleCount);
const hasMore = visibleItems.length < filteredItems.length;

useEffect(() => {
  setVisibleCount(PAGE_SIZE);
}, [normalizedQuery]);
```

왜 이 코드가 중요했는가:

query가 바뀔 때 visible window를 다시 `PAGE_SIZE`로 되돌리는 이 블록이 search와 pagination을 같은 앱 규칙으로 묶는다. 이런 reset rule이 없으면 load-more state가 이전 검색 결과를 끌고 와서 consumer app 전체가 모호해진다.

새로 배운 것:

- consumer app에서도 상태는 그냥 늘어나는 게 아니라, 특정 입력 변화에서 어디까지를 리셋할지 정해야 흐름이 예측 가능해진다.

다음:

- 제품형 결과물과 포트폴리오 신호는 다음 트랙 `frontend-portfolio`에서 본다.

## 남은 경계

- actual network layer, persistence, infinite scroll observer는 없다.
- metrics는 학습용 관찰값이지 production profiler가 아니다.
- 이 앱은 runtime 한계를 보여 주는 consumer로 의도적으로 범위를 좁게 잡았다.
