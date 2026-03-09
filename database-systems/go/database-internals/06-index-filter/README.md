# 06 Index Filter

## Summary

Bloom filter와 sparse index를 함께 붙인 SSTable을 구현해서, 없는 key는 즉시 거절하고 있는 key는 작은 block 범위만 읽도록 만든다.

## Status

- 상태: `verified`
- 구현 언어: `Go 1.26.0`

## Commands

```bash
cd go/database-internals/06-index-filter
GOWORK=off go test ./...
GOWORK=off go run ./cmd/index-filter
```
