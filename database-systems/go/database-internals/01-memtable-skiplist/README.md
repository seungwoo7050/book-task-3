# 01 MemTable SkipList

## Summary

이 프로젝트는 LSM-Tree의 active MemTable 자료구조를 독립적으로 구현하고 검증하는 첫 파일럿이다. 핵심 목표는 정렬된 쓰기 경로, tombstone 표현, ordered iteration을 작은 범위에서 먼저 고정하는 것이다.

## Scope

- SkipList insertion and update
- tombstone semantics
- ordered iteration
- approximate byte-size accounting

## Status

- 상태: `verified`
- 구현 언어: `Go 1.26.0`

## Commands

```bash
cd go/database-internals/01-memtable-skiplist
GOWORK=off go test ./...
GOWORK=off go run ./cmd/skiplist-demo
```
