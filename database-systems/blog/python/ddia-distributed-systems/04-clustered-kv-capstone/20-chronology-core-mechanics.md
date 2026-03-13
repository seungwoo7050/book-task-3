# 20 Core Mechanics

## Day 1
### Session 3

write path는 `Cluster.put()`에서 완전히 드러난다.

```python
shard_id = self.route_shard(key)
group = self.groups[shard_id]
self.nodes[group.leader].stores[shard_id].append_put(key, value)
if self.auto_replicate:
    for follower_id in group.followers:
        self.sync_follower(shard_id, follower_id)
```

순서가 핵심이다.

1. key -> shard route
2. shard leader에 append
3. follower catch-up (auto_replicate 켜진 경우)

`sync_follower()`는 follower watermark 이후 엔트리만 적용한다.

```python
entries = leader_store.entries_from(follower_store.watermark() + 1)
for entry in entries:
    follower_store.apply(entry)
```

- 목표: routing + replication 결합 write pipeline 확인
- 진행: `test_write_routes_to_leader_and_replicates`, `test_follower_catch_up_and_delete` 대조

CLI:

```bash
cd python/ddia-distributed-systems/projects/04-clustered-kv-capstone
sed -n '118,260p' src/clustered_kv/core.py
sed -n '1,35p' tests/test_clustered_kv.py
```

### Session 4

restart 경계도 명확하다.

```python
def restart_node(self, node_id: str) -> None:
    node = self.nodes[node_id]
    for store in node.stores.values():
        store.reload()
```

`test_restart_node_loads_from_disk`가 이 경계를 고정한다. 즉 follower는 메모리 캐시가 아니라 디스크 로그 재적재로 복구된다.

다음 질문:

- read quorum을 추가하면 `read()`는 리더 고정에서 어떻게 바뀌어야 하나
- election이 붙으면 `group.leader` 갱신은 누가 책임져야 하나