# Bridge Vs JSI

Status: verified

## Summary

RN 0.84 기준으로 legacy runtime 토글 대신 `async serialized surface`와 `sync TurboModule/JSI-style surface`를 비교하는 benchmark 학습 프로젝트다.

## Source Provenance

- Legacy source: `legacy/02-architecture/bridge-vs-jsi`
- Study path: `study/React-Native-Architecture/bridge-vs-jsi`

## Build/Test

```bash
make -C study/React-Native-Architecture/bridge-vs-jsi/problem test
make -C study/React-Native-Architecture/bridge-vs-jsi/problem app-build
make -C study/React-Native-Architecture/bridge-vs-jsi/problem app-test
```

## Current Status

- problem scaffold: modernized for RN 0.84
- react-native implementation: verified with benchmark dashboard, statistics, JSON export
- docs migration: verified for architecture-study scope
