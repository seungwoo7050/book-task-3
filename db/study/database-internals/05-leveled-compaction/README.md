# 05 Leveled Compaction

L0의 겹치는 SSTable을 병합해서 L1로 내리고, manifest를 원자적으로 갱신하는 작은 leveled compaction 경로를 구현한다.

- 상태: `verified`
- 구현 언어: `Go 1.26.0`
- 검증 범위: `k-way merge`, `tombstone drop policy`, `manifest round-trip`, `old file cleanup`
- 원본: `legacy/storage-engine/compaction`

## Public Surface

- `problem/`: 원본 문제와 정규화 근거
- `go/`: compaction manager, SSTable reader/writer, 테스트, 데모
- `docs/`: merge ordering, manifest 원자성 설명

## Verification

```bash
cd study/database-internals/05-leveled-compaction/go
GOWORK=off go test ./...
GOWORK=off go run ./cmd/leveled-compaction
```

## What This Project Teaches

- 왜 L0 입력은 최신 순서로 merge 해야 하는가
- 언제 tombstone을 떨어뜨려도 안전한가
- compaction 결과와 manifest 갱신을 함께 다뤄야 하는 이유
