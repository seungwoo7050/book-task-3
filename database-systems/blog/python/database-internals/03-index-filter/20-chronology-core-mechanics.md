# 20 Core Mechanics

## Day 1
### Session 3

Bloom filter 구현에서 중요한 건 false positive가 아니라 false negative가 없어야 한다는 점이다.

```python
def might_contain(self, key: str) -> bool:
    for position in self.positions(key):
        if self.bits[position // 8] & (1 << (position % 8)) == 0:
            return False
    return True
```

한 비트라도 비어 있으면 즉시 `False`를 반환한다. 그래서 "없는 키는 빠르게 버릴 수 있지만, True가 나와도 확정은 아니다"라는 Bloom의 역할이 코드에 그대로 보인다.

다음은 sparse index.

```python
def find_block(self, key: str, data_size: int) -> tuple[tuple[int, int], bool]:
    ...
    start = self.entries[block].offset
    end = data_size if block + 1 >= len(self.entries) else self.entries[block + 1].offset
    return (start, end), True
```

핵심은 key 전체 검색이 아니라 "어느 block 구간만 읽으면 되는지"를 주는 것이다.

- 목표: Bloom reject와 sparse block narrowing의 역할 분리 확인
- 진행: `BloomFilter.positions/might_contain`, `SparseIndex.find_block`를 테스트와 대조

CLI:

```bash
cd python/database-internals/projects/03-index-filter
sed -n '40,220p' src/index_filter/table.py
sed -n '1,80p' tests/test_index_filter.py
```

### Session 4

`test_sstable_bloom_reject_and_bounded_scan`이 가장 중요한 통합 테스트다.

- missing key는 `stats.bloom_rejected is True`, `bytes_read == 0`
- present key는 `0 < bytes_read < table.data_size`

이 두 조건이 동시에 만족되어야 "거절은 빠르고, 조회는 전체 scan이 아니다"라는 메시지가 성립한다.

다음 질문:

- footer metadata는 load 시 어떤 순서로 해석되나
- block_size를 조정하면 false positive와 bytes_read의 균형은 어떻게 변하나