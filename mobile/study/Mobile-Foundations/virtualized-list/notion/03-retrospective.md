# 03 — Retrospective: 리스트 가상화 비교 회고

## 무엇을 만들었나

10,000개 아이템 데이터셋을 FlatList와 FlashList v2로 렌더링하는 비교 앱을 구현했다.
cursor 기반 pagination으로 50개씩 로딩하고, 합성 벤치마크 지표로 성능 차이를 정량화했다.
세 가지 cell type(text/image/card)을 순환 배치해 가상화 엔진의 크기 추정과 recycling 동작을 검증했다.

## 잘된 점

### 1. 결정적 데이터 생성기

`createDeterministicItems()`의 seed 기반 설계는 테스트와 벤치마크 모두에서 빛을 발했다.
같은 seed면 항상 같은 결과이므로, "flaky test" 걱정 없이 `toEqual` 비교가 가능하다.
`Math.random()`을 사용했다면 테스트를 snapshot 기반으로 바꿔야 했을 것이다.

### 2. Pagination의 순수 함수 설계

`PaginationState`를 React state와 분리한 것은 좋은 판단이었다.
`loadNextPage()`가 순수 함수이므로 UI 없이 상태 전이를 테스트할 수 있다.
같은 로직을 React 외에 다른 프레임워크에서도 그대로 쓸 수 있다.

### 3. 동일한 ListCell로 공정한 비교

FlatList와 FlashList가 완전히 동일한 `ListCell` 컴포넌트를 사용한다.
이것은 비교 실험에서 통제 변인을 최소화하는 기본 원칙이다.
렌더링 결과의 차이가 오직 가상화 엔진의 동작 차이에서만 온다는 것을 보장한다.

## 아쉬운 점

### 1. 합성 지표의 한계

`SAMPLE_BENCHMARK`의 값은 실제 디바이스 측정이 아니라 하드코딩된 대표값이다.
"FPS 47 vs 58"이라고 표시하지만 이 숫자가 어떤 디바이스에서 측정된 것인지 기록이 없다.
학습 목적으로는 충분하지만, 실무에서는 React Native Performance Monitor나 Flipper의 FPS 측정을 사용해야 한다.

### 2. benchmark 스크립트와 소스 코드의 중복

`benchmark.ts`의 `SAMPLE_BENCHMARK`과 `scripts/benchmark-summary.mjs`의 summary 객체가
동일한 값을 두 곳에서 관리하고 있다.
한쪽을 바꾸면 다른 쪽도 수동으로 맞춰야 한다.
Node.js 스크립트에서 TypeScript 소스를 직접 import할 수 없어서 생긴 구조적 한계다.

### 3. FlashList의 `overrideItemLayout` 미사용

FlashList v2는 `getItemType` 외에도 `overrideItemLayout`으로 아이템 크기를 정확하게 지정할 수 있다.
이 프로젝트에서는 `itemHeightForType()`이 있으므로 `overrideItemLayout`을 활용하면
blank area를 거의 0으로 줄일 수 있었을 것이다.

## 설계 판단 기록

### 왜 10k 아이템인가?

1,000개 정도에서는 FlatList도 충분히 빠르다.
차이가 눈에 보이려면 mount count가 유의미하게 누적되어야 하고,
10,000개는 "실제 앱에서 채팅 히스토리나 뉴스 피드가 충분히 도달할 수 있는 규모"다.

### 왜 cursor pagination인가?

무한 스크롤이 아니라 "다음 50개 불러오기" 버튼을 둔 이유는
pagination 상태 전이를 명시적으로 관찰하기 위해서다.
무한 스크롤은 `onEndReached`와 threshold 설정이 추가되어 핵심 비교에서 벗어난다.

### 왜 UI에서 benchmark를 표시하는가?

benchmark 결과를 콘솔이나 별도 파일로만 확인하면 "앱을 쓰는 관점"에서 체감하기 어렵다.
같은 화면에서 FlatList → FlashList → Benchmark Summary를 전환하면
"이 앱에서 어떤 엔진이 더 나은지"를 즉시 확인할 수 있다.

## FlatList vs FlashList: 핵심 차이 정리

| 측면 | FlatList | FlashList v2 |
|------|----------|--------------|
| Cell 관리 | mount/unmount (매번 새로 생성) | recycling (재사용) |
| 크기 추정 | 렌더링 후 측정 | estimatedItemSize + type별 pool |
| Type 분리 | 없음 | getItemType으로 recycling pool 분리 |
| Blank area | scroll 속도에 비례 | recycling으로 최소화 |
| Mount count | 높음 (10k → 1230회) | 낮음 (10k → 472회) |
| API 호환 | React Native 내장 | FlatList 호환 API + 추가 props |

## 다음 단계에서 시도할 것

1. **`overrideItemLayout` 적용**: type별 고정 높이를 FlashList에 직접 전달해 blank area 제거
2. **실제 디바이스 측정**: Flipper Performance Plugin으로 FPS, JS Thread 측정
3. **`onEndReached` 기반 무한 스크롤**: cursor pagination을 자동 트리거로 전환
4. **SectionList / FlashList sticky header**: group별 섹션 헤더 추가
