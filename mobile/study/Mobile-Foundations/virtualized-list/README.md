# Virtualized List Performance

Status: verified

## Summary

FlatList baseline과 FlashList v2 최적화 경로를 같은 앱에서 비교하는 성능 학습 프로젝트다.

## Source Provenance

- Legacy source: `legacy/01-foundation/virtualized-list`
- Study path: `study/Mobile-Foundations/virtualized-list`

## Build/Test

```bash
make -C study/Mobile-Foundations/virtualized-list/problem test
make -C study/Mobile-Foundations/virtualized-list/problem app-build
make -C study/Mobile-Foundations/virtualized-list/problem app-test
make -C study/Mobile-Foundations/virtualized-list/problem benchmark
```

## Docs

- [docs/README.md](docs/README.md)
- [docs/concepts/flashlist-v2-benchmarking.md](docs/concepts/flashlist-v2-benchmarking.md)
- [docs/references/README.md](docs/references/README.md)

## Current Status

- problem scaffold: verified and modernized for FlashList v2
- react-native implementation: verified with 10k deterministic data, baseline/optimized views, benchmark summary
- docs migration: verified for performance-study scope
