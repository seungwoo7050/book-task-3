# 04 Clustered KV Capstone — 개발 타임라인

## Phase 0: 환경 준비

```bash
cd python/ddia-distributed-systems/04-clustered-kv-capstone
python3 --version
# Python 3.14.x

python3 -m pip install -e .[dev]
```

### pyproject.toml에서 FastAPI 의존성 확인

```toml
[project]
name = "clustered-kv-capstone"
dependencies = ["fastapi>=0.110", "pydantic>=2", "httpx>=0.27"]

[project.optional-dependencies]
dev = ["pytest>=8,<9"]
```

**결정**: 이 프로젝트만 외부 의존성(FastAPI, Pydantic, httpx)이 있음. `pip install -e .[dev]`로 설치.

### 디렉토리 구조 생성

```bash
mkdir -p src/clustered_kv tests docs/concepts docs/references
touch src/clustered_kv/__init__.py
touch src/clustered_kv/__main__.py
touch src/clustered_kv/core.py
touch src/clustered_kv/app.py
touch tests/test_clustered_kv.py
```

**결정**: 핵심 로직은 `core.py`, FastAPI 경계는 `app.py`로 분리. 테스트에서 core만 테스트하거나 HTTP까지 테스트 가능.

---

## Phase 1: Operation과 DiskStore

### 1.1 Operation dataclass

```python
@dataclass(slots=True)
class Operation:
    offset: int
    op_type: str
    key: str
    value: str | None = None
```

DDIA-02의 `LogEntry`를 rename. `value`에 기본값을 넣어 delete 시 생략 가능.

### 1.2 DiskStore — JSON Lines append-only

```python
class DiskStore:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.data: dict[str, str] = {}
        self.log: list[Operation] = []
        self._load()
```

**결정**: 생성자에서 `_load()` 호출. 파일이 있으면 복구, 없으면 빈 상태로 시작.

### 1.3 apply — 멱등적 디스크 쓰기

```python
def apply(self, op: Operation) -> None:
    if op.offset < len(self.log):
        return  # idempotent
    with self.path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(asdict(op)) + "\n")
    self._apply_in_memory(op)
    self.log.append(op)
```

**결정**: `dataclasses.asdict(op)`로 JSON 직렬화. 각 필드를 수동으로 매핑하지 않음.

### 1.4 _load — 디스크에서 복구

```python
def _load(self) -> None:
    self.path.parent.mkdir(parents=True, exist_ok=True)
    self.path.touch(exist_ok=True)
    for line in self.path.read_text(encoding="utf-8").splitlines():
        if not line:
            continue
        payload = json.loads(line)
        op = Operation(...)
        self._apply_in_memory(op)
        self.log.append(op)
```

**결정**: `mkdir(parents=True)` + `touch(exist_ok=True)` — 디렉토리와 파일이 없어도 에러 없이 생성.

### 1.5 watermark과 entries_from

```python
def watermark(self) -> int:
    return len(self.log) - 1

def entries_from(self, offset: int) -> list[Operation]:
    return list(self.log[max(offset, 0):])
```

DDIA-02의 복제 프로토콜을 위한 인터페이스.

---

## Phase 2: ShardRing과 ReplicaGroup

### 2.1 ShardRing

```python
class ShardRing:
    def __init__(self, virtual_nodes: int = 64) -> None:
```

DDIA-03의 Ring을 재구현. **다른 점**: 키를 노드가 아니라 **샤드**로 라우팅. virtual_nodes 기본값은 64 (DDIA-03의 150보다 적음).

### 2.2 ReplicaGroup

```python
@dataclass(slots=True)
class ReplicaGroup:
    shard_id: str
    leader: str
    followers: list[str] = field(default_factory=list)
```

정적 토폴로지 정의. Go 버전의 `ReplicaGroup`과 동일 구조.

### 2.3 Node

```python
@dataclass(slots=True)
class Node:
    node_id: str
    stores: dict[str, DiskStore] = field(default_factory=dict)
```

하나의 노드가 여러 샤드의 스토어를 가질 수 있음.

---

## Phase 3: Cluster 통합

### 3.1 초기화

```python
class Cluster:
    def __init__(self, data_dir, groups, virtual_nodes=64):
        for group in groups:
            self.router.add_shard(group.shard_id)
            for node_id in [group.leader, *group.followers]:
                node = self.nodes.setdefault(node_id, Node(node_id))
                node.stores[group.shard_id] = DiskStore(...)
```

