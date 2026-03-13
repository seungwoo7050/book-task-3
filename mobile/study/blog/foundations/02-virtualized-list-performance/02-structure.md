# Structure Plan: 02 Virtualized List Performance

## 글의 중심 질문

- 이 프로젝트의 핵심은 FlashList를 도입했다는 사실이 아니라, baseline과 optimized가 정말 같은 조건을 쓰게 만들었느냐였다. 그래서 구현 순서도 데이터 고정 -> pagination 통제 -> benchmark export로 흘러간다.

## 구현 순서 요약

- deterministic dataset과 item height map을 먼저 만든다.
- 같은 `visibleItems`를 `FlatList`와 `FlashList`에 동시에 공급한다.
- delta 계산과 JSON export를 테스트와 artifact로 고정한다.

## 섹션 설계

1. Phase 1: seed 기반 data generator와 height map으로 비교 조건을 닫는다.
변경 단위: `react-native/src/listData.ts`
코드 앵커: `createDeterministicItems()`
2. Phase 2: shared pagination state와 dual renderer 화면을 연결한다.
변경 단위: `react-native/src/pagination.ts`, `react-native/src/VirtualizedListStudyApp.tsx`
코드 앵커: `const visibleItems = ITEMS.slice(...)`
3. Phase 3: benchmark delta를 계산하고 `summary.json`으로 내보낸다.
변경 단위: `react-native/src/benchmark.ts`, `react-native/scripts/benchmark-summary.mjs`, `react-native/tests/virtualized-list.test.tsx`
코드 앵커: `computeBenchmarkSummary()`

## 반드시 넣을 근거

- CLI: `npm run verify`
- verification: current replay 기준 `4`개 테스트 통과, benchmark summary 재생성
- artifact: `benchmarks/summary.json`
- concept: 이 프로젝트의 canonical evidence는 absolute FPS가 아니라 baseline 대비 개선 폭

## 개념 설명 포인트

- 새로 이해한 것: 리스트 성능 문제는 렌더러 선택이 아니라 비교 조건 설계 문제다
- 같은 dataset slice와 같은 pagination 규칙을 유지해야 mount count와 render delta가 해석 가능해진다

## 마무리 질문

- 다음 프로젝트에서는 같은 “비교 가능성” 원칙을 제스처와 spring 규칙 쪽으로 옮긴다.
