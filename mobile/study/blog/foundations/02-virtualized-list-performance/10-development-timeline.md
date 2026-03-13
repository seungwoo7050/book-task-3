# 02 Virtualized List Performance

대량 리스트 프로젝트는 쉽게 “FlashList가 더 빠르다” 같은 결론 요약으로 끝난다. 이 프로젝트가 더 중요하게 본 것은 그 결론을 어떤 조건으로 증명할 수 있느냐였다. 그래서 구현 순서를 일부러 데이터 고정 -> pagination 통제 -> benchmark export 순으로 잡았다.

## 이번 글에서 따라갈 구현 순서

- deterministic dataset과 item height map을 먼저 만든다.
- 같은 `visibleItems`를 `FlatList` baseline과 `FlashList v2` optimized 화면에 같이 올린다.
- benchmark delta를 계산해 JSON artifact와 테스트로 고정한다.

## 새로 이해한 것: baseline과 optimized는 같은 slice를 써야 비교가 된다

이 프로젝트의 핵심은 `FlashList` 채택 자체가 아니다. `ITEMS.slice(0, pagination.cursor)` 같은 shared slice를 유지해 두 renderer가 같은 조건을 보게 만드는 것이 먼저였다. 그래야 mount count, render time, blank area 같은 숫자가 나중에 의미를 가진다.

## Phase 1
### deterministic dataset과 height map을 먼저 만든다

- 당시 목표: baseline과 optimized가 같은 10k 데이터셋을 쓰도록 데이터 생성 규칙을 먼저 잠근다.
- 변경 단위: `react-native/src/listData.ts`
- 처음 가설: 데이터 생성 규칙이 흔들리면 어떤 렌더러가 더 나은지 비교할 근거가 없다.
- 실제 진행: `createDeterministicItems(seed, count)`가 `id`, `type`, `subtitle`, `tags`, `timestamp`를 seed 기반으로 만들고, `itemHeightForType()`이 각 카드 높이를 고정했다.

CLI:

```bash
cd /Users/woopinbell/work/book-task-3/mobile/study/foundations/02-virtualized-list-performance/react-native
npm run typecheck
```

검증 신호:

- `createDeterministicItems(24, 3)`는 반복 호출해도 같은 결과를 만든다.
- 각 item type은 고정 height를 가져 renderer 비교의 입력 조건이 된다.

핵심 코드:

```ts
return {
  id: `item-${seed}-${index}`,
  type,
  title: `${type.toUpperCase()} item ${index + 1}`,
  subtitle: `seed:${seed} sample:${sample}`,
};
```

왜 이 코드가 중요했는가:

비교의 출발점을 “같은 데이터셋”으로 잠그는 순간, 이후의 성능 차이는 renderer 쪽에서 해석할 수 있게 된다.

새로 배운 것:

- 리스트 성능 문제의 첫 단계는 최적화가 아니라 실험 통제다.

다음:

- 이 데이터셋을 같은 pagination state와 함께 두 renderer에 올린다.

## Phase 2
### shared pagination state로 두 renderer를 맞춘다

- 당시 목표: baseline과 optimized가 page size와 load-more 동작까지 같게 움직이게 만든다.
- 변경 단위: `react-native/src/pagination.ts`, `react-native/src/VirtualizedListStudyApp.tsx`
- 처음 가설: renderer만 같고 pagination이 다르면 mount 수나 체감 속도를 공정하게 읽을 수 없다.
- 실제 진행: `createPaginationState()`, `loadNextPage()`, `isPaginationComplete()`를 만들고, 앱은 하나의 `visibleItems`를 `FlatList`와 `FlashList`에 번갈아 공급했다. summary 모드에서는 같은 입력 조건을 전제로 delta만 읽게 했다.

CLI:

```bash
npm test
```

검증 신호:

- current replay에서 pagination 테스트가 `50 -> 100 -> 130` cursor progression을 통과했다.
- shell 렌더 테스트가 `FlatList`, `FlashList v2`, `Benchmark` 세 모드를 모두 확인했다.

핵심 코드:

```ts
const visibleItems = ITEMS.slice(0, pagination.cursor);
...
<FlatList data={visibleItems} ... />
...
<FlashList data={visibleItems} ... />
```

왜 이 코드가 중요했는가:

비교 대상이 라이브러리 두 개가 아니라 “같은 slice를 소비하는 두 전략”으로 바뀌는 지점이기 때문이다.

새로 배운 것:

- pagination state를 공유해야 renderer 비교가 숫자 이상의 설명력을 가진다.

다음:

- delta 계산과 export를 artifact로 남겨 benchmark를 문장 밖으로 꺼낸다.

## Phase 3
### benchmark summary를 artifact로 남긴다

- 당시 목표: 성능 차이를 요약문이 아니라 JSON artifact와 테스트로 재생한다.
- 변경 단위: `react-native/src/benchmark.ts`, `react-native/scripts/benchmark-summary.mjs`, `react-native/tests/virtualized-list.test.tsx`, `react-native/benchmarks/summary.json`
- 처음 가설: device profiler가 공용 게이트가 아니라면, synthetic metric이라도 deterministic summary가 필요하다.
- 실제 진행: `computeBenchmarkSummary()`로 fps/render/blank-area/memory/mount delta를 계산하고, `benchmark-summary.mjs`가 현재 summary를 다시 써서 `benchmarks/summary.json`으로 내보내게 했다.

CLI:

```bash
npm run verify
```

검증 신호:

- current replay에서 `PASS tests/virtualized-list.test.tsx`
- `Test Suites: 1 passed`
- `Tests: 4 passed`
- `benchmark summary written to benchmarks/summary.json`
- artifact 값은 `fps 47 -> 58`, `render 222ms -> 141ms`, `mountCount 1230 -> 472`

핵심 코드:

```ts
return {
  fpsGain: flashList.fps - flatList.fps,
  renderGainMs: flatList.initialRenderMs - flashList.initialRenderMs,
  mountSavings: flatList.mountCount - flashList.mountCount,
};
```

왜 이 코드가 중요했는가:

이 함수가 baseline과 optimized의 차이를 “더 빠르다”가 아니라 “얼마나, 어떤 항목에서, 어떤 방향으로”로 바꿔 준다.

새로 배운 것:

- 이 프로젝트의 canonical evidence는 절대 수치 하나가 아니라 baseline 대비 개선 폭이다.

다음:

- 다음 단계에서는 스크롤 성능 대신 swipe, reorder, dismiss처럼 제스처 규칙을 공용 vocabulary로 묶는다.

## 여기까지 정리

- 이 프로젝트가 실제로 해결한 것은 리스트 최적화 자체보다, 비교 가능한 조건과 artifact를 함께 설계하는 방법이었다.
- 다음 단계의 질문: 체감 품질은 숫자 대신 어떤 규칙과 테스트로 고정할 수 있을까?
