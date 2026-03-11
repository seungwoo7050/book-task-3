# 03 Shard Routing — 개발 타임라인

## Phase 0: 환경 준비

```bash
cd python/ddia-distributed-systems/projects/03-shard-routing
python3 --version
# Python 3.14.x

python3 -m pip install -U pytest
```

### 디렉토리 구조 생성

```bash
mkdir -p src/shard_routing tests docs/concepts docs/references
touch src/shard_routing/__init__.py
touch src/shard_routing/__main__.py
touch src/shard_routing/core.py
touch tests/test_shard_routing.py
```

---

## Phase 1: 해시 함수와 RingEntry

### 1.1 hash_value 함수

```python
def hash_value(value: str) -> int:
    return int.from_bytes(hashlib.sha256(value.encode("utf-8")).digest()[:8], "big")
```

**결정**: Go는 shared/hash의 MurmurHash3를 사용했지만, Python에서는 외부 의존성 없이 hashlib.sha256 사용. 03-index-filter와 동일한 패턴.

### 1.2 RingEntry dataclass

```python
@dataclass(slots=True, order=True)
class RingEntry:
    hash_value: int
    node_id: str
```

**결정**: `order=True`로 `<`, `>` 비교 자동 생성. `bisect.insort`가 이 비교를 사용하여 정렬된 삽입. 비교 시 `hash_value` → `node_id` 순서로 정렬됨 (dataclass 필드 순서).

---

## Phase 2: Ring 구현

### 2.1 add_node — 가상 노드 배치

```python
class Ring:
    def __init__(self, virtual_nodes: int = 150) -> None:
        self.virtual_nodes = virtual_nodes or 150
        self.ring: list[RingEntry] = []
        self._nodes: set[str] = set()
```

**결정**: virtual_nodes 기본값 150. Go 버전과 동일. `_nodes` set으로 중복 추가 방지.

```python
def add_node(self, node_id: str) -> None:
    for index in range(self.virtual_nodes):
        entry = RingEntry(hash_value(f"{node_id}#v{index}"), node_id)
        bisect.insort(self.ring, entry)
```

`f"{node_id}#v{index}"` — Go와 동일한 가상 노드 키 패턴.

### 2.2 remove_node — 리스트 필터링

```python
def remove_node(self, node_id: str) -> None:
    self._nodes.discard(node_id)
    self.ring = [entry for entry in self.ring if entry.node_id != node_id]
```

**결정**: in-place 제거가 아닌 새 리스트 생성. O(n)이지만 단순하고 정확.

### 2.3 node_for_key — 이진 탐색

```python
def node_for_key(self, key: str) -> tuple[str, bool]:
    target = hash_value(key)
    hashes = [entry.hash_value for entry in self.ring]
    index = bisect.bisect_left(hashes, target)
    if index == len(self.ring):
        index = 0
    return self.ring[index].node_id, True
```

`bisect.bisect_left` — Go의 `sort.Search`에 해당. O(log n).

### 2.4 빈 링과 단일 노드 테스트

```bash
PYTHONPATH=src python3 -m pytest tests/test_shard_routing.py::test_empty_and_single_node_routing -v
```

---

## Phase 3: 분포와 재배치

### 3.1 assignments와 moved_keys

```python
def assignments(self, keys: list[str]) -> dict[str, str]:
    result = {}
    for key in keys:
        node_id, ok = self.node_for_key(key)
        if ok:
            result[key] = node_id
    return result

def moved_keys(self, keys: list[str], previous: dict[str, str]) -> int:
    current = self.assignments(keys)
    return sum(1 for key in keys if previous.get(key) and previous[key] != current.get(key))
```

"이전 배치"와 "현재 배치"를 비교하여 이동한 키 수를 세는 accounting 함수.

### 3.2 분포 테스트

```bash
PYTHONPATH=src python3 -m pytest tests/test_shard_routing.py::test_distribution_and_rebalance -v
```

3000개 키, 3개 노드: 각 20~50% 범위.  
노드 추가 시: 1000개 중 50~500개만 이동.  
노드 제거 후: 제거된 노드로 라우팅되는 키 없음.

---

## Phase 4: Router

### 4.1 Router 클래스

```python
class Router:
    def __init__(self, ring: Ring) -> None:
        self.ring = ring

    def route(self, key: str) -> tuple[str, bool]:
        return self.ring.node_for_key(key)

    def route_batch(self, keys: list[str]) -> dict[str, list[str]]:
```

Ring의 래퍼. `route_batch`로 키를 노드별로 그룹화.

### 4.2 배치 라우팅 테스트

```bash
PYTHONPATH=src python3 -m pytest tests/test_shard_routing.py::test_batch_routing -v
```

5개 키 → 모든 키가 어떤 노드에든 배치됨 (총합 == 5).

---

## Phase 5: Demo와 마무리

### 5.1 demo 실행

```bash
PYTHONPATH=src python3 -m shard_routing
# {'node-a': ['k1', ...], 'node-b': ['k2', ...]}
```

### 5.2 전체 테스트

```bash
PYTHONPATH=src python3 -m pytest tests/ -v
```

3개 테스트 모두 통과 확인.

---

## 소스코드에서 드러나지 않는 결정들

1. **SHA-256 vs MurmurHash3**: Go는 shared/hash에 종속되지만, Python은 stdlib만 사용. 해시 품질보다 이식성 우선.

2. **bisect.insort 사용**: 가상 노드 수(150)가 적으므로 삽입 시 O(n) shift 비용은 무시 가능. 정렬된 리스트 + 이진 탐색이 트리보다 단순.

3. **hashes 리스트 매번 생성**: `node_for_key`에서 `[e.hash_value for e in self.ring]`을 매번 만듦. 캐싱하면 빠르지만, 간결성 우선. 실제 프로덕션에서는 캐싱 필요.

4. **moved_keys 느슨한 bound**: `50 < moved < 500`. 이상적으로는 ~250(1000/4)이지만, 해시 분포에 따라 변동. 넓은 범위로 flaky test 방지.

5. **virtual_nodes=150**: 경험적 값. 3~5개 물리 노드에서 충분한 균등성 보장. 노드 수가 늘어나면 가상 노드를 줄일 수도 있음.

6. **`order=True` dataclass**: RingEntry의 비교 연산자를 자동 생성. 필드 순서(hash_value → node_id)가 비교 우선순위. hash_value로 정렬하되, 같은 hash면 node_id로 tiebreak.
