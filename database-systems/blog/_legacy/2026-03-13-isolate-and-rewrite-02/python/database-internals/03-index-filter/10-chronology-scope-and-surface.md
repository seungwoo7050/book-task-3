# 10 03 Index Filter의 범위를 다시 잡기

이 글은 프로젝트 전체에서 가장 앞부분에 해당한다. README의 한 줄 설명을 곧바로 믿지 않고, 파일 구조와 테스트 이름만으로 먼저 범위를 다시 세운다.

## Phase 1
### Session 1

- 당시 목표:
  `03 Index Filter`가 어떤 invariant를 먼저 고정하는 슬롯인지 파악한다.
- 변경 단위:
  `database-systems/python/database-internals/projects/03-index-filter/README.md`, `database-systems/python/database-internals/projects/03-index-filter/tests/test_index_filter.py`
- 처음 가설:
  구현이 너무 작아서 단순 API 연습에 가까울 거라고 봤다.
- 실제 진행:
  `find src tests -type f | sort`로 구조를 펼친 뒤 `rg -n "^def test_" tests`로 테스트 이름을 나열했다. `test_sstable_bloom_reject_and_bounded_scan`까지 테스트 이름을 훑고 나니, 이 프로젝트의 중심이 단순 기능 추가가 아니라 `BloomFilter` 주변의 invariant를 고정하는 일이라는 게 보였다.

CLI:

```bash
$ find src tests -type f | sort
src/index_filter/__init__.py
src/index_filter/__main__.py
src/index_filter/__pycache__/__init__.cpython-312.pyc
src/index_filter/__pycache__/__init__.cpython-314.pyc
src/index_filter/__pycache__/__main__.cpython-312.pyc
src/index_filter/__pycache__/__main__.cpython-314.pyc
src/index_filter/__pycache__/table.cpython-312.pyc
src/index_filter/__pycache__/table.cpython-314.pyc
src/index_filter/table.py
tests/__pycache__/test_index_filter.cpython-312-pytest-8.3.5.pyc
tests/__pycache__/test_index_filter.cpython-314-pytest-9.0.2.pyc
tests/test_index_filter.py
```

```bash
$ rg -n "^def test_" tests
tests/test_index_filter.py:5:def test_bloom_filter_has_no_false_negatives():
tests/test_index_filter.py:14:def test_bloom_filter_false_positive_rate_is_bounded():
tests/test_index_filter.py:26:def test_sparse_index_finds_expected_block():
tests/test_index_filter.py:35:def test_sstable_bloom_reject_and_bounded_scan(tmp_path):
```

검증 신호:

- `test_bloom_filter_has_no_false_negatives`는 가장 기본 표면을 보여 줬고, `test_sstable_bloom_reject_and_bounded_scan`는 이 프로젝트가 이미 경계 조건까지 포함한다는 신호였다.
- 테스트 이름만으로도 문제의 중심이 `BloomFilter` 주변의 ordering / visibility 규칙이라는 점이 드러났다.

핵심 코드:

```python
def test_sstable_bloom_reject_and_bounded_scan(tmp_path):
    table = SSTable(tmp_path / "index.sst", 8)
    records = [(fmt_key(index), f"value-{fmt_key(index)}") for index in range(64)]
    table.write(records)

    value, ok, stats, _ = table.get_with_stats("missing-key")
    assert ok is False
    assert value is None
    assert stats.bloom_rejected is True
    assert stats.bytes_read == 0
```

왜 이 코드가 중요했는가:

`test_sstable_bloom_reject_and_bounded_scan`는 README의 추상 설명보다 더 직접적으로, 어떤 실패를 막아야 하는지 보여 준다. 나는 여기서 구현 순서를 거꾸로 세우기보다 테스트가 요구하는 경계를 먼저 고정해야 한다고 판단했다.

새로 배운 것:

- `Bloom Filter Sizing`에서 정리한 요점처럼, Bloom filter는 false negative가 없어야 하고, false positive는 허용 가능한 수준으로만 남아야 한다. 이 프로젝트는 레거시와 같은 식을 사용한다.

다음:

- `BloomFilter`와 `_hash_value`를 코드에서 직접 확인해, 테스트 이름이 가리키는 invariant가 실제로 어디에 박혀 있는지 본다.

### Session 2

- 당시 목표:
  소스 파일의 중심 타입/클래스가 어떤 책임을 한곳에 묶고 있는지 확인한다.
- 변경 단위:
  `database-systems/python/database-internals/projects/03-index-filter/src/index_filter/table.py`
- 처음 가설:
  구현이 작으면 책임도 단순하게 한 줄로 설명될 거라고 생각했다.
- 실제 진행:
  가장 큰 구현 파일인 `database-systems/python/database-internals/projects/03-index-filter/src/index_filter/table.py`를 먼저 읽고, 테스트가 요구한 상태 전이가 정말 이 파일 안에서 닫히는지 확인했다.

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

- `BloomFilter` 같은 이름이 초기에 바로 보이면 write path의 중심이 선명해진다.
- 반대로 `_hash_value`가 함께 보이면 read path나 visibility 규칙을 따로 떼어 설명할 수 없다는 뜻이다.

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

`BloomFilter`는 이 프로젝트가 가장 먼저 고정해야 하는 상태 전이를 보여 준다. 이 조각을 읽고 나서야 테스트 이름과 실제 구현 책임이 같은 축에 놓여 있다는 확신이 생겼다.

새로 배운 것:

- `Sparse Index Scan`에서 정리한 요점처럼, sparse index는 모든 key를 메모리에 들고 있지 않고, block 경계 key만 유지한다. lookup은 다음 순서로 진행된다.

다음:

- 같은 상태를 반대 방향에서 고정하는 `_hash_value`를 읽어, write/read 혹은 append/replay가 서로 어떻게 잠기는지 확인한다.
