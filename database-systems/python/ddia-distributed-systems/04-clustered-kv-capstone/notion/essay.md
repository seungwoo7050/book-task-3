# "분산 데이터베이스의 뼈대를 세우는 법" — Python Clustered KV Capstone

## 모든 것이 합쳐지는 순간

이전 프로젝트들은 각각 하나의 문제를 해결했다:
- **DDIA-02**: leader-follower 복제 (데이터를 두 곳에 유지)
- **DDIA-03**: consistent hash ring (키를 어떤 서버로 보낼지)
- **DB-01~02**: JSON Lines 기반 디스크 저장

이 프로젝트는 세 가지를 **하나의 동작하는 클러스터**로 통합한다. Python 분산 시스템 트랙의 마지막 프로젝트이자, Go DDIA-05의 Python 대응이다.

## 의도적 축소: Raft 없이

Go 트랙에는 04-raft-lite가 있었다. Python 트랙에는 없다. 이 프로젝트는 **정적 토폴로지(static topology)**를 사용한다. 리더가 누구인지 미리 정해져 있고, 합의 알고리즘으로 선출하지 않는다. 이 결정으로 핵심 데이터 흐름에 집중할 수 있다.

## DiskStore: JSON Lines Append-Only Log

```python
class DiskStore:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.data: dict[str, str] = {}
        self.log: list[Operation] = []
        self._load()
```

Go 버전은 JSON Lines append-only log + `LoadStore` 복구를 별도의 모듈로 가지고 있었다. Python에서는 `DiskStore` 하나가 모두 담당한다.

### Operation: 로그 엔트리

```python
@dataclass(slots=True)
class Operation:
    offset: int
    op_type: str
    key: str
    value: str | None = None
```

DDIA-02의 `LogEntry`와 같은 역할이지만, 이름을 `Operation`으로 바꿨다. `offset`은 순차적으로 증가하고, `op_type`은 `"put"` 또는 `"delete"`.

### Append + Flush

```python
def apply(self, op: Operation) -> None:
    if op.offset < len(self.log):
        return    # 이미 적용됨 → 멱등
    if op.offset != len(self.log):
        raise ValueError(f"store: non-sequential offset {op.offset}")
    with self.path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(asdict(op)) + "\n")
    self._apply_in_memory(op)
    self.log.append(op)
```

핵심 설계:
1. **멱등성**: `op.offset < len(self.log)` 이면 무시 → 같은 operation을 여러 번 받아도 안전
2. **순차성 검사**: offset이 연속이 아니면 에러
3. **디스크 먼저, 메모리 나중**: `open("a")` + `write` → `_apply_in_memory`

### 복구: _load

```python
def _load(self) -> None:
    for line in self.path.read_text(encoding="utf-8").splitlines():
        payload = json.loads(line)
        op = Operation(...)
        self._apply_in_memory(op)
        self.log.append(op)
```

파일을 한 줄씩 읽어서 in-memory state를 재구축한다. `restart_node()`는 이 `_load()`를 다시 호출하는 것뿐이다.

## ShardRing: 키를 샤드로

```python
class ShardRing:
    def add_shard(self, shard_id: str) -> None:
        for index in range(self.virtual_nodes):
            bisect.insort(self.ring, RingEntry(hash_value(f"{shard_id}#v{index}"), shard_id))
```

DDIA-03의 `Ring`을 거의 그대로 가져왔지만, 키를 **노드**가 아니라 **샤드**로 라우팅한다. 샤드와 노드는 다르다:
- **샤드(shard)**: 데이터의 논리적 파티션 (예: shard-a, shard-b)
- **노드(node)**: 물리적 서버 (예: node-1, node-2, node-3)

하나의 샤드는 여러 노드에 복제될 수 있다.

## ReplicaGroup: 샤드와 노드의 매핑

```python
@dataclass(slots=True)
class ReplicaGroup:
    shard_id: str
    leader: str
    followers: list[str] = field(default_factory=list)
```

정적 토폴로지의 핵심 구조. 각 샤드마다 리더 하나와 팔로워 목록이 정해져 있다.

테스트의 토폴로지:

```python
[
    ReplicaGroup("shard-a", "node-1", ["node-2"]),
    ReplicaGroup("shard-b", "node-2", ["node-3"]),
]
```

node-2는 shard-a의 follower이면서 동시에 shard-b의 leader다. 하나의 노드가 여러 역할을 가질 수 있다.

## Cluster: 통합 오케스트레이터

