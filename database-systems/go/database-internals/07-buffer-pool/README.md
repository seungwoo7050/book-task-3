# 07 Buffer Pool

## Summary

이 프로젝트는 disk-backed page를 메모리에 캐시하고, pin count와 dirty write-back 정책을 포함한 buffer pool manager를 구현한다.

## Scope

- O(1) LRU cache
- page fetch and pin/unpin
- dirty tracking and write-back

## Status

- 상태: `verified`
- 구현 언어: `Go 1.26.0`

## Commands

```bash
cd go/database-internals/07-buffer-pool
GOWORK=off go test ./...
GOWORK=off go run ./cmd/buffer-pool
```
