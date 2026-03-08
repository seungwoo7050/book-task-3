# 06 Index Filter

Bloom filter와 sparse index를 함께 붙인 SSTable을 구현해서, 없는 key는 즉시 거절하고 있는 key는 작은 block 범위만 읽도록 만든다.

- 상태: `verified`
- 구현 언어: `Go 1.26.0`
- 검증 범위: `Bloom filter`, `sparse index`, `footer metadata`, `bounded block scan`
- 원본: `legacy/storage-engine/index-filter`

## Verification

```bash
cd study/database-internals/06-index-filter/go
GOWORK=off go test ./...
GOWORK=off go run ./cmd/index-filter
```

## What This Project Teaches

- probabilistic membership test를 read path에 어디에 넣는가
- sparse index가 point lookup의 scan 범위를 어떻게 줄이는가
- metadata footer가 reader open path를 어떻게 단순화하는가
