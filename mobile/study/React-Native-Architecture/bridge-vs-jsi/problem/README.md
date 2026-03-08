# Problem: Bridge Vs JSI Benchmark

> Status: VERIFIED
> Scope: modernized benchmark spec
> Last Checked: 2026-03-08

## Objective

RN 0.84에서는 old/new runtime 자체를 토글하지 않는다.
대신 `Promise + serialized payload` 표면과 `sync direct-call` 표면을 같은 workload로 비교한다.

## Required Scope

1. async interop-style benchmark surface
2. sync TurboModule/JSI-style benchmark surface
3. 5-run statistics
4. dashboard summary
5. JSON export

## Test Criteria

1. 평균과 표준편차 계산이 정확하다.
2. async/sync surface가 같은 payload 크기를 사용한다.
3. export 결과가 deterministic JSON shape를 가진다.
4. docs가 “왜 runtime toggle을 하지 않는가”를 설명한다.

## Evaluation

```bash
make test
make app-build
make app-test
```
