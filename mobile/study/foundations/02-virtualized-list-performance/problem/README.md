# Problem: List Performance & Virtualization

> Status: VERIFIED
> Scope: baseline vs optimized list benchmark
> Last Checked: 2026-03-12

## 문제 요약

같은 10k 데이터셋을 `FlatList` baseline과 `FlashList v2` optimized path에 적용해
pagination, mount count, benchmark summary를 비교하는 앱을 만든다.

## 왜 이 문제가 커리큘럼에 필요한가

리스트 성능은 RN 기본기에서 가장 자주 체감되는 병목이다.
이 프로젝트는 "성능 문제를 감각이 아니라 같은 조건 비교와 artifact export로 설명할 수 있는가"를 확인한다.

## 제공 자료

- 기존 virtualized-list 과제 요구사항
- `problem/code/README.md`의 benchmark scaffold
- `problem/data/README.md`의 dataset 설명

## 필수 요구사항

1. seed 기준 deterministic mock data generator
2. `FlatList` baseline screen
3. `FlashList v2` optimized screen
4. cursor-style pagination state
5. benchmark summary 계산과 export

## 의도적 비범위

- 네트워크 기반 실측 수집
- 다중 디바이스 비교 저장소
- legacy FlashList v1 sizing 규칙 재도입

## 평가/검증 기준

```bash
make test
make app-build
make app-test
make benchmark
```

- baseline과 optimized가 같은 dataset slice를 써야 한다.
- summary export가 deterministic JSON shape를 가져야 한다.
- benchmark 재실행이 같은 계산 규칙을 유지해야 한다.

## 원문/출처 보존 위치

- [SOURCE-PROVENANCE.md](SOURCE-PROVENANCE.md)
- [code/README.md](code/README.md)
- [data/README.md](data/README.md)
