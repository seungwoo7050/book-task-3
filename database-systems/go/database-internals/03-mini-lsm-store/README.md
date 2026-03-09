# 03 Mini LSM Store

## Summary

이 프로젝트는 active MemTable, flush, newest-first read path를 묶어 최소 LSM store를 완성한다. `01`과 `02`에서 따로 배운 자료구조와 파일 형식을 상위 orchestration으로 연결하는 단계다.

## Scope

- active memtable write path
- flush threshold and immutable swap
- newest-first SSTable search
- reopen after persisted flush

## Status

- 상태: `verified`
- 구현 언어: `Go 1.26.0`

## Commands

```bash
cd go/database-internals/03-mini-lsm-store
GOWORK=off go test ./...
GOWORK=off go run ./cmd/mini-lsm-store
```
