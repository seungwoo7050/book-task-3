# 03 Testing And Debugging

## Status

`verified`

## Legacy source

- `study`에서 새로 추가한 입문 과제

## Problem scope

- table-driven test
- subtest
- benchmark
- race detector에 안전한 recorder 작성

## Build

```bash
cd go
go run ./cmd/debugdemo
```

## Test

```bash
cd go
go test ./... -bench=.
```

## Verification

- `go run ./cmd/debugdemo`
- `go test ./... -bench=.`

## Known gaps

- 실제 debugger 사용법은 docs와 후속 프로젝트에서 보강한다.

