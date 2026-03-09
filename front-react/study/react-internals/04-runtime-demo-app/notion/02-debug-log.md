# 디버그 기록 — demo app에서 마주친 문제들

## debounce timer cleanup이 되지 않아 이전 검색어가 반영됨

### 증상

"met"을 입력한 뒤 바로 "eff"로 바꿨는데, 250ms 후에 "met" 기준의 필터링 결과가 먼저 나타났다가 다시 "eff" 결과로 바뀌었다. 화면이 두 번 깜빡였다.

### 원인

useDebouncedValue의 useEffect에서 cleanup(clearTimeout)을 반환하지 않고 있었다. 이전 타이머가 그대로 남아서 먼저 발동한 뒤, 새 타이머도 나중에 발동하는 상황이었다.

### 해결

```typescript
useEffect(() => {
  const timeoutId = window.setTimeout(() => setDebounced(value), delayMs);
  return () => window.clearTimeout(timeoutId);
}, [value, delayMs]);
```

cleanup에서 이전 타이머를 제거한다. 03-hooks-and-events의 effect lifecycle(이전 cleanup → 새 setup)이 정확히 이 시점에 작동한다. value가 바뀌면 이전 effect의 clearTimeout이 먼저 실행되고, 새 setTimeout이 설정된다.

## query 변경 후 visibleCount가 리셋되지 않음

### 증상

10개 아이템에서 Load more를 두 번 눌러 전체를 보이게 한 뒤, 검색어를 입력하면 결과가 2개인데 "Showing 2 of 2 matches"가 아닌 "Showing 2 of 2 matches"로 보이지만 visibleCount가 10인 상태였다. 다른 검색어로 바꾸면 처음부터 전체가 보이는 문제.

### 원인

debouncedQuery가 바뀔 때 visibleCount를 PAGE_SIZE로 리셋하는 effect가 없었다. visibleCount가 이전 값(8이나 10)을 유지하고 있었다.

### 해결

```typescript
useEffect(() => {
  setVisibleCount(PAGE_SIZE);
}, [normalizedQuery]);
```

검색어가 바뀌면 반드시 첫 페이지부터 시작한다. 이 effect는 debouncedQuery 기반이므로, 타이핑 중에는 리셋되지 않고 debounce 후에만 리셋된다.

## metrics가 무한 루프에 빠짐

### 증상

render가 멈추지 않고 무한 반복됐다. 콘솔에 metrics 변경 로그가 계속 찍혔다.

### 원인

metrics를 갱신하는 useEffect가 매 렌더마다 실행됐다. metrics가 바뀌면 재렌더 → 재렌더에서 또 metrics 갱신 → 무한 루프.

초기에 useEffect의 deps를 `[metrics]`로 잡았거나, deps 없이 호출한 것이 원인이었다.

### 해결

metrics 갱신 effect의 deps를 `[normalizedQuery, visibleItems.length, filteredItems.length]`로 변경. metrics 자체가 아니라 metrics를 결정하는 입력값에만 반응한다.

```typescript
useEffect(() => {
  updateMetrics(setMetrics, renderStartedAt, visibleItems.length, filteredItems.length, normalizedQuery || "all");
}, [normalizedQuery, visibleItems.length, filteredItems.length]);
```

metrics가 바뀌어도 이 effect는 다시 실행되지 않는다. deps에 metrics가 없기 때문이다.

## fake timer와 debounce 테스트

### 증상

demo.test.ts에서 debounce 후 결과를 검증하려는데, `vi.useFakeTimers()` 후에 `vi.advanceTimersByTimeAsync(260)`을 호출해도 debouncedQuery가 업데이트되지 않았다.

### 원인

두 가지 이유가 있었다:
1. `window.setTimeout`을 사용하는데, Vitest의 fake timer가 `globalThis.setTimeout`만 mock하고 `window.setTimeout`을 놓치는 경우
2. `advanceTimersByTime`(동기 버전)을 사용해서 Promise 기반 state update가 처리되지 않는 경우

### 해결

`vi.advanceTimersByTimeAsync(260)`을 사용한다(비동기 버전). 260ms는 DEBOUNCE_MS(250)보다 조금 크게 잡아 타이머가 확실히 발동되게 한다.

```typescript
await vi.advanceTimersByTimeAsync(260);
```

jsdom 환경에서는 window와 globalThis가 같은 객체이므로 첫 번째 문제는 자연스럽게 해결된다.

## input 이벤트가 delegated event로 처리 안 됨

### 증상

검색 input에 값을 입력해도 onInput이 호출되지 않았다. click은 되는데 input 이벤트만 안 됐다.

### 원인

onInput 핸들러의 `event` 파라미터 타입이 DelegatedEvent인데, handler에서 `event.currentTarget`을 `HTMLInputElement`로 접근하려고 했다. DelegatedEvent의 currentTarget은 `EventTarget | null`이므로 value 속성이 없었다.

### 해결

handler의 타입을 명시적으로 지정:

```typescript
onInput: (event: { currentTarget: HTMLInputElement | null }) =>
  setQuery(event.currentTarget?.value ?? ""),
```

DelegatedEvent 래퍼가 currentTarget을 DOM 노드로 설정하므로, 런타임에서는 실제로 HTMLInputElement가 들어온다. 타입을 좁혀서 value에 접근한다.

## performance.now()의 위치

### 증상

metrics panel의 lastCommitMs가 항상 0에 가까운 값이었다.

### 원인

`renderStartedAt`을 컴포넌트 함수 밖에서(모듈 레벨) 한 번만 찍고 있었다. 모든 렌더에서 같은 시작 시간을 참조하므로 의미 있는 차이가 나지 않았다.

### 해결

`renderStartedAt`을 DemoApp 함수 본문 첫 줄에 놓았다:

```typescript
function DemoApp() {
  const renderStartedAt = performance.now();
  // ...
}
```

함수 컴포넌트는 매 렌더마다 호출되므로, 매번 새로운 시작 시간이 찍힌다. effect에서 `performance.now() - renderStartedAt`을 계산하면 해당 렌더의 render+commit 시간이 나온다.
