# Modernized Runtime Benchmark

이 과제는 더 이상 legacy runtime 자체를 토글하지 않는다.

## Why

- 현재 저장소 baseline은 React Native `0.84.1`이다.
- 이 버전에서는 New Architecture-only 기준으로 생각하는 편이 자연스럽다.

## What The App Compares

- `async serialized`: Promise 기반, payload copy를 흉내 내는 surface
- `sync direct-call`: 즉시 값을 돌려주는 JSI-style surface

## What Still Matters

- 동일한 workload
- 5-run 평균과 표준편차
- export 가능한 결과물