모든 노드의 모든 DiskStore를 미리 생성. 디렉토리 구조: `data_dir/{node_id}/{shard_id}.log`

### 3.2 put / delete

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
2. 리더에 기록
3. auto_replicate이면 동기 복제

### 3.3 sync_follower

```python
def sync_follower(self, shard_id, follower_id):
    entries = leader_store.entries_from(follower_store.watermark() + 1)
    for entry in entries:
        follower_store.apply(entry)
```

DDIA-02의 `replicate_once` 패턴.

### 3.4 read / read_from_node

`read()`: 항상 리더에서 읽기.  
`read_from_node()`: 특정 노드에서 읽기 (테스트에서 팔로워 상태 확인용).

### 3.5 restart_node

```python
def restart_node(self, node_id: str) -> None:
    for store in node.stores.values():
        store.reload()
```

모든 스토어를 디스크에서 재로드.

### 3.6 핵심 테스트 실행

```bash
PYTHONPATH=src python3 -m pytest tests/test_clustered_kv.py::test_write_routes_to_leader_and_replicates -v
PYTHONPATH=src python3 -m pytest tests/test_clustered_kv.py::test_follower_catch_up_and_delete -v
PYTHONPATH=src python3 -m pytest tests/test_clustered_kv.py::test_restart_node_loads_from_disk -v
```

---

## Phase 4: FastAPI 서비스 경계

### 4.1 create_app

```python
def create_app(cluster: Cluster) -> FastAPI:
    app = FastAPI()

    @app.put("/kv/{key}")
    def put_value(key: str, payload: ValuePayload):
        shard_id = cluster.put(key, payload.value)
        return {"key": key, "value": payload.value, "shard_id": shard_id}
```

**결정**: FastAPI의 `TestClient`로 HTTP 경계 테스트. 실제 소켓 서버 없이 in-process 테스트.

### 4.2 ValuePayload

```python
class ValuePayload(BaseModel):
    value: str
```

Pydantic 모델로 요청 검증 자동화. Go에서 수동으로 JSON 파싱한 부분을 프레임워크에 위임.

### 4.3 FastAPI 테스트

```bash
PYTHONPATH=src python3 -m pytest tests/test_clustered_kv.py::test_fastapi_round_trip -v
```

PUT → GET → DELETE → GET 순서로 전체 CRUD 검증.

---

## Phase 5: Demo와 마무리

### 5.1 demo 실행

```bash
PYTHONPATH=src python3 -m clustered_kv
# {"key": "alpha", "value": "1", "found": true, "shard_id": "shard-a"}
```

### 5.2 전체 테스트

```bash
PYTHONPATH=src python3 -m pytest tests/ -v
```

4개 테스트 모두 통과 확인.

---

## 소스코드에서 드러나지 않는 결정들

1. **Raft 배제**: Go 트랙의 04-raft-lite를 Python에서는 건너뜀. 정적 리더 배치로 단순화. 합의 알고리즘 없이도 데이터 흐름의 전체 모습을 볼 수 있다는 판단.

2. **virtual_nodes=64**: DDIA-03은 150, 여기서는 64. 샤드 수가 적어(2개) 가상 노드를 줄여도 충분한 분배.

3. **auto_replicate 플래그**: 테스트에서 복제를 꺼서 "팔로워에 아직 없음"을 확인하고, 수동 sync 후 "팔로워에 있음"을 확인. 복제의 동작을 세밀하게 테스트하기 위한 설계.

4. **`dataclasses.asdict`**: Operation을 JSON으로 직렬화할 때 수동 매핑 대신 라이브러리 함수 활용. Go에서 `json.Marshal`이 struct tag를 읽는 것에 해당.

5. **FastAPI TestClient**: httpx 기반. 실제 서버를 띄우지 않고 ASGI 앱을 직접 호출. 테스트 속도와 격리성 확보.

6. **Node 구조**: 하나의 노드가 여러 샤드의 스토어를 가짐. `stores: dict[str, DiskStore]`로 샤드별 독립 저장. 이 구조가 node-2가 shard-a의 follower이면서 shard-b의 leader인 상황을 가능하게 함.

7. **JSON Lines 포맷**: `json.dumps(asdict(op)) + "\n"`. 한 줄에 하나의 operation. 복구 시 줄 단위로 파싱하면 됨. 바이너리 포맷보다 디버깅 편리.
