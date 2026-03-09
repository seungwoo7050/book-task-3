# 05 Leveled Compaction

## Summary

L0의 겹치는 SSTable을 병합해서 L1로 내리고, manifest를 원자적으로 갱신하는 작은 leveled compaction 경로를 구현한다.

## Status

- 상태: `verified`
- 구현 언어: `Go 1.26.0`

## Commands

```bash
cd go/database-internals/05-leveled-compaction
GOWORK=off go test ./...
GOWORK=off go run ./cmd/leveled-compaction
```
