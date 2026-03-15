# Evidence Ledger

## Primary sources

- [`problem/README.md`](/Users/woopinbell/work/book-task-3/database-systems/python/ddia-distributed-systems/projects/04-clustered-kv-capstone/problem/README.md)
- [`README.md`](/Users/woopinbell/work/book-task-3/database-systems/python/ddia-distributed-systems/projects/04-clustered-kv-capstone/README.md)
- [`docs/README.md`](/Users/woopinbell/work/book-task-3/database-systems/python/ddia-distributed-systems/projects/04-clustered-kv-capstone/docs/README.md)
- [`docs/concepts/static-topology.md`](/Users/woopinbell/work/book-task-3/database-systems/python/ddia-distributed-systems/projects/04-clustered-kv-capstone/docs/concepts/static-topology.md)
- [`docs/concepts/replicated-write-pipeline.md`](/Users/woopinbell/work/book-task-3/database-systems/python/ddia-distributed-systems/projects/04-clustered-kv-capstone/docs/concepts/replicated-write-pipeline.md)
- [`src/clustered_kv/core.py`](/Users/woopinbell/work/book-task-3/database-systems/python/ddia-distributed-systems/projects/04-clustered-kv-capstone/src/clustered_kv/core.py)
- [`src/clustered_kv/app.py`](/Users/woopinbell/work/book-task-3/database-systems/python/ddia-distributed-systems/projects/04-clustered-kv-capstone/src/clustered_kv/app.py)
- [`src/clustered_kv/__main__.py`](/Users/woopinbell/work/book-task-3/database-systems/python/ddia-distributed-systems/projects/04-clustered-kv-capstone/src/clustered_kv/__main__.py)
- [`tests/test_clustered_kv.py`](/Users/woopinbell/work/book-task-3/database-systems/python/ddia-distributed-systems/projects/04-clustered-kv-capstone/tests/test_clustered_kv.py)

## Re-run commands

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/python/ddia-distributed-systems/projects/04-clustered-kv-capstone
PYTHONPATH=src python3 -m pytest
PYTHONPATH=src python3 -m clustered_kv
PYTHONPATH=src python3 - <<'PY'
from tempfile import TemporaryDirectory
from clustered_kv import Cluster, ReplicaGroup
with TemporaryDirectory(prefix='clustered-kv-check-') as temp_dir:
    cluster = Cluster(
        temp_dir,
        [ReplicaGroup('shard-a', 'node-1', ['node-2']), ReplicaGroup('shard-b', 'node-2', ['node-3'])],
        64,
    )
    alpha_shard = cluster.put('alpha', '1')
    print('alpha_shard', alpha_shard, cluster.read('alpha'))
    cluster.set_auto_replicate(False)
    beta_shard = cluster.put('beta', '2')
    beta_group = cluster.group(beta_shard)
    print('beta_before_sync', cluster.read_from_node(beta_group.followers[0], 'beta'))
    print('beta_sync_applied', cluster.sync_follower(beta_shard, beta_group.followers[0]))
    print('beta_after_sync', cluster.read_from_node(beta_group.followers[0], 'beta'))
    cluster.delete('beta')
    print('beta_leader_after_delete', cluster.read('beta'))
    cluster.restart_node(beta_group.followers[0])
    print('beta_follower_after_restart', cluster.read_from_node(beta_group.followers[0], 'beta'))
PY
```

## Observed outputs

- `pytest`: `4 passed, 1 warning in 0.23s`
- demo: `{'key': 'alpha', 'value': '1', 'found': True, 'shard_id': 'shard-b'}`
- extra snippet:
  - `alpha_shard shard-b ('1', True, 'shard-b')`
  - `beta_before_sync ('', False)`
  - `beta_sync_applied 1`
  - `beta_after_sync ('2', True)`
  - `beta_leader_after_delete ('', False, 'shard-b')`
  - `beta_follower_after_restart ('2', True)`

## Source-grounded claims

- `DiskStore.apply()` appends JSON lines before mutating in-memory state.
- follower apply skips duplicate offsets and rejects non-sequential gaps.
- `Cluster.put()` and `Cluster.delete()` only sync followers when `auto_replicate` is enabled.
- public FastAPI read path always uses `Cluster.read()`, which reads from the shard leader.
- stale follower visibility is proven only in the extra Python snippet via `read_from_node()`, not by the public FastAPI round trip.

## Explicit boundaries

- No dynamic membership or leader election
- No network transport or retry model
- No HTTP follower-read selector
- No repair path that reconciles stale followers on restart
