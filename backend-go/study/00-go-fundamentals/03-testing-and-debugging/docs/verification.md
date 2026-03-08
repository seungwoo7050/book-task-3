# Verification

## Commands

```bash
cd 00-go-fundamentals/03-testing-and-debugging/go
go run ./cmd/debugdemo
go test ./... -bench=.
```

## Result

- 2026-03-07 기준 `go run ./cmd/debugdemo`가 정상 실행됐다.
- 2026-03-07 기준 `go test ./... -bench=.`가 통과했다.

## Remaining Checks

- pprof나 execution trace는 이 과제 범위에 넣지 않았다.

