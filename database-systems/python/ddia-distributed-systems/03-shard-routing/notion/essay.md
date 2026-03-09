# "키를 어떤 서버에 넣을 것인가" — Python으로 Consistent Hash Ring 만들기

## 단순한 해시 분배의 문제

3대 서버에 데이터를 나누는 가장 쉬운 방법: `hash(key) % 3`. 하지만 서버가 4대가 되면 `hash(key) % 4`로 바뀌고, **거의 모든 키가 다른 서버로 이동**한다. 서버 한 대 추가에 전체 데이터가 재배치되는 것은 현실적이지 않다.

Consistent hashing은 이 문제의 해결책이다: 서버 하나가 추가되거나 제거될 때, **전체 키의 일부만** 이동한다.

## Hash Ring의 기본 아이디어

키와 서버를 같은 해시 공간에 배치한다. 키의 해시값에서 시계 방향으로 가장 가까운 서버가 그 키의 담당이다.

```python
def hash_value(value: str) -> int:
    return int.from_bytes(hashlib.sha256(value.encode("utf-8")).digest()[:8], "big")
```

SHA-256의 처음 8바이트를 64비트 정수로 변환한다. Go 버전은 MurmurHash3를 사용했지만, Python에서는 03-index-filter와 마찬가지로 stdlib의 hashlib을 사용한다.

## Virtual Nodes: 균등 분배의 비밀

실제 서버가 3대면 링 위의 점도 3개다. 해시 함수의 분포가 아무리 좋아도, 3개 점으로 균등 분배는 어렵다. **가상 노드(virtual node)**가 이 문제를 해결한다. 각 서버를 링 위에 150개의 점으로 배치한다.

```python
def add_node(self, node_id: str) -> None:
    if node_id in self._nodes:
        return
    self._nodes.add(node_id)
    for index in range(self.virtual_nodes):
        entry = RingEntry(hash_value(f"{node_id}#v{index}"), node_id)
        bisect.insort(self.ring, entry)
```

`"{node_id}#v{index}"` — 가상 노드의 해시 키. Go 버전에서도 동일한 `"nodeID#v<i>"` 패턴을 사용한다. `bisect.insort`로 정렬된 리스트에 삽입하여 이진 탐색이 가능한 상태를 유지한다.

### RingEntry: 정렬 가능한 데이터

```python
@dataclass(slots=True, order=True)
class RingEntry:
    hash_value: int
    node_id: str
```

`order=True`로 `<`, `>` 비교가 가능해진다. `bisect.insort`가 이 비교를 사용한다.

## 키 라우팅: bisect_left

```python
def node_for_key(self, key: str) -> tuple[str, bool]:
    if not self.ring:
        return "", False
    target = hash_value(key)
    hashes = [entry.hash_value for entry in self.ring]
    index = bisect.bisect_left(hashes, target)
    if index == len(self.ring):
        index = 0    # 링의 끝을 넘으면 처음으로
    return self.ring[index].node_id, True
```

"시계 방향으로 가장 가까운 서버"를 `bisect.bisect_left`로 O(log n)에 찾는다. `index == len(self.ring)`이면 링의 끝을 지났으므로 처음(index 0)으로 돌아간다. 이것이 "링"인 이유다.

테스트가 세 가지 시나리오를 확인한다:

```python
# 빈 링
assert ring.node_for_key("key") == ("", False)

# 단일 노드 → 모든 키가 그 노드로
ring.add_node("node-a")
assert ring.node_for_key("key") == ("node-a", True)
```

## 분포와 재배치 검증

```python
def test_distribution_and_rebalance():
    ring = Ring(150)
    ring.add_node("node-a")
    ring.add_node("node-b")
    ring.add_node("node-c")

    keys = [f"key-{index}" for index in range(3000)]
    for node_id in counts:
        share = counts[node_id] / 3000
        assert 0.2 < share < 0.5    # 각 노드가 20~50% 범위
```

3000개 키, 3개 노드, 각 150개 가상 노드. 이상적으로는 33%씩이지만, 20~50% 범위면 합격이다. 가상 노드가 없으면 한 노드에 80%가 몰릴 수도 있다.

### 재배치 측정

```python
movement_keys = keys[:1000]
before = ring.assignments(movement_keys)
ring.add_node("node-d")
moved = ring.moved_keys(movement_keys, before)
assert 50 < moved < 500    # 1000개 중 50~500개만 이동
```

노드 하나 추가 시 1000개 키 중 50~500개만 이동한다. `% n`이었다면 거의 전부가 이동했을 것이다. 이것이 consistent hashing의 핵심 가치다.

## 노드 제거

```python
def remove_node(self, node_id: str) -> None:
    self._nodes.discard(node_id)
    self.ring = [entry for entry in self.ring if entry.node_id != node_id]
```

리스트 필터링으로 해당 노드의 모든 가상 노드를 제거한다. 남은 노드들이 제거된 노드의 키를 자연스럽게 흡수한다.

## Router: 배치 라우팅

```python
class Router:
    def route_batch(self, keys: list[str]) -> dict[str, list[str]]:
        grouped: dict[str, list[str]] = {}
        for key in keys:
            node_id, ok = self.ring.node_for_key(key)
            if ok:
                grouped.setdefault(node_id, []).append(key)
        return grouped
```

여러 키를 한 번에 라우팅하고, 노드별로 그룹화한다. 실제 시스템에서는 이 그룹별로 네트워크 요청을 보내면 된다.

## Go 버전과의 차이

| 항목 | Go DDIA-03 | Python DDIA-03 |
|------|-----------|----------------|
| 해시 함수 | MurmurHash3 (shared/hash) | SHA-256 (hashlib) |
| 정렬 | sort.Search | bisect.bisect_left |
| 가상 노드 기본값 | 150 | 150 (동일) |
| ring 자료구조 | []RingEntry 정렬 | list[RingEntry] 정렬 |
| moved_keys | Ring 메서드 | Ring 메서드 (동일) |
| 테스트 수 | 3개 | 3개 |

구조적으로 거의 동일하다. 해시 함수와 이진 탐색 API만 다르다.

## 마무리

Consistent hashing은 "서버가 추가되거나 제거될 때 최소한의 키만 이동시키는" 문제를 해결한다. 가상 노드는 균등 분배를 보장하고, `bisect` 기반 이진 탐색으로 O(log n) 라우팅이 가능하다.

소스코드에서 드러나지 않는 핵심: **가상 노드 수(150)는 경험적 값이다.** 너무 적으면 분포가 불균등하고(hotspot), 너무 많으면 메모리와 탐색 시간이 늘어난다. 3~5개 노드에서 150은 충분한 균등성과 적절한 메모리 사용의 균형점이다.
