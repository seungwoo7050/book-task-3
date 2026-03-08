# Gestures And Reanimated

Status: verified

## Summary

Swipe card, reorder list, shared transition을 한 앱 안에서 묶어 Reanimated 4와 Gesture Handler 2 상호작용을 학습하는 프로젝트다.

## Source Provenance

- Legacy source: `legacy/01-foundation/gestures`
- Study path: `study/Mobile-Foundations/gestures`

## Build/Test

```bash
make -C study/Mobile-Foundations/gestures/problem test
make -C study/Mobile-Foundations/gestures/problem app-build
make -C study/Mobile-Foundations/gestures/problem app-test
```

## Docs

- [docs/README.md](docs/README.md)
- [docs/concepts/gesture-workflow.md](docs/concepts/gesture-workflow.md)
- [docs/references/README.md](docs/references/README.md)

## Current Status

- problem scaffold: verified
- react-native implementation: verified with swipe/reorder/shared-transition shell
- docs migration: verified for interaction-study scope
