# Evidence Ledger: 02 Virtualized List Performance

## 독립 프로젝트 판정

- 판정: 처리
- 근거: 자체 `README.md`, benchmark 문제 정의, `react-native/scripts/benchmark-summary.mjs`, 테스트, committed benchmark artifact를 모두 갖춘 독립 실험 앱이다.
- 소스 경로: `mobile/study/foundations/02-virtualized-list-performance`

## 사용한 근거

- `mobile/study/foundations/02-virtualized-list-performance/README.md`
- `mobile/study/foundations/02-virtualized-list-performance/problem/README.md`
- `mobile/study/foundations/02-virtualized-list-performance/react-native/README.md`
- `mobile/study/foundations/02-virtualized-list-performance/docs/concepts/flashlist-v2-benchmarking.md`
- `mobile/study/foundations/02-virtualized-list-performance/react-native/src/listData.ts`
- `mobile/study/foundations/02-virtualized-list-performance/react-native/src/pagination.ts`
- `mobile/study/foundations/02-virtualized-list-performance/react-native/src/benchmark.ts`
- `mobile/study/foundations/02-virtualized-list-performance/react-native/src/VirtualizedListStudyApp.tsx`
- `mobile/study/foundations/02-virtualized-list-performance/react-native/tests/virtualized-list.test.tsx`
- `mobile/study/foundations/02-virtualized-list-performance/react-native/benchmarks/summary.json`

## CLI Replay

```bash
cd /Users/woopinbell/work/book-task-3/mobile/study/foundations/02-virtualized-list-performance/react-native
npm install --no-audit --no-fund
npm run verify
```

## Chronology Ledger

### Phase 1 | 같은 데이터셋을 재생할 수 있게 만든다

- 당시 목표: baseline과 optimized가 같은 조건을 쓰도록 deterministic dataset과 height map을 만든다.
- 변경 단위: `react-native/src/listData.ts`
- 처음 가설: 10k 리스트 비교는 데이터 생성 규칙이 먼저 닫히지 않으면 숫자 자체가 의미를 잃는다.
- 실제 조치: `createDeterministicItems(seed, count)`와 `itemHeightForType()`를 두고 item id, type, subtitle, tags, timestamp를 seed 기반으로 고정했다.
- CLI:
```bash
npm run typecheck
```
- 검증 신호:
- `createDeterministicItems(24, 3)`는 항상 같은 배열을 만든다.
- `itemHeightForType()`이 각 item type의 높이를 분기해 baseline/optimized가 같은 셀 조건을 쓴다.
- 핵심 코드 앵커:
```ts
return {
  id: `item-${seed}-${index}`,
  type,
  title: `${type.toUpperCase()} item ${index + 1}`,
  subtitle: `seed:${seed} sample:${sample}`,
};
```
- 새로 배운 것: 리스트 성능 비교의 첫 단계는 렌더러 선택이 아니라 데이터 조건의 고정이다.
- 다음: 이 데이터셋을 pagination과 두 list surface 위에 올린다.

### Phase 2 | FlatList와 FlashList를 같은 화면 규칙으로 맞춘다

- 당시 목표: baseline과 optimized를 같은 page size, 같은 footer interaction으로 비교한다.
- 변경 단위: `react-native/src/pagination.ts`, `react-native/src/VirtualizedListStudyApp.tsx`
- 처음 가설: 데이터는 같아도 page cursor가 다르면 mount 수와 perceived performance 비교가 흔들린다.
- 실제 조치: `createPaginationState()`, `loadNextPage()`, `isPaginationComplete()`를 만들고, 앱에서 `mode === 'flat' | 'flash' | 'summary'`를 전환해 같은 `visibleItems`를 두 renderer에 그대로 공급했다.
- CLI:
```bash
npm test
```
- 검증 신호:
- `createPaginationState(130, 50)`는 `50 -> 100 -> 130`으로만 진행한다.
- summary 화면과 두 list 화면이 모두 같은 `visibleItems`를 공유한다.
- 핵심 코드 앵커:
```ts
const visibleItems = ITEMS.slice(0, pagination.cursor);
...
<FlatList data={visibleItems} ... />
...
<FlashList data={visibleItems} ... />
```
- 새로 배운 것: baseline/optimized 비교에서 중요한 것은 라이브러리 차이보다 shared slice를 유지하는 통제 장치다.
- 다음: benchmark delta를 JSON artifact로 고정한다.

### Phase 3 | benchmark summary를 artifact로 남긴다

- 당시 목표: 감각 대신 재생 가능한 숫자와 테스트를 남긴다.
- 변경 단위: `react-native/src/benchmark.ts`, `react-native/tests/virtualized-list.test.tsx`, `react-native/scripts/benchmark-summary.mjs`, `react-native/benchmarks/summary.json`
- 처음 가설: 공용 게이트가 device profiler가 아니라면, synthetic metric이라도 summary export가 deterministic해야 한다.
- 실제 조치: `computeBenchmarkSummary()`로 fps/render/blank-area/memory/mount delta를 계산하고, `benchmark-summary.mjs`가 이를 `benchmarks/summary.json`으로 다시 쓴다.
- CLI:
```bash
npm run verify
```
- 검증 신호:
- current replay에서 `PASS tests/virtualized-list.test.tsx`
- `Test Suites: 1 passed`, `Tests: 4 passed`
- `benchmark summary written to benchmarks/summary.json`
- artifact 값은 `fps 47 -> 58`, `mountCount 1230 -> 472`
- 핵심 코드 앵커:
```ts
return {
  fpsGain: flashList.fps - flatList.fps,
  renderGainMs: flatList.initialRenderMs - flashList.initialRenderMs,
  mountSavings: flatList.mountCount - flashList.mountCount,
};
```
- 새로 배운 것: 이 프로젝트의 canonical evidence는 절대 수치보다 baseline 대비 개선 폭이다.
- 다음: 다음 프로젝트에서는 스크롤 성능 대신 threshold, spring, dismiss처럼 손맛에 가까운 상호작용 규칙을 다룬다.
