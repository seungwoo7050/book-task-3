# 03 Mini LSM Store

## Summary

이 프로젝트는 active MemTable, flush, newest-first read path를 묶어 최소 LSM store를 완성한다. `01`과 `02`에서 따로 배운 자료구조와 파일 형식을 상위 orchestration으로 연결하는 단계다.

## Status

- 상태: `verified`
- 구현 언어: Go 1.26.0
- 검증 명령:

```bash
cd study/database-internals/03-mini-lsm-store/go
go test ./...
go run ./cmd/mini-lsm-store
```

