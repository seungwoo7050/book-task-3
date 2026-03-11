# 03 Index Filter — 개발 타임라인

## Phase 0: 환경 준비

```bash
cd python/database-internals/projects/03-index-filter
python3 --version
# Python 3.14.x

python3 -m pip install -U pytest
```

### pyproject.toml 확인

```toml
[project]
name = "index-filter"
version = "0.1.0"
requires-python = ">=3.12"

[tool.setuptools]
package-dir = {"" = "src"}
```

src layout이므로 테스트 실행 시 `PYTHONPATH=src`가 필요하다.

### 디렉토리 구조 생성

```bash
mkdir -p src/index_filter tests docs/concepts docs/references
touch src/index_filter/__init__.py
touch src/index_filter/__main__.py
touch src/index_filter/table.py
touch tests/test_index_filter.py
```

---

## Phase 1: Binary Serialization 기반 코드

### 1.1 상수 및 인코딩 함수

`table.py`에 레코드 직렬화부터 작성한다. Py 02-wal-recovery에서 사용한 것과 동일한 binary 포맷을 채택한다.

```python
TOMBSTONE_MARKER = 0xFFFFFFFF
FOOTER_MAGIC = b"SIF1"

def encode_record(key: str, value: str | None) -> bytes:
    key_bytes = key.encode()
    value_bytes = b"" if value is None else value.encode()
    value_length = TOMBSTONE_MARKER if value is None else len(value_bytes)
    return struct.pack(">II", len(key_bytes), value_length) + key_bytes + value_bytes
```

**결정**: JSON Lines 대신 바이너리 포맷을 선택. 바이트 단위 오프셋 계산이 정확해야 sparse index가 동작하기 때문.

### 1.2 디코드 함수

```python
def decode_record(buffer: bytes, offset: int) -> tuple[tuple[str, str | None], int]:
```

오프셋 기반 디코딩. 헤더 8바이트(key_length 4B + value_length 4B) 읽고 나머지를 파싱. 반환값에 소비한 바이트 수를 포함하여 연속 디코딩 가능.

---

## Phase 2: Bloom Filter 구현

### 2.1 해시 함수 결정

Go 버전은 `shared/hash` 패키지의 MurmurHash3를 사용했지만, Python 버전에서는 외부 의존성 없이 stdlib만 사용하기로 결정.

```python
import hashlib

def _hash_value(key: str, seed: int) -> int:
    payload = f"{seed}:{key}".encode("utf-8")
    return int.from_bytes(hashlib.sha256(payload).digest()[:8], "big")
```

**결정 근거**: `hashlib.sha256`은 Python 표준 라이브러리에 포함되어 있어 추가 설치 불필요. SHA-256의 첫 8바이트(64비트)만 사용하면 Bloom filter의 비트 배열 크기에 비해 충분한 범위.

### 2.2 BloomFilter 클래스

```python
class BloomFilter:
    def __init__(self, expected_items: int, false_positive_rate: float = 0.01) -> None:
```

핵심 설계:
- `m = -(n × ln(p)) / (ln2)²` 으로 비트 수 계산
- `k = (m / n) × ln2` 으로 해시 함수 수 결정
- `bytearray(ceil(bit_count / 8))` 로 비트 배열 할당
- double hashing: `(h1 + i * h2) % bit_count` 로 k개 위치 유도

### 2.3 Bloom filter 단독 테스트

```bash
PYTHONPATH=src python3 -m pytest tests/test_index_filter.py::test_bloom_filter_has_no_false_negatives -v
```

512개 키를 넣고 모두 `might_contain() == True`인지 확인. false negative가 없음을 증명.

```bash
PYTHONPATH=src python3 -m pytest tests/test_index_filter.py::test_bloom_filter_false_positive_rate_is_bounded -v
```

1000개 present 키를 넣고, 5000개 absent 키로 false positive rate가 3% 이하인지 확인. 목표 p=0.01보다 느슨한 bound(0.03)를 사용하여 환경 차이로 인한 flake 방지.

---

## Phase 3: Sparse Index 구현

### 3.1 IndexEntry와 SparseIndex

```python
@dataclass(slots=True)
class IndexEntry:
    key: str
    offset: int

class SparseIndex:
    def __init__(self, block_size: int = 16) -> None:
```

`build()`: N개 엔트리 중 `block_size` 간격으로만 선택.  
`find_block()`: 이진 탐색으로 target key가 속하는 블록의 `(start_offset, end_offset)` 반환.

### 3.2 JSON 직렬화

