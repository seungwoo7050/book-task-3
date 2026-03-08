# Problem: List Performance & Virtualization

> Status: VERIFIED
> Scope: 문제 정의 + FlashList v2 기준 재구성
> Last Checked: 2026-03-08

## Objective

같은 10k dataset을 `FlatList` baseline과 `FlashList v2` optimized path에 적용해
pagination, mount count, benchmark summary를 비교하는 앱을 만든다.

## Required Scope

1. 결정적 mock data generator
2. `FlatList` baseline screen
3. `FlashList v2` optimized screen
4. cursor-style pagination state
5. benchmark summary export

## Modernization Rule

- public spec은 FlashList v2 기준으로 쓴다.
- legacy 문서의 v1 sizing 설명은 `docs/references/`의 archival reference로만 남긴다.
- repository-wide gate는 JS/type/test와 benchmark summary export다.

## Test Criteria

1. 10k data generator가 seed 기준으로 결정적이다.
2. baseline과 optimized가 같은 dataset slice를 사용한다.
3. pagination reducer가 end state를 정확히 계산한다.
4. benchmark summary가 개선 폭을 계산한다.
5. `make benchmark`가 summary JSON을 재생성한다.

## Evaluation

```bash
make test
make app-build
make app-test
make benchmark
```
