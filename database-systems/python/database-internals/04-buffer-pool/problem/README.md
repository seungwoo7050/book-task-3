# Problem Framing

page cache hit를 높이면서 dirty page를 안전하게 flush하는 buffer pool manager를 구현한다.

## Success Criteria

- page id로 file path와 page number를 안정적으로 분리
- fetch 시 cache hit면 pin count 증가, miss면 disk read
- dirty page는 eviction이나 explicit flush 때 write-back
- pinned page는 eviction하지 않음

## Source Provenance

- 원본 문제: `legacy/transaction-engine/buffer-pool/problem/README.md`
- 원본 solution 참고: `legacy/transaction-engine/buffer-pool/solve/solution/lru-cache.js`
- 원본 solution 참고: `legacy/transaction-engine/buffer-pool/solve/solution/buffer-pool.js`
