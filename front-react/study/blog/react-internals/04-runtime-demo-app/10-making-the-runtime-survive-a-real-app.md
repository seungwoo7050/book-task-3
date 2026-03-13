# Making The Runtime Survive A Real App

런타임을 직접 만들고 나면 곧장 드는 욕심이 하나 있다. 기능을 더 붙여 보고 싶어진다. 하지만 이 프로젝트는 그 반대 방향을 택한다. 새로운 런타임 기능을 늘리기보다, 이미 만든 `@front-react/hooks-and-events`가 평범한 앱 상호작용을 실제로 버틸 수 있는지부터 본다.

이 선택이 중요한 이유는 internals 학습의 마지막 검증이 결국 consumer app이기 때문이다. library 테스트만으로는 런타임의 한계가 잘 드러나지 않는다. debounce가 정말 cleanup과 함께 움직이는지, pagination이 render count에 어떤 흔적을 남기는지, metrics가 상호작용 뒤에도 계속 보이는지 같은 문제는 실제 화면 위에 올려 봐야 드러난다.

그래서 이 프로젝트의 중심은 새 알고리즘이 아니라 소비 방식이다. runtime 코드를 앱 안에 복사하지 않고 workspace dependency로 가져다 쓰면서, 앱 레이어는 search, load more, metrics 같은 사용자 흐름에만 집중한다.

## 구현 순서를 먼저 짚으면

- `useDebouncedValue()`로 effect cleanup과 state update가 실제 consumer hook에서 버티는지 확인했다.
- 결과 목록과 metrics 패널을 한 화면에 두어 사용자 상호작용과 런타임 관찰값을 같이 보게 했다.
- `npm run verify`로 debounce, pagination, metrics 유지 시나리오를 고정했다.

## 가장 먼저 검증한 것은 fancy UI가 아니라 debounce였다

debounce는 작고 익숙한 패턴이지만, 런타임 입장에서는 꽤 까다롭다. state 저장, timeout 등록, cleanup, 재렌더 예약이 모두 맞물려야 하기 때문이다. 그래서 이 앱은 시작부터 `useDebouncedValue()`를 통해 런타임의 effect semantics를 소비자 관점에서 시험했다.

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

이 함수가 좋은 시험대인 이유는 간단하다. cleanup이 제때 돌지 않으면 이전 timeout이 남고, state update가 제대로 예약되지 않으면 debounce 자체가 작동하지 않는다. 즉 runtime의 기초 semantics가 흔들리면 가장 먼저 무너지는 곳이 바로 이런 consumer hook이다.

## 앱은 결과보다 관찰값을 함께 보여 주도록 설계됐다

DemoApp은 검색 결과만 보여 주지 않는다. render count, last commit time, visible count, active query를 나란히 노출한다. 이게 학습용 앱으로서 이 프로젝트를 특별하게 만든다.

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

이 effect 덕분에 사용자는 검색어를 바꾸거나 더 많은 결과를 불러올 때, 화면 결과와 함께 런타임이 어떤 관찰값을 남기는지도 같이 보게 된다. `docs/concepts/shared-runtime-consumption.md`가 "runtime 복사본이 아니라 shared package 소비"를 굳이 강조하는 이유도 여기에 있다. 앱이 런타임을 테스트하는 또 다른 장치가 되기 때문이다.

실제 UI도 그 목적을 숨기지 않는다. 결과 패널 옆에 metrics 패널을 둬서, consumer app이 곧 관찰 도구가 되도록 만들었다.

```ts
createElement(
  "aside",
  { className: "metrics-panel" },
  createElement("h2", null, "Render metrics"),
  createElement("dd", { id: "metric-renders" }, String(metrics.renderCount)),
  createElement("dd", { id: "metric-commit-ms" }, `${metrics.lastCommitMs} ms`),
)
```

이 패널은 production profiler를 흉내 내는 것이 아니다. 오히려 "지금 만든 런타임은 이런 상호작용에서 이 정도로 움직인다"는 학습용 관찰값을 노출하는 쪽에 가깝다. 그래서 글도 자연스럽게 기능 설명보다 런타임 반응 설명으로 이동한다.

## verify가 말해 주는 건 앱이 아니라 런타임의 생존성이다

이 프로젝트의 테스트 이름을 보면 의도가 분명하다. debounce 이후에만 결과가 바뀌는지, load more가 visible metrics를 같이 바꾸는지, 여러 상호작용 뒤에도 render metrics가 계속 보이는지를 확인한다.

```bash
cd study
npm run verify --workspace @front-react/runtime-demo-app
```

2026-03-13 replay 기준으로 `vitest` 3개 테스트와 `tsc --noEmit`이 통과했다. 숫자만 보면 작아 보이지만, 이 테스트들은 앱 기능 자체보다 consumer runtime semantics를 확인하는 성격이 강하다.

테스트 코드도 그 점을 잘 보여 준다. 예를 들어 debounce 시나리오는 timer를 260ms 진행시킨 뒤에야 query와 match count가 바뀌는지 확인한다.

```ts
input.value = "metrics";
input.dispatchEvent(new Event("input", { bubbles: true }));

expect(container.textContent).toContain("Showing 4 of 10 matches");

await vi.advanceTimersByTimeAsync(260);

expect(container.textContent).toContain("Showing 2 of 2 matches");
expect(container.querySelector("#metric-query")?.textContent).toBe("metrics");
```

즉 이 프로젝트의 verify는 "앱이 잘 동작한다"보다 "런타임이 소비되는 순간에도 여전히 설명 가능한가"를 묻는 검증에 가깝다.

## 무엇이 아직 남았는가

이 앱은 실제 infinite scroll observer도 없고, 네트워크 계층도 없고, persistence도 없다. 그럼에도 마지막 internals 프로젝트로서 충분한 이유는 분명하다. 런타임은 library 내부에서만 완성되는 것이 아니라, 실제 consumer app 위에 올렸을 때 비로소 어디까지가 설계된 범위이고 어디서부터가 한계인지 드러난다.

이후 포트폴리오 트랙으로 넘어가면 주제가 조금 달라진다. internals가 런타임의 설명 가능성을 다뤘다면, 다음 단계는 실제 제품처럼 읽히는 UI surface와 실패 복구 경험을 다루게 된다.
