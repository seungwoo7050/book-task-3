# 02-virtualized-list-performance-react-native 문제지

## 왜 중요한가

리스트 성능은 RN 기본기에서 가장 자주 체감되는 병목이다. 이 프로젝트는 "성능 문제를 감각이 아니라 같은 조건 비교와 artifact export로 설명할 수 있는가"를 확인한다.

## 목표

같은 10k 데이터셋을 FlatList baseline과 FlashList v2 optimized path에 적용해 pagination, mount count, benchmark summary를 비교하는 앱을 만든다.

## 시작 위치

- `../study/foundations/02-virtualized-list-performance/react-native/src/benchmark.ts`
- `../study/foundations/02-virtualized-list-performance/react-native/src/listData.ts`
- `../study/foundations/02-virtualized-list-performance/react-native/src/pagination.ts`
- `../study/foundations/02-virtualized-list-performance/react-native/src/VirtualizedListStudyApp.tsx`
- `../study/foundations/02-virtualized-list-performance/react-native/tests/virtualized-list.test.tsx`
- `../study/foundations/02-virtualized-list-performance/problem/script/verify_task.sh`
- `../study/foundations/02-virtualized-list-performance/react-native/app.json`
- `../study/foundations/02-virtualized-list-performance/react-native/benchmarks/summary.json`

## starter code / 입력 계약

- `../study/foundations/02-virtualized-list-performance/react-native/src/benchmark.ts`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- 기존 virtualized-list 과제 요구사항
- seed 기준 deterministic mock data generator
- FlatList baseline screen
- FlashList v2 optimized screen

## 제외 범위

- `../study/foundations/02-virtualized-list-performance/problem/script/verify_task.sh` 등 fixture나 trace를 읽지 않고 동작을 추측해서 구현하지 않는다.
- 같은 주제의 다른 runtime 구현을 섞어 읽지 않는다.
- 검증 명령이 통과한다고 해서 입력 계약과 경계 조건까지 자동으로 맞는다고 가정하지 않는다.

## 성공 체크리스트

- 핵심 흐름은 `SAMPLE_BENCHMARK`와 `computeBenchmarkSummary`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `virtualized list study`와 `renders the shell`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../study/foundations/02-virtualized-list-performance/problem/script/verify_task.sh` 등 fixture/trace 기준으로 결과를 대조했다.
- `make test && make app-build && make app-test && make benchmark`가 통과한다.

## 검증 방법

```bash
make test && make app-build && make app-test && make benchmark
```

```bash
cd /Users/woopinbell/work/book-task-3/mobile/study/foundations/02-virtualized-list-performance/react-native && npm run test
```

```bash
cd /Users/woopinbell/work/book-task-3/mobile/study/foundations/02-virtualized-list-performance/react-native && npm run verify
```

- Node 계열 lab는 의존성 설치(`npm install` 등)가 끝난 뒤 검증 명령을 실행한다.
- Spring/Java 계열 검증은 `JDK/JRE`가 현재 머신에 설치돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`02-virtualized-list-performance-react-native_answer.md`](02-virtualized-list-performance-react-native_answer.md)에서 확인한다.
