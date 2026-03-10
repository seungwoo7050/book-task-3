# 01 — Approach Log: 리스트 가상화 구현 과정

## Phase 1: 결정적 데이터 생성기 — listData.ts

첫 번째로 만든 것은 리스트 데이터 모델이다.

`StudyListItem` 인터페이스는 실제 앱의 피드 아이템을 간략화한 구조다:
`id`, `type`(text/image/card), `title`, `subtitle`, `imageUrl`, `tags`, `timestamp`.
세 가지 type은 `index % 3`으로 순환 배정되어 리스트에 균등하게 섞인다.

`seededFloat(seed)` 함수가 핵심이다.
`Math.sin(seed) * 10000`의 소수 부분을 반환하는 방식으로,
`Math.random()` 없이도 재현 가능한 유사 난수를 생성한다.
seed와 index를 조합하면 각 아이템이 고유하면서도 결정적인 값을 갖는다.

`itemHeightForType()` 함수는 type별로 고정 높이를 반환한다.
text는 92px, image는 232px, card는 156px.
이 정보는 FlashList의 `estimatedItemSize` 계산과 UI cell의 `minHeight`에 모두 사용된다.

10,000개 아이템을 seed 24로 생성하는 결과는 항상 동일하다.
테스트에서 `createDeterministicItems(24, 3)`을 두 번 호출해도 `toEqual`이 통과한다.

## Phase 2: Pagination 상태 관리 — pagination.ts

pagination은 의도적으로 순수 함수로 설계했다.

`PaginationState`는 세 개의 숫자만 가진다: `cursor`(현재까지 로딩된 아이템 수), `pageSize`(페이지 크기), `total`(전체 수).
초기 상태를 만드는 `createPaginationState(total, pageSize)`는 cursor를 첫 페이지 크기(pageSize)로 설정한다.
즉, 앱이 시작하면 첫 50개가 바로 보인다.

`loadNextPage(state)`는 cursor를 pageSize만큼 전진시키되, total을 넘지 않도록 `Math.min`으로 클램핑한다.
`isPaginationComplete(state)`는 cursor가 total에 도달했는지 확인한다.

이 패턴의 장점은 **테스트가 쉽다**는 것이다.
```
initial: { cursor: 50, pageSize: 50, total: 130 }
→ loadNextPage → { cursor: 100, ... }
→ loadNextPage → { cursor: 130, ... }
→ isPaginationComplete → true
```
순수 함수이므로 UI 없이 로직만 검증할 수 있다.

## Phase 3: Benchmark 지표 계산 — benchmark.ts

`SAMPLE_BENCHMARK`는 FlatList와 FlashList의 대표적인 성능 측정값을 하드코딩한 객체다.
`satisfies Record<string, BenchmarkMetric>`으로 타입 안전성을 확보하면서 `as const`와 유사한 구체 타입을 유지한다.

`computeBenchmarkSummary(flatList, flashList)`는 다섯 가지 개선 폭을 계산한다:

| 지표 | FlatList | FlashList | Delta |
|------|----------|-----------|-------|
| FPS | 47 | 58 | +11 |
| Initial render | 222ms | 141ms | -81ms |
| Blank area | 61ms | 18ms | -43ms |
| Peak memory | 188MB | 134MB | -54MB |
| Mount count | 1230 | 472 | -758 |

delta가 양수면 FlashList가 더 좋다는 의미다.
모든 지표에서 FlashList가 우세한 것은 cell recycling의 효과를 명확히 보여준다.

왜 합성 지표인가?
이 저장소의 CI 게이트는 JS/type/test 기반이다.
디바이스 실측은 환경에 따라 달라지므로 CI에 넣을 수 없다.
대신 결정적 샘플 값으로 "개선 폭 계산 로직"이 올바른지를 검증한다.

## Phase 4: UI 조립 — VirtualizedListStudyApp.tsx

앱은 세 가지 모드(flat/flash/summary)를 Chip 버튼으로 전환한다.

### FlatList 모드

```tsx
<FlatList
  data={visibleItems}
  renderItem={({ item }) => <ListCell item={item} />}
  keyExtractor={item => item.id}
  ListFooterComponent={<Footer ... />}
/>
```

기본 FlatList는 `keyExtractor`와 `renderItem`만 있으면 동작한다.
별도 최적화 없이 mount/unmount 기반으로 cell을 관리한다.

### FlashList 모드

```tsx
<FlashList
  data={visibleItems}
  renderItem={({ item }) => <ListCell item={item} />}
  keyExtractor={item => item.id}
  getItemType={item => item.type}
  ListFooterComponent={<Footer ... />}
/>
```

FlashList의 핵심 차이는 `getItemType`이다.
이 함수가 cell의 type을 반환하면, FlashList는 같은 type의 cell만 재활용한다.
text cell이 화면 밖으로 나가면 다음에 표시할 text cell에 데이터만 바꿔 넣고 DOM 트리를 유지한다.
다른 type(image/card)의 cell을 text cell에 재활용하지 않으므로 레이아웃이 깨지지 않는다.

### Benchmark Summary 모드

chip에서 "Benchmark"를 누르면 리스트 대신 `computeBenchmarkSummary()` 결과를 카드로 보여준다.
FPS gain, render gain, blank area gain, memory gain, mount savings 다섯 가지 delta가 한눈에 보인다.

### ListCell 컴포넌트

모든 아이템에 공통으로 사용되는 cell 컴포넌트다.
`minHeight: itemHeightForType(item.type)`으로 type별 높이를 강제하고,
type badge, title, subtitle, tags를 표시한다.
FlatList와 FlashList가 동일한 `ListCell`을 사용하므로 렌더링 결과의 차이는 순수하게 가상화 엔진의 차이다.

### Footer 컴포넌트

pagination이 완료되면 "모든 항목을 불러왔습니다"를 표시하고,
아직 남아있으면 "다음 50개 항목 불러오기" 버튼을 보여준다.
`ListFooterComponent`로 FlatList와 FlashList 모두에 동일하게 적용된다.

## Phase 5: Benchmark Export 스크립트

`scripts/benchmark-summary.mjs`는 Node.js 스크립트로 `benchmarks/summary.json`을 생성한다.
CI에서 `npm run benchmark` 또는 `make benchmark`로 실행되며,
벤치마크 결과를 JSON 파일로 내보내 외부 도구나 문서에서 참조할 수 있게 한다.

스크립트의 지표 값은 `benchmark.ts`의 `SAMPLE_BENCHMARK`과 동일하다.
양쪽을 동기화해야 하는 번거로움이 있지만,
JS 빌드 없이 Node.js만으로 실행 가능하다는 장점이 있다.

## 테스트 구조

`virtualized-list.test.tsx`는 네 개 테스트를 가진다:

1. **렌더링 셸 확인**: App을 렌더링하고 제목과 chip 텍스트가 존재하는지 검증
2. **결정적 데이터 검증**: 같은 seed/count로 두 번 호출해 동일한 결과 확인
3. **Pagination 상태 머신**: 130개 아이템을 50개씩 로딩하면 3번째 페이지에서 complete
4. **Benchmark delta 계산**: 모든 개선 폭이 양수인지 검증
