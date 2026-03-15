# Scope, Surface, And The First Write

## 1. 문제 범위는 통합이지만 control plane은 아니다

[`problem/README.md`](/Users/woopinbell/work/book-task-3/database-systems/python/ddia-distributed-systems/projects/04-clustered-kv-capstone/problem/README.md)는 key routing, shard별 leader/follower 선택, leader write의 log-backed store 기록, follower catch-up, restart 후 disk replay, leader/follower read까지 요구한다.

하지만 동시에 dynamic membership, automatic failover, consensus leader election, production deployment는 뺀다고 선언한다. 이 capstone은 통합 프로젝트이지만, 어디까지나 static topology 안에서만 통합된다.

## 2. 코드 표면은 세 층으로 나뉜다

핵심 계층은 [`core.py`](/Users/woopinbell/work/book-task-3/database-systems/python/ddia-distributed-systems/projects/04-clustered-kv-capstone/src/clustered_kv/core.py)에 모여 있다.

- `DiskStore`: append-only JSON line log와 in-memory state를 함께 가진다.
- `ShardRing`: key를 shard id로 라우팅한다.
- `Cluster`: replica group, node, store를 묶고 write/read/sync/restart orchestration을 담당한다.

여기에 [`app.py`](/Users/woopinbell/work/book-task-3/database-systems/python/ddia-distributed-systems/projects/04-clustered-kv-capstone/src/clustered_kv/app.py)가 FastAPI surface를 얹는다. `PUT /kv/{key}`, `GET /kv/{key}`, `DELETE /kv/{key}`는 모두 결국 `Cluster` 메서드로 내려간다.

## 3. 첫 write는 route -> leader append -> optional follower sync 순서다

`Cluster.put()`을 보면 흐름이 정확히 드러난다.

1. `route_shard(key)`로 shard id를 구한다.
2. 해당 replica group의 leader store에 `append_put()`을 호출한다.
3. `auto_replicate`가 켜져 있으면 follower마다 `sync_follower()`를 돌린다.

이 순서는 docs의 [`replicated-write-pipeline.md`](/Users/woopinbell/work/book-task-3/database-systems/python/ddia-distributed-systems/projects/04-clustered-kv-capstone/docs/concepts/replicated-write-pipeline.md) 설명과 그대로 맞아떨어진다. 네트워크 호출은 없지만, write ordering 의미는 leader-first다.

## 4. 실제 데모는 leader read surface만 노출한다

2026-03-14에 아래 명령을 다시 실행했다.

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/python/ddia-distributed-systems/projects/04-clustered-kv-capstone
PYTHONPATH=src python3 -m clustered_kv
```

출력은 아래였다.

```python
{'key': 'alpha', 'value': '1', 'found': True, 'shard_id': 'shard-b'}
```

이 출력은 두 가지를 보여 준다.

- key `alpha`는 현재 topology에서 `shard-b`로 라우팅된다.
- HTTP `GET /kv/{key}`는 `cluster.read()`를 사용하므로 leader 기준 read다.

문제 정의에는 follower read도 가능해야 한다고 적혀 있지만, public HTTP surface에는 follower 선택 파라미터가 없다. follower read는 현재 `read_from_node()`라는 내부 메서드로만 노출된다.

## 5. 정적 topology의 모양도 다시 확인했다

`new_cluster()`와 demo는 둘 다 같은 정적 group을 쓴다.

- `shard-a`: leader `node-1`, follower `node-2`
- `shard-b`: leader `node-2`, follower `node-3`

이 정적 구성 덕분에 capstone은 membership change 없이도, "라우팅 결과에 따라 어느 leader store에 쓰이고 어느 follower가 따라잡아야 하는가"를 끝까지 보여 줄 수 있다.
