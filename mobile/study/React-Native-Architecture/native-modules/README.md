# Native Modules

Status: verified

## Summary

Battery, Haptics, Sensor 세 모듈의 TypeScript spec, codegen summary, consumer screen을 묶은 native-boundary 학습 프로젝트다.

## Source Provenance

- Legacy source: `legacy/02-architecture/native-modules`
- Study path: `study/React-Native-Architecture/native-modules`

## Build/Test

```bash
make -C study/React-Native-Architecture/native-modules/problem test
make -C study/React-Native-Architecture/native-modules/problem codegen
make -C study/React-Native-Architecture/native-modules/problem app-build
make -C study/React-Native-Architecture/native-modules/problem app-test
```
