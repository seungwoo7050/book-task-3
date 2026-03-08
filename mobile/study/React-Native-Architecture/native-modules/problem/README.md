# Problem: Native Modules

> Status: VERIFIED
> Scope: spec/codegen/consumer app
> Last Checked: 2026-03-08

## Objective

Battery, Haptics, Sensor 세 모듈의 public TypeScript spec을 고정하고,
codegen summary와 consumer app으로 JS/native 경계를 설명한다.

## Required Scope

1. typed module specs
2. codegen summary export
3. consumer screen
4. docs on platform parity

## Evaluation

```bash
make test
make codegen
make app-build
make app-test
```