```python
class Cluster:
    def __init__(self, data_dir, groups, virtual_nodes=64):
        for group in groups:
            self.router.add_shard(group.shard_id)
            for node_id in [group.leader, *group.followers]:
                node = self.nodes.setdefault(node_id, Node(node_id))
                node.stores[group.shard_id] = DiskStore(...)
```

초기화 시 모든 노드의 모든 DiskStore를 생성한다. 디렉토리 구조:

```
data_dir/
├── node-1/
│   └── shard-a.log
├── node-2/
│   ├── shard-a.log    (follower)
│   └── shard-b.log    (leader)
└── node-3/
    └── shard-b.log
```

### 쓰기 경로

```python
def put(self, key: str, value: str) -> str:
    shard_id = self.route_shard(key)
    group = self.groups[shard_id]
    self.nodes[group.leader].stores[shard_id].append_put(key, value)
    if self.auto_replicate:
        for follower_id in group.followers:
            self.sync_follower(shard_id, follower_id)
    return shard_id
```

1. 키 → 샤드 라우팅
2. 해당 샤드의 리더에게 기록
3. `auto_replicate=True`이면 팔로워에게 동기적 복제

### 복제: sync_follower

```python
def sync_follower(self, shard_id, follower_id):
    leader_store = self.nodes[group.leader].stores[shard_id]
    follower_store = self.nodes[follower_id].stores[shard_id]
    entries = leader_store.entries_from(follower_store.watermark() + 1)
    for entry in entries:
        follower_store.apply(entry)
```

DDIA-02의 `replicate_once`와 동일한 패턴: watermark + 1부터 가져와서 적용. `DiskStore.apply()`의 멱등성으로 재전송 안전.

### 읽기 경로

```python
def read(self, key: str) -> tuple[str, bool, str]:
    shard_id = self.route_shard(key)
    value, ok = self.nodes[group.leader].stores[shard_id].get(key)
    return value, ok, shard_id

def read_from_node(self, node_id, key):
    shard_id = self.route_shard(key)
    return node.stores[shard_id].get(key)
```

`read()`는 항상 리더에서 읽고, `read_from_node()`는 특정 노드에서 읽는다. 팔로워 읽기로 읽기 부하를 분산할 수 있다.

### 노드 재시작

```python
def restart_node(self, node_id: str) -> None:
    node = self.nodes[node_id]
    for store in node.stores.values():
        store.reload()
```

`reload()` = `_load()`. 디스크의 JSON Lines에서 in-memory state를 재구축한다.

## FastAPI 서비스 경계

```python
def create_app(cluster: Cluster) -> FastAPI:
    app = FastAPI()

    @app.put("/kv/{key}")
    def put_value(key: str, payload: ValuePayload):
        shard_id = cluster.put(key, payload.value)
        return {"key": key, "value": payload.value, "shard_id": shard_id}
```

FastAPI는 **HTTP 경계**만 담당한다. 모든 비즈니스 로직은 `Cluster` 클래스에 있다. 테스트에서 `TestClient`로 HTTP 레벨 round-trip을 검증한다.

Go 버전에서는 HTTP 서버를 직접 구현했지만, Python에서는 FastAPI + Pydantic의 자동 검증을 활용한다.

## Go 버전과의 비교

| 항목 | Go DDIA-05 | Python DDIA-04 |
|------|-----------|----------------|
| 합의 | Raft (DDIA-04 통합) | 없음 (정적 토폴로지) |
| 저장소 | JSON Lines + LoadStore | DiskStore (JSON Lines) |
| HTTP | net/http 직접 | FastAPI |
| 해시 함수 | MurmurHash3 | SHA-256 |
| 가상 노드 | 150 | 64 |
| 테스트 수 | 3개 | 4개 (FastAPI 포함) |
| 코드량 | ~300줄 | ~200줄 (core) + ~40줄 (app) |

Python 버전이 더 짧은 이유: Raft 통합이 빠지고, FastAPI가 라우팅/직렬화를 자동화.

## 마무리

이 프로젝트는 "작은 분산 데이터베이스"의 모든 계층을 한 곳에 모았다. 키 라우팅(어떤 샤드?), 리더 쓰기(어떤 노드?), 팔로워 복제(어떻게 따라가?), 디스크 저장(죽어도 살아남기), HTTP 경계(외부 접근점).

소스코드에서 드러나지 않는 핵심: **각 계층의 코드는 이전 프로젝트에서 거의 그대로 가져왔다.** DiskStore는 DB-01/02의 JSON Lines, ShardRing은 DDIA-03의 consistent hash, sync_follower는 DDIA-02의 replicate_once. 캡스톤의 가치는 새로운 알고리즘이 아니라, **독립적인 조각들이 하나로 합쳐지는 통합 경험**에 있다.
