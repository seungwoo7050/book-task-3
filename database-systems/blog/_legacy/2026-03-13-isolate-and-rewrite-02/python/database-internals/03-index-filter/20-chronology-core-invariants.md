# 20 03 Index Filter의 핵심 invariant를 코드에서 고정하기

이 글은 프로젝트 전체의 가운데에 해당한다. 여기서는 README 문장을 다시 요약하지 않고, 실제 구현에서 상태 전이가 어디서 강제되는지만 따라간다.

## Phase 2
### Session 1

- 당시 목표:
  `BloomFilter`가 어떤 입력을 받아 어떤 상태를 고정하는지 분해한다.
- 변경 단위:
  `database-systems/python/database-internals/projects/03-index-filter/src/index_filter/table.py`의 `BloomFilter`
- 처음 가설:
  `BloomFilter` 하나를 이해하면 나머지 흐름도 거의 자동으로 따라올 거라고 생각했다.
- 실제 진행:
  `rg -n "BloomFilter|_hash_value" src`로 핵심 함수 위치를 다시 잡고, `BloomFilter`가 문제 정의의 첫 번째 bullet과 정확히 맞물리는지 확인했다.

CLI:

```bash
$ rg -n "BloomFilter|_hash_value" src
src/index_filter/table.py:15:def _hash_value(key: str, seed: int) -> int:
src/index_filter/table.py:48:class BloomFilter:
src/index_filter/table.py:73:    def deserialize(cls, buffer: bytes) -> "BloomFilter":
src/index_filter/table.py:86:        h1 = _hash_value(key, 0)
src/index_filter/table.py:87:        h2 = _hash_value(key, 42)
src/index_filter/table.py:143:        self.filter: BloomFilter | None = None
src/index_filter/table.py:151:        bloom = BloomFilter(len(records) + 1, 0.01)
src/index_filter/table.py:192:        self.filter = BloomFilter.deserialize(buffer[self.bloom_offset : self.bloom_offset + self.bloom_size])
src/index_filter/__init__.py:1:from .table import BloomFilter, LookupStats, SparseIndex, SSTable
src/index_filter/__init__.py:3:__all__ = ["BloomFilter", "LookupStats", "SparseIndex", "SSTable"]
```

검증 신호:

- `BloomFilter` 안에서 상태가 한 번에 굳는지, 아니면 보조 구조로 넘겨지는지가 프로젝트의 설명 밀도를 갈랐다.
- `Bloom filter가 negative lookup 비용을 어떻게 줄이는지 이해합니다.`

핵심 코드:

```python
class BloomFilter:
    def __init__(self, expected_items: int, false_positive_rate: float = 0.01) -> None:
        expected_items = max(expected_items, 1)
        if not 0 < false_positive_rate < 1:
            false_positive_rate = 0.01
        bit_count = math.ceil(-(expected_items * math.log(false_positive_rate)) / (math.log(2) ** 2))
        hash_functions = max(1, round((bit_count / expected_items) * math.log(2)))
        self.bit_count = bit_count
        self.hash_functions = hash_functions
        self.bits = bytearray(math.ceil(bit_count / 8))
```

왜 이 코드가 중요했는가:

`BloomFilter`는 이 프로젝트의 write path 혹은 primary decision point를 드러낸다. 테스트가 요구하는 첫 번째 조건을 만족시키는 규칙이 여기서 한 번에 보였다.

새로 배운 것:

- `Sparse Index Scan`에서 정리한 요점처럼, sparse index는 모든 key를 메모리에 들고 있지 않고, block 경계 key만 유지한다. lookup은 다음 순서로 진행된다.

다음:

- `_hash_value`까지 읽어야 비로소 이 프로젝트가 '쓰는 방법'만이 아니라 '읽고 복원하는 방법'까지 같이 고정하는지 판단할 수 있다.

### Session 2

- 당시 목표:
  `_hash_value`가 `BloomFilter`와 어떤 짝을 이루는지 확인한다.
- 변경 단위:
  `database-systems/python/database-internals/projects/03-index-filter/src/index_filter/table.py`의 `_hash_value`
- 처음 가설:
  `_hash_value`는 단순 보조 함수일 거라고 생각했다.
- 실제 진행:
  두 번째 앵커를 읽고 나니, 실제로는 `BloomFilter`가 만든 상태를 외부에서 관찰 가능하게 만드는 규칙이 여기 있었다.

CLI:

```bash
$ rg -n "^(class|def) " src
src/index_filter/table.py:15:def _hash_value(key: str, seed: int) -> int:
src/index_filter/table.py:20:def encode_record(key: str, value: str | None) -> bytes:
src/index_filter/table.py:27:def decode_record(buffer: bytes, offset: int) -> tuple[tuple[str, str | None], int]:
src/index_filter/table.py:42:class LookupStats:
src/index_filter/table.py:48:class BloomFilter:
src/index_filter/table.py:92:class IndexEntry:
src/index_filter/table.py:97:class SparseIndex:
src/index_filter/table.py:134:class SSTable:
src/index_filter/table.py:226:def demo() -> None:
```

검증 신호:

- `_hash_value`는 테스트의 뒤쪽 시나리오를 설명하는 열쇠였다.
- 특히 `test_sstable_bloom_reject_and_bounded_scan` 같은 이름이 왜 필요한지, 이 함수에서야 연결이 됐다.

핵심 코드:

```python
def _hash_value(key: str, seed: int) -> int:
    payload = f"{seed}:{key}".encode("utf-8")
    return int.from_bytes(hashlib.sha256(payload).digest()[:8], "big")


def encode_record(key: str, value: str | None) -> bytes:
    key_bytes = key.encode()
    value_bytes = b"" if value is None else value.encode()
    value_length = TOMBSTONE_MARKER if value is None else len(value_bytes)
    return struct.pack(">II", len(key_bytes), value_length) + key_bytes + value_bytes
```

왜 이 코드가 중요했는가:

`_hash_value`가 없으면 `BloomFilter`의 의미도 끝까지 설명되지 않는다. 이 코드를 보고 나서야, 이 프로젝트가 단일 API 구현이 아니라 ordering / visibility / recovery 규칙을 통째로 묶는 이유를 납득할 수 있었다.

새로 배운 것:

- `Sparse Index Scan`에서 정리한 요점처럼, sparse index는 모든 key를 메모리에 들고 있지 않고, block 경계 key만 유지한다. lookup은 다음 순서로 진행된다.

다음:

- 실제 재검증 명령을 다시 돌려, 지금까지 읽은 invariant가 테스트와 demo 출력에서 같은 모양으로 보이는지 확인한다.
