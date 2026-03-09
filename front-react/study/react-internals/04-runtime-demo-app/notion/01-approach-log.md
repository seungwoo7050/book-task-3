# 접근 기록 — demo app 구현 과정

## 데이터 설계: 10개의 의도된 아이템

가장 먼저 data.ts에 DemoItem 배열을 만들었다. 10개의 아이템이 6개 카테고리(metrics, interaction, search, pagination, effects, integration, limitations)에 걸쳐 있다.

이 데이터는 무작위가 아니다. 각 아이템이 runtime의 특정 측면을 설명하는 내용을 담고 있다. "Render Inspector"는 metrics 카테고리이고, "Debounce Loop"은 search 카테고리다. 사용자가 검색할 때 카테고리별로 필터링되면 runtime의 어떤 부분이 동작하는지 자기 설명적으로 보인다.

이 아이템이 PAGE_SIZE(4) 단위로 나뉘므로, 10개 아이템에서 첫 페이지 4개, Load more 후 8개, 다시 한 번 누르면 전부 — 이 세 단계가 자연스럽게 만들어진다.

## useDebouncedValue: 커스텀 hook의 첫 실전

커스텀 hook을 만드는 것 자체는 간단하지만, 이것이 작동한다는 건 runtime이 "hook 안에서 hook을 호출하는 패턴"을 지원한다는 뜻이다.

```typescript
function useDebouncedValue<T>(value: T, delayMs: number): T {
  const [debounced, setDebounced] = useState(value);
  useEffect(() => {
    const timeoutId = window.setTimeout(() => setDebounced(value), delayMs);
    return () => window.clearTimeout(timeoutId);
  }, [value, delayMs]);
  return debounced;
}
```

useState로 debounced 값을 저장하고, useEffect로 타이머를 관리한다. value가 바뀔 때마다 이전 타이머를 cleanup(clearTimeout)하고 새 타이머를 설정한다.

이 패턴이 작동하려면 effect cleanup이 정확한 시점에 실행되어야 한다. 03-hooks-and-events에서 구현한 "이전 cleanup → 새 setup" 순서가 여기서 실전 검증된다.

## DemoApp 컴포넌트: 상태 조합

DemoApp은 네 개의 상태를 관리한다:
- `query`: 입력 필드의 실시간 값
- `debouncedQuery`: 250ms 후에 확정되는 검색어 (useDebouncedValue)
- `visibleCount`: 현재 보이는 아이템 수
- `metrics`: DemoMetrics 객체 (renderCount, lastCommitMs, visibleCount, matchCount, activeQuery)

상태 간의 연결:
1. query → useDebouncedValue → debouncedQuery
2. debouncedQuery가 바뀌면 → useEffect로 visibleCount를 PAGE_SIZE로 리셋
3. debouncedQuery, visibleItems.length, filteredItems.length가 바뀌면 → useEffect로 metrics 갱신
4. metrics 갱신 시 performance.now()로 현재 렌더의 시작 시점과의 차이를 commit 시간으로 기록

이 연쇄가 하나의 render cycle 안에서 일어난다. query가 바뀌면 → 즉시 렌더 → debounce 효과는 아직 → 250ms 후 debouncedQuery 갱신 → 다시 렌더 → visibleCount 리셋 + metrics 갱신 → 또 렌더.

## createElement의 함수형 UI 작성

React의 JSX 없이 createElement 호출만으로 UI를 작성한다. header, section, aside, button, input, ul, li — 모든 UI가 createElement 체인이다.

이 방식의 장점은 runtime이 정확히 어떤 VNode을 받는지 숨김 없이 보인다는 것이다. `createElement("button", { onClick: handler }, text)` — 이 호출이 VNode을 만들고, resolveNode가 RuntimeNode로 변환하고, handler가 delegated event로 등록되는 전체 과정이 createElement로부터 시작된다.

## 검색 흐름

```
사용자 입력 → onInput handler → setQuery → 즉시 렌더
→ 250ms 대기 → setTimeout 발동 → setDebounced → 재렌더
→ filteredItems 재계산 → visibleCount 리셋 → DOM 업데이트
→ metrics 갱신 → 또 DOM 업데이트
```

검색 결과는 `DEMO_ITEMS.filter()`로 계산한다. title, category, excerpt를 합쳐 소문자로 변환한 뒤 includes로 검색한다.

빈 검색어면 전체 아이템을 보여 주고, `normalizedQuery`가 있으면 필터링한다. 결과가 0개면 "No demo items match the current query" 메시지를 보여 주고, 있으면 Load more 버튼을 보여 준다.

## pagination 흐름

```
Load more 클릭 → setVisibleCount(count => count + PAGE_SIZE)
→ 재렌더 → filteredItems.slice(0, 새 visibleCount) → DOM 업데이트
→ hasMore가 false면 버튼 disabled
```

`hasMore = visibleItems.length < filteredItems.length`로 더 가져올 항목이 있는지 판단한다. 버튼 텍스트도 조건부: "Load more results" vs "All results loaded".

검색어가 바뀌면 visibleCount가 PAGE_SIZE로 리셋되므로, 새 검색 결과는 항상 첫 페이지부터 시작한다.

## metrics panel

metrics는 앱 상태로 관리하는 "관찰값"이다. runtime에 profiler API가 없으므로, 렌더 시작 시점에 `performance.now()`를 찍고 effect에서 다시 찍어 차이를 계산한다.

```typescript
const renderStartedAt = performance.now();
// ... 렌더 로직 ...
useEffect(() => {
  updateMetrics(setMetrics, renderStartedAt, visibleItems.length, ...);
}, [normalizedQuery, visibleItems.length, filteredItems.length]);
```

이 방식은 정확하지 않다 — effect는 commit 후에 실행되므로, render phase의 시간과 commit phase의 시간이 합산된다. 하지만 "얼마나 가벼운가"가 아니라 "이 상호작용이 재렌더를 trigger하는가"를 보여 주는 게 목적이므로 충분하다.

## mountRuntimeDemo / resetRuntimeDemo

render와 resetRuntime을 감싸는 진입점 함수다. main.ts에서 DOM을 찾고 mountRuntimeDemo를 호출한다. 테스트에서는 resetRuntimeDemo로 상태를 초기화한다.

이 패턴이 "앱 코드는 runtime API만 알면 된다"는 경계의 실체다. mountRuntimeDemo는 createElement와 render 두 함수만 쓴다.
