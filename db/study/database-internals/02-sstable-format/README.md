# 02 SSTable Format

## Summary

이 프로젝트는 immutable SSTable 파일 형식, footer metadata, point lookup, full scan을 Go로 구현한다. tombstone도 같은 binary format 안에서 표현한다.

## Status

- 상태: `verified`
- 구현 언어: Go 1.26.0
- 검증 명령:

```bash
cd study/database-internals/02-sstable-format/go
go test ./...
go run ./cmd/sstable-format
```

## Public Layout

- [problem/README.md](problem/README.md)
- [go/README.md](go/README.md)
- [docs/README.md](docs/README.md)

