# "없는 키를 빨리 거르는 법" — Python으로 Bloom Filter와 Sparse Index 붙이기

## SSTable의 약점

Py 01에서 만든 SSTable은 단순했다. JSON Lines로 key-value 쌍을 정렬해서 기록하고, 조회할 때는 파일 전체를 읽어서 선형 탐색했다. 데이터가 수십 건이면 아무 문제가 없지만, 수천, 수만 건이 쌓이면 **없는 키를 찾으러 파일 끝까지 가는 비용**이 무시할 수 없었다.

이 프로젝트의 출발점은 간단한 질문이었다: "존재하지 않는 키를 디스크를 건드리지 않고 바로 걸러낼 수 있을까?"

## Bloom Filter: 확률적 거부기

Bloom filter는 "이 키가 집합에 들어 있을 **수도** 있다"고 말하거나, "확실히 없다"고 말하는 확률적 자료구조다. false negative는 절대 발생하지 않고, false positive만 제한된 비율로 허용한다.

### 크기 결정

필요한 비트 수 `m`과 해시 함수 수 `k`는 다음 식으로 정해진다:

```
m = -(n × ln(p)) / (ln2)²
k = (m / n) × ln2
```

`n=1000`, `p=0.01`이면 약 9585비트, 7개 해시 함수가 나온다. 구현에서는 byte 단위로 올림한다:

```python
bit_count = math.ceil(-(expected_items * math.log(false_positive_rate)) / (math.log(2) ** 2))
hash_functions = max(1, round((bit_count / expected_items) * math.log(2)))
self.bits = bytearray(math.ceil(bit_count / 8))
```

### Double Hashing

k개의 독립적인 해시 함수를 진짜로 만들 필요는 없다. 두 개의 기본 해시 `h1`, `h2`만 있으면 `h1 + i × h2` 조합으로 k개 위치를 유도할 수 있다. Go 버전은 MurmurHash3를 사용했지만, Python 버전은 SHA-256을 seed와 결합하는 방식을 택했다:

```python
def _hash_value(key: str, seed: int) -> int:
    payload = f"{seed}:{key}".encode("utf-8")
    return int.from_bytes(hashlib.sha256(payload).digest()[:8], "big")
```

seed 0과 42에서 각각 h1, h2를 얻는다. SHA-256의 처음 8바이트만 취하면 64비트 정수가 되고, 비트 배열 크기로 모듈러 연산하면 위치가 결정된다.

### 직렬화

Bloom filter는 SSTable 파일에 함께 저장되어야 한다. `bit_count`와 `hash_functions` 두 개의 정수를 4바이트 big-endian으로 쓰고, 뒤에 비트 배열 전체를 덧붙인다:

```python
def serialize(self) -> bytes:
    return struct.pack(">II", self.bit_count, self.hash_functions) + bytes(self.bits)
```

복원할 때는 8바이트 헤더를 읽고 나머지를 `bytearray`로 복원한다.

## Sparse Index: 블록 경계만 기억하기

Bloom filter가 "있을 수도 있다"고 말하면, 그 다음에는 실제 데이터에서 키를 찾아야 한다. 모든 key-offset 매핑을 메모리에 올리면 빠르지만 메모리를 많이 쓴다. sparse index는 **N번째 레코드마다 하나씩만 인덱스에 넣는** 절충안이다.

```python
def build(self, entries: list[IndexEntry]) -> None:
    self.entries = [entry for index, entry in enumerate(entries) if index % self.block_size == 0]
```

`block_size=8`이면 64개 레코드 중 8개만 인덱스에 남는다. 조회할 때는 이진 탐색으로 "target key보다 작거나 같은 가장 큰 인덱스 엔트리"를 찾고, 그 블록 범위만 디스크에서 읽는다:

```python
def find_block(self, key: str, data_size: int) -> tuple[tuple[int, int], bool]:
    # ... 이진 탐색 ...
    start = self.entries[block].offset
    end = data_size if block + 1 >= len(self.entries) else self.entries[block + 1].offset
    return (start, end), True
```

전체 파일이 아니라 **한 블록만** 읽으면 된다.

## SSTable 파일 레이아웃

세 가지 컴포넌트를 하나의 파일에 합쳐야 한다. 레이아웃은 이렇다:

```
┌─────────────────────────┐
│     Data Section        │  encode_record() 연속 배치
│     (정렬된 KV 쌍들)     │
├─────────────────────────┤
│     Bloom Filter        │  serialize() 결과
├─────────────────────────┤
│     Sparse Index        │  JSON 직렬화
├─────────────────────────┤
│     Footer (40 bytes)   │  magic "SIF1" + offsets + sizes + block_size
└─────────────────────────┘
```

