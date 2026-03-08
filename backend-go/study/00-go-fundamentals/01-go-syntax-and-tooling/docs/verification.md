# Verification

## Commands

```bash
cd 00-go-fundamentals/01-go-syntax-and-tooling/go
go run ./cmd/toolingdemo
go test ./...
```

## Result

- 2026-03-07 기준 `go run ./cmd/toolingdemo`가 정상 실행됐다.
- 2026-03-07 기준 `go test ./...`가 통과했다.

## Remaining Checks

- stdin 입력과 flag 파싱은 현재 범위 밖이라 별도 검증하지 않았다.

