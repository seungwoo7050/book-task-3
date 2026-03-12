# Virtualized List Performance

Status: verified

## 한 줄 답

같은 10k 데이터셋을 `FlatList` baseline과 `FlashList v2` optimized path에 적용해 성능 차이를 재현 가능한 benchmark로 남긴 프로젝트다.

## 무슨 문제를 풀었나

대량 리스트는 "느리다"는 인상만으로는 학습 가치가 낮다.
이 프로젝트의 질문은 "같은 조건에서 baseline과 optimized 전략을 어떻게 비교하고, 그 차이를 숫자와 문서로 남길 수 있는가"다.

## 내가 만든 답

- seed 기반 deterministic mock data generator를 만들었다.
- baseline/optimized 화면이 동일한 dataset slice를 쓰도록 맞췄다.
- pagination state와 benchmark summary export를 구현했다.
- `make benchmark`로 비교 결과를 재생성하게 만들었다.

## 무엇이 동작하나

- 10k mock data 생성
- `FlatList` baseline screen
- `FlashList v2` optimized screen
- cursor-style pagination
- benchmark summary 계산과 export

## 검증 명령

```bash
make -C study/foundations/02-virtualized-list-performance/problem test
make -C study/foundations/02-virtualized-list-performance/problem app-build
make -C study/foundations/02-virtualized-list-performance/problem app-test
make -C study/foundations/02-virtualized-list-performance/problem benchmark
```

## 읽는 순서

1. [problem/README.md](problem/README.md)
2. [react-native/README.md](react-native/README.md)
3. [docs/README.md](docs/README.md)
4. [notion/README.md](notion/README.md)

## 학습 포인트

- 리스트 성능 문제를 느낌이 아니라 동일 조건 비교로 다루기
- measurement artifact를 저장소 안에 남기기
- modern RN 리스트 선택 기준을 문서로 고정하기

## 현재 상태

- 문제 정의: `verified`
- RN 구현: `verified`
- benchmark 문서화: `verified`
