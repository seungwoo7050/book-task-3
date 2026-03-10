# 00 — Problem Framing: 리스트 가상화 성능 비교

## 문제의 출발점

모바일 앱에서 "긴 리스트"는 가장 흔한 UI 패턴이면서 가장 쉽게 성능 병목이 되는 지점이다.
React Native의 `FlatList`는 가상화(windowing)를 기본 제공하지만,
대규모 데이터셋에서는 cell mount/unmount 빈도, blank area 발생, 메모리 사용량이 눈에 띄게 증가한다.

Shopify의 `FlashList`는 cell recycling 방식으로 이 문제에 접근한다.
기존 cell을 파괴하고 새로 만드는 대신, 화면 밖으로 나간 cell을 재사용해 mount 횟수를 줄인다.

이 프로젝트의 질문은 단순하다:
**같은 10,000개 아이템 데이터셋을 FlatList와 FlashList v2에 각각 넣으면, 어떤 차이가 발생하는가?**

## 왜 이 비교가 의미 있는가

1. **FlatList는 사실상 기본값이다** — React Native 프로젝트 대부분이 FlatList를 사용하고, 성능 문제가 생겨야 대안을 찾는다. 문제가 발생하기 전에 차이를 정량적으로 이해하면 기술 선택이 명확해진다.

2. **Cell recycling은 직관적이지 않다** — FlatList의 unmount/mount와 FlashList의 type별 recycling은 완전히 다른 모델이다. 코드를 직접 비교해봐야 동작 차이를 체감할 수 있다.

3. **Benchmark는 절대값보다 상대 비교가 중요하다** — 디바이스마다 절대 FPS나 메모리 수치는 다르지만, 같은 데이터셋에서 FlatList 대비 FlashList의 개선 비율은 일관된다.

## 설계 방향

### 데이터: 결정적 생성기

`createDeterministicItems(seed, count)`는 seed 기반으로 항상 같은 데이터를 생성한다.
`Math.sin(seed + index) * 10000`에서 소수 부분을 추출하는 간단한 pseudo-random이다.
같은 seed, 같은 count면 항상 같은 결과가 나오므로 테스트 재현성이 보장된다.

아이템은 세 가지 타입(text/image/card)을 순환하며,
각 타입에 따라 높이가 다르다 (text: 92px, image: 232px, card: 156px).
이 다양한 높이가 가상화 엔진의 크기 추정 정확도를 시험한다.

### Pagination: 커서 기반 상태 머신

한 번에 10k 개를 렌더링하지 않고, PAGE_SIZE(50개)씩 로딩하는 커서 pagination을 구현한다.
`PaginationState`는 `{ cursor, pageSize, total }` 세 값만 가지는 순수 상태 객체이고,
`loadNextPage()`가 새 상태를 반환하는 reducer 패턴이다.

이 구조가 중요한 이유는 FlatList와 FlashList가 **동일한 데이터 슬라이스**를 사용하도록 보장하기 때문이다.
pagination이 별도로 관리되면 비교가 공정하지 않을 수 있다.

### Benchmark: 합성 지표

디바이스 실측은 환경에 따라 달라지므로, 학습 목적의 벤치마크는 합성(synthetic) 지표를 사용한다.
`SAMPLE_BENCHMARK`에 FlatList와 FlashList의 대표적인 측정값을 하드코딩하고,
`computeBenchmarkSummary()`가 개선 폭(delta)을 계산한다.

측정 항목:
- FPS (프레임율)
- Initial render time (첫 화면 렌더링 시간)
- Blank area duration (스크롤 시 빈 영역 노출 시간)
- Peak memory (최대 메모리 사용량)
- Mount count (cell 컴포넌트 mount 횟수)

## 학습 범위

| 영역 | 구체적 목표 |
|------|-------------|
| 데이터 | seed 기반 결정적 10k 아이템 생성, 3가지 타입별 높이 분리 |
| Pagination | cursor 기반 순수 함수 상태 관리, 완료 판정 |
| FlatList | baseline 렌더링, keyExtractor, ListFooterComponent |
| FlashList v2 | cell recycling, getItemType, estimatedItemSize |
| Benchmark | 합성 지표 기반 개선 폭 계산, JSON export |
