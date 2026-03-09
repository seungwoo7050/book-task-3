# 08 MVCC

## Summary

이 프로젝트는 snapshot isolation을 위한 version chain과 transaction manager를 구현한다.

## Scope

- version chain storage
- snapshot visibility
- first-committer-wins conflict detection
- stale-version garbage collection

## Status

- 상태: `verified`
- 구현 언어: `Go 1.26.0`

## Commands

```bash
cd go/database-internals/08-mvcc
GOWORK=off go test ./...
GOWORK=off go run ./cmd/mvcc
```