```python
def serialize(self) -> bytes:
    payload = [{"key": entry.key, "offset": entry.offset} for entry in self.entries]
    return json.dumps(payload).encode("utf-8")
```

**Go 버전과의 차이**: Go는 커스텀 바이너리 직렬화를 사용하지만, Python에서는 JSON으로 간결하게 처리. 인덱스 엔트리 수가 적어서(block_size 간격) 성능 차이는 무시 가능.

### 3.3 sparse index 단독 테스트

```bash
PYTHONPATH=src python3 -m pytest tests/test_index_filter.py::test_sparse_index_finds_expected_block -v
```

32개 엔트리, block_size=8 → 인덱스 4개 생성. key "k017"이 블록 (320, 480)에 속하는지 확인.

---

## Phase 4: SSTable 통합

### 4.1 SSTable 클래스

```python
class SSTable:
    def __init__(self, path: str | Path, block_size: int = 16) -> None:
```

세 단계 구현:
1. `write()`: 정렬된 레코드 기록 → Bloom filter 구축 → sparse index 구축 → footer 기록
2. `load()`: 마지막 40바이트(footer) 읽기 → Bloom filter, sparse index 복원
3. `get_with_stats()`: Bloom check → sparse index lookup → block scan

### 4.2 파일 레이아웃

```
[Data][Bloom][Index][Footer 40B]
```

Footer 구조:
```python
FOOTER_MAGIC + struct.pack(">QQQQI",
    bloom_offset, bloom_size,
    index_offset, index_size,
    block_size
)
```

- magic `b"SIF1"`: 4바이트
- offset/size: 각 8바이트(Q) × 4 = 32바이트  
- block_size: 4바이트(I)
- 총 40바이트

### 4.3 LookupStats

```python
@dataclass(slots=True)
class LookupStats:
    bloom_rejected: bool = False
    bytes_read: int = 0
    block_range: tuple[int, int] = (0, 0)
```

조회 과정의 성능 지표를 캡슐화. 테스트가 이 값을 검증하여 "정말로 적게 읽었는지" 증명.

### 4.4 통합 테스트

```bash
PYTHONPATH=src python3 -m pytest tests/test_index_filter.py::test_sstable_bloom_reject_and_bounded_scan -v
```

64개 레코드, block_size=8:
- `"missing-key"` → bloom_rejected=True, bytes_read=0
- `fmt_key(23)` → found=True, 0 < bytes_read < data_size

---

## Phase 5: Demo와 마무리

### 5.1 __main__.py

```python
from .table import demo

if __name__ == "__main__":
    demo()
```

### 5.2 demo 실행

```bash
PYTHONPATH=src python3 -m index_filter
# {"found": True, "value": "value-k023", "bytes_read": ...}
```

TemporaryDirectory 사용으로 임시 파일 자동 정리.

### 5.3 __init__.py 공개 API 정의

```python
from .table import BloomFilter, LookupStats, SparseIndex, SSTable
__all__ = ["BloomFilter", "LookupStats", "SparseIndex", "SSTable"]
```

### 5.4 전체 테스트

```bash
PYTHONPATH=src python3 -m pytest tests/ -v
```

4개 테스트 모두 통과 확인.

---

## Phase 6: 개념 문서 작성

### docs/concepts/bloom-filter-sizing.md
- Bloom filter 크기 결정 공식 설명
- m, k 계산 과정

### docs/concepts/sparse-index-scan.md
- 조회 경로 4단계 설명
- block_size와 메모리/I/O 트레이드오프

---

## 소스코드에서 드러나지 않는 결정들

1. **SHA-256 vs MurmurHash3**: Go 버전은 shared/hash의 MurmurHash3를 사용했지만, Python은 외부 의존성 회피를 위해 hashlib.sha256을 선택. 분포 품질보다 이식성 우선.

2. **sparse index JSON 직렬화**: 엔트리 수가 적어 JSON 오버헤드가 무시 가능. 바이너리 대신 JSON을 선택하여 디버깅 편의성 확보.

3. **false positive 테스트 bound 0.03**: 목표 p=0.01이지만 테스트에서는 0.03으로 느슨하게 검증. 해시 함수 구현, 키 분포, 환경 차이로 인한 flaky test 방지.

4. **4번째 반환값 None**: `get_with_stats`가 4-tuple을 반환하는데 마지막 값은 항상 None. Go 버전의 error 반환 패턴과의 일관성을 위한 자리.

5. **정렬 검증**: `write()` 시 레코드가 정렬되어 있는지 체크하고 아니면 ValueError. 정렬 보장은 caller의 책임이지만, 잘못된 입력을 조기에 차단.
