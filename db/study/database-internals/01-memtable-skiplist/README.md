# 01 MemTable SkipList

## Summary

이 프로젝트는 LSM-Tree의 active MemTable 자료구조를 독립적으로 구현하고 검증하는 첫 파일럿이다. 핵심 목표는 정렬된 쓰기 경로, tombstone 표현, ordered iteration을 작은 범위에서 먼저 고정하는 것이다.

## Status

- 상태: `verified`
- 구현 언어: Go 1.26.0
- 검증 명령:

```bash
cd study/database-internals/01-memtable-skiplist/go
go test ./...
go run ./cmd/skiplist-demo
```

## Public Layout

- [problem/README.md](problem/README.md)
- [go/README.md](go/README.md)
- [docs/README.md](docs/README.md)

## Learning Focus

- lexicographic ordering이 유지되는 in-memory write path
- delete를 tombstone으로 모델링하는 이유
- flush 이전 단계에서 필요한 최소 API를 어떻게 고정할지

