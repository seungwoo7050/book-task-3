# 02 SSTable Format

## Summary

이 프로젝트는 immutable SSTable 파일 형식, footer metadata, point lookup, full scan을 Go로 구현한다. tombstone도 같은 binary format 안에서 표현한다.

## Scope

- immutable SSTable write
- footer metadata parse
- in-memory sparse key index for point lookup
- tombstone-preserving record round-trip

## Status

- 상태: `verified`
- 구현 언어: `Go 1.26.0`

## Commands

```bash
cd go/database-internals/02-sstable-format
GOWORK=off go test ./...
GOWORK=off go run ./cmd/sstable-format
```
