# 10 filter 와 index 를 왜 같이 붙였는가

## Day 1
### Session 1

이 프로젝트를 처음 열었을 때는 Bloom filter 실습 하나라고 생각했다. 그런데 `tests/test_index_filter.py`를 보면 의도가 더 넓다.

```bash
cd python/database-internals/projects/03-index-filter
grep -n "def test_" tests/test_index_filter.py
```

```text
5:def test_bloom_filter_has_no_false_negatives():
13:def test_bloom_filter_false_positive_rate_is_bounded():
24:def test_sparse_index_finds_expected_block():
32:def test_sstable_bloom_reject_and_bounded_scan(tmp_path):
```

Bloom filter 단독이 아니라 `Bloom + Sparse Index + SSTable footer`를 한 lookup pipeline으로 묶는 단계다.

- 목표: "없는 키 빠른 거절"과 "있는 키 scan 범위 축소"를 분리해서 이해
- 진행: `BloomFilter`, `SparseIndex`, `SSTable.get_with_stats` 순서로 읽음

이 시점에서 먼저 눈에 들어온 타입은 `LookupStats`였다.

```python
@dataclass(slots=True)
class LookupStats:
    bloom_rejected: bool = False
    bytes_read: int = 0
    block_range: tuple[int, int] = (0, 0)
```

결과 값만 반환하는 대신 lookup 비용을 같이 반환한다. 즉 이 프로젝트의 핵심은 "정답을 찾는다"가 아니라 "얼마나 덜 읽고 찾는가"다.

### Session 2

wire format도 살펴봤다.

```python
def encode_record(key: str, value: str | None) -> bytes:
    ...
    return struct.pack(">II", len(key_bytes), value_length) + key_bytes + value_bytes
```

delete tombstone은 여기서도 `TOMBSTONE_MARKER`를 쓴다. 02의 WAL slot에서 썼던 삭제 표현이 SSTable 레코드 포맷에서도 유지된다.

다음 질문:

- Bloom filter를 통과한 뒤 block range는 어떻게 계산되나
- footer metadata 없이도 filter/index 위치를 복원할 수 있나
