# 02 — Debug Log: 리스트 가상화 디버깅 기록

## Issue 1: FlashList에서 estimatedItemSize 경고

### 증상

FlashList를 처음 적용했을 때 콘솔에 다음 경고가 반복적으로 출력되었다:
```
FlashList: estimatedItemSize is not provided. This can affect performance.
```

### 원인

FlashList는 cell을 recycling하기 위해 대략적인 아이템 크기를 미리 알아야 한다.
`estimatedItemSize` prop이 없으면 첫 렌더링에서 몇 개의 cell을 측정한 뒤 추정하는데,
이 과정에서 빈 영역(blank area)이 발생할 수 있다.

### 해결

이 프로젝트에서는 `estimatedItemSize`를 명시적으로 넣는 대신,
`getItemType`으로 cell type을 분리하는 방식을 선택했다.
type별로 높이가 다르지만 같은 type 내에서는 높이가 일정하므로,
FlashList가 type별 크기를 빠르게 학습해 추정 정확도가 올라간다.

실무에서는 모든 아이템의 평균 높이를 `estimatedItemSize`로 넘기는 것이 가장 간단한 해결책이다:
```typescript
estimatedItemSize={(92 + 232 + 156) / 3}  // ≈ 160
```

### 교훈

FlashList의 경고는 무시하면 안 된다.
경고만 나오고 앱은 동작하지만 blank area가 늘고 스크롤 경험이 나빠진다.

---

## Issue 2: Cell recycling으로 인한 잔상 문제

### 증상

FlashList에서 빠르게 스크롤할 때, image type cell에 이전 text type의 layout이 잠깐 보이는 잔상이 발생했다.

### 원인

`getItemType`을 지정하지 않으면 FlashList가 모든 cell을 같은 type으로 취급해
text cell을 image cell에 재활용하게 된다.
recycling 시 이전 cell의 DOM 구조가 잠깐 보이다가 새 데이터로 업데이트되면서 깜빡임이 생긴다.

### 해결

`getItemType={item => item.type}`을 FlashList에 추가했다.
이렇게 하면 text, image, card 세 가지 recycling pool이 분리되어
같은 type의 cell만 서로 재활용한다.

```tsx
<FlashList
  data={visibleItems}
  renderItem={({ item }) => <ListCell item={item} />}
  getItemType={item => item.type}
  // ...
/>
```

### 교훈

`getItemType`은 FlashList 성능 최적화의 핵심이다.
리스트에 두 가지 이상의 cell layout이 있다면 반드시 type을 분리해야 한다.
type 분리가 없으면 recycling이 오히려 시각적 버그를 만들 수 있다.

---

## Issue 3: Pagination에서 마지막 페이지가 정확히 total에 도달하지 않는 문제

### 증상

total이 130이고 pageSize가 50일 때, 세 번째 `loadNextPage()` 호출 후 cursor가 150이 되어
`visibleItems = ITEMS.slice(0, 150)`에서 `ITEMS` 길이(130)를 초과하는 인덱스에 접근했다.

### 원인

초기 구현에서 `loadNextPage`가 단순히 `cursor + pageSize`를 반환했다.
`Math.min(total, ...)` 클램핑이 빠져 있었다.

### 해결

```typescript
export function loadNextPage(state: PaginationState): PaginationState {
  return {
    ...state,
    cursor: Math.min(state.total, state.cursor + state.pageSize),
  };
}
```

`Math.min`으로 cursor가 total을 넘지 않도록 보장했다.
`Array.prototype.slice`는 인덱스를 넘어도 에러를 던지지 않지만,
의미상 cursor가 total보다 큰 것은 잘못된 상태이므로 로직 레벨에서 막는 것이 맞다.

### 교훈

pagination은 경계 조건(boundary condition) 테스트가 필수다.
total이 pageSize의 배수가 아닌 경우를 반드시 테스트해야 한다.

---

## Issue 4: FlatList와 FlashList 전환 시 스크롤 위치가 유지되는 현상

### 증상

FlatList 모드에서 상당히 스크롤을 내린 뒤 FlashList 모드로 전환하면,
간혹 FlashList가 이전 스크롤 위치를 기억하고 있는 것처럼 보였다.

### 분석

React의 reconciliation이 원인이다. FlatList와 FlashList가 같은 위치에서 조건부 렌더링되면,
React가 내부 state를 일부 공유할 수 있다. `key` prop이 없으면 이전 컴포넌트의 state가 이어질 수 있다.

### 해결

mode 전환 시 각 리스트 컴포넌트에 고유한 `key`를 부여하는 것이 정석이지만,
이 프로젝트에서는 모드 전환 자체가 학습 목적이므로 스크롤 초기화보다는 두 엔진의 동작 차이 관찰에 집중했다.
실무에서는 `key={mode}`를 리스트 컴포넌트에 넣어 mode 전환 시 완전히 새로운 인스턴스를 만들어야 한다.

### 교훈

조건부 렌더링으로 컴포넌트를 교체할 때, 이전 컴포넌트의 state가 남아 있을 수 있다.
`key`를 사용해 명시적으로 인스턴스를 분리하는 것이 React의 올바른 패턴이다.