Footer 40바이트의 구조:

```python
footer = FOOTER_MAGIC + struct.pack(">QQQQI",
    self.bloom_offset,   # 8B: Bloom 시작 위치
    self.bloom_size,     # 8B: Bloom 크기
    self.index_offset,   # 8B: Index 시작 위치
    self.index_size,     # 8B: Index 크기
    self.block_size,     # 4B: 블록 크기
)
```

파일을 열 때는 **마지막 40바이트만 읽으면** Bloom filter와 sparse index의 위치를 알 수 있다. 이것이 footer 패턴의 핵심이다.

## 조회 경로: 세 단계 필터링

```python
def get_with_stats(self, key: str) -> tuple[str | None, bool, LookupStats, None]:
```

1. **Bloom filter 검사**: `might_contain(key)`이 False면 즉시 반환. `bloom_rejected=True`, `bytes_read=0`.
2. **Sparse index 탐색**: 이진 탐색으로 블록 범위 `(start, end)` 결정.
3. **블록 스캔**: 해당 범위만 `seek`+`read`로 읽고 순차 디코딩. 키를 지나치면 조기 종료.

테스트가 이 세 단계를 명확히 검증한다:

```python
# 없는 키 → Bloom reject, 디스크 I/O 없음
value, ok, stats, _ = table.get_with_stats("missing-key")
assert stats.bloom_rejected is True
assert stats.bytes_read == 0

# 있는 키 → 블록만 읽음
value, ok, stats, _ = table.get_with_stats(fmt_key(23))
assert 0 < stats.bytes_read < table.data_size
```

`stats.bytes_read < table.data_size`는 **전체 파일을 읽지 않았다**는 증거다.

## Binary Serialization: Go와의 공통 패턴

레코드 인코딩은 Go 02-sstable-format, Py 02-wal-recovery와 동일한 구조를 따른다:

```
[KeyLen 4B][ValLen 4B][Key bytes][Value bytes]
```

삭제 마커(tombstone)는 `ValLen = 0xFFFFFFFF`로 표현한다. Go의 `shared/serializer`가 정의한 것과 같은 규약이다. Python에서는 `struct.pack(">II", ...)` 로 big-endian 4바이트 정수 두 개를 기록한다.

## Go 버전과의 차이

같은 개념이지만 구현 선택이 다르다:

| 항목 | Go 06-index-filter | Python 03-index-filter |
|------|---------------------|------------------------|
| 해시 함수 | MurmurHash3 (shared/hash) | SHA-256 첫 8바이트 |
| 인덱스 직렬화 | 바이너리 (custom) | JSON |
| 테스트 수 | 6개 + GetWithStats | 4개 + get_with_stats |
| 외부 의존성 | shared/ 패키지 | hashlib (stdlib) |
| Tombstone | 동일 (0xFFFFFFFF) | 동일 |

Python 버전이 SHA-256을 쓴 이유는 외부 해시 라이브러리 의존 없이 순수 stdlib만으로 동작하게 하기 위해서였다. MurmurHash3의 분포 특성은 Bloom filter에 더 적합하지만, 학습 목적에서는 SHA-256으로도 충분한 결과를 얻을 수 있다.

## LookupStats: 눈에 보이는 성능 지표

```python
@dataclass(slots=True)
class LookupStats:
    bloom_rejected: bool = False
    bytes_read: int = 0
    block_range: tuple[int, int] = (0, 0)
```

이 dataclass는 단순한 디버깅 도구가 아니라 **설계 의도를 테스트로 증명하는 도구**다. Bloom filter가 제대로 걸러냈는지, 블록 범위가 전체보다 작은지를 수치로 확인할 수 있다. `slots=True`는 메모리 효율성과 접근 속도를 위한 Python 최적화 옵션이다.

## 마무리

이 프로젝트는 "디스크를 덜 읽는 법"에 대한 두 가지 답을 SSTable 하나에 합쳤다. Bloom filter는 없는 키를 디스크 접근 없이 거절하고, sparse index는 있는 키의 위치를 좁은 블록으로 제한한다. footer metadata가 이 두 구조를 파일 끝에서 발견 가능하게 만들고, 40바이트만 읽으면 전체 인덱스를 복원할 수 있다.

소스코드에서는 드러나지 않는 핵심 통찰: **이 세 가지(Bloom, sparse index, footer)는 독립적으로 설계되었지만, SSTable 파일 하나에 합쳐졌을 때 비로소 의미를 갖는다.** 각각은 단순하지만, 조합이 실제 데이터베이스의 읽기 경로를 만든다.
