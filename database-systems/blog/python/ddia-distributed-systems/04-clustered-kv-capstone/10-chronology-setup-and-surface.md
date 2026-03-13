# 10 Python 분산 트랙의 통합 지점

## Day 1
### Session 1

이 프로젝트를 보면 웹 API가 먼저 보인다. 하지만 핵심은 `FastAPI`가 아니라 `Cluster` core다.

```python
class Cluster:
    def __init__(self, data_dir: str | Path, groups: list[ReplicaGroup], virtual_nodes: int = 64) -> None:
        self.router = ShardRing(virtual_nodes)
        self.groups = {group.shard_id: group for group in groups}
        self.nodes: dict[str, Node] = {}
```

여기서 이미 세 축이 결합된다.

1. shard routing
2. replica group topology
3. node-local disk store

- 목표: framework surface와 core pipeline 경계 분리
- 진행: `core.py`를 먼저 읽고, `app.py`는 마지막에 확인

CLI:

```bash
cd python/ddia-distributed-systems/projects/04-clustered-kv-capstone
grep -n "def test_" tests/test_clustered_kv.py
```

```text
6:def test_write_routes_to_leader_and_replicates(tmp_path):
20:def test_follower_catch_up_and_delete(tmp_path):
35:def test_restart_node_loads_from_disk(tmp_path):
48:def test_fastapi_round_trip(tmp_path):
```

테스트 순서도 core -> boundary 흐름으로 배치되어 있다.

### Session 2

`DiskStore`를 보면 복제 단위가 state snapshot이 아니라 operation log임을 다시 확인할 수 있다.

```python
with self.path.open("a", encoding="utf-8") as handle:
    handle.write(json.dumps(asdict(op)) + "\n")
self._apply_in_memory(op)
self.log.append(op)
```

메모리 state와 디스크 로그를 함께 유지하는 최소 durable replica 모델이다.

다음 질문:

- put/delete에서 shard 선택, leader append, follower sync가 어떤 순서로 연결되나
- node restart 시 로그 기반 복구가 실제로 동작하나
