# Evidence Ledger

## Primary sources

- [`problem/README.md`](/Users/woopinbell/work/book-task-3/database-systems/python/ddia-distributed-systems/projects/03-shard-routing/problem/README.md)
- [`README.md`](/Users/woopinbell/work/book-task-3/database-systems/python/ddia-distributed-systems/projects/03-shard-routing/README.md)
- [`docs/README.md`](/Users/woopinbell/work/book-task-3/database-systems/python/ddia-distributed-systems/projects/03-shard-routing/docs/README.md)
- [`docs/concepts/virtual-nodes.md`](/Users/woopinbell/work/book-task-3/database-systems/python/ddia-distributed-systems/projects/03-shard-routing/docs/concepts/virtual-nodes.md)
- [`docs/concepts/rebalance-accounting.md`](/Users/woopinbell/work/book-task-3/database-systems/python/ddia-distributed-systems/projects/03-shard-routing/docs/concepts/rebalance-accounting.md)
- [`src/shard_routing/core.py`](/Users/woopinbell/work/book-task-3/database-systems/python/ddia-distributed-systems/projects/03-shard-routing/src/shard_routing/core.py)
- [`src/shard_routing/__main__.py`](/Users/woopinbell/work/book-task-3/database-systems/python/ddia-distributed-systems/projects/03-shard-routing/src/shard_routing/__main__.py)
- [`tests/test_shard_routing.py`](/Users/woopinbell/work/book-task-3/database-systems/python/ddia-distributed-systems/projects/03-shard-routing/tests/test_shard_routing.py)

## Re-run commands

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/python/ddia-distributed-systems/projects/03-shard-routing
PYTHONPATH=src python3 -m pytest
PYTHONPATH=src python3 -m shard_routing
PYTHONPATH=src python3 - <<'PY'
from shard_routing import Ring, Router
ring = Ring(150)
print('empty', ring.node_for_key('key-0'))
ring.add_node('node-a'); ring.add_node('node-b'); ring.add_node('node-c')
keys = [f'key-{i}' for i in range(3000)]
counts = {node: 0 for node in ring.nodes()}
for key in keys:
    node, _ = ring.node_for_key(key)
    counts[node] += 1
print('distribution', counts)
before = ring.assignments(keys[:1000])
ring.add_node('node-d')
print('moved_after_add', ring.moved_keys(keys[:1000], before))
router = Router(ring)
print('batch', router.route_batch(['k1', 'k2', 'k3', 'k4', 'k5']))
ring.remove_node('node-b')
print('nodes_after_remove', ring.nodes())
print('sample_after_remove', {k: ring.node_for_key(k)[0] for k in ['key-0', 'key-1', 'key-2']})
PY
```

## Observed outputs

- `pytest`: `3 passed, 1 warning in 0.06s`
- demo: `{'node-a': ['k1', 'k3', 'k4'], 'node-b': ['k2']}`
- extra snippet:
  - `empty ('', False)`
  - `distribution {'node-a': 1010, 'node-b': 889, 'node-c': 1101}`
  - `moved_after_add 237`
  - `batch {'node-d': ['k1', 'k3', 'k4'], 'node-b': ['k2', 'k5']}`
  - `nodes_after_remove ['node-a', 'node-c', 'node-d']`

## Source-grounded claims

- hash input is SHA-256 first 8 bytes, not Python runtime hash.
- ring lookup uses `bisect_left` and wrap-around to index `0`.
- duplicate add/remove is idempotent through `_nodes` set plus `discard()`, but this is source-grounded rather than explicitly pinned by the canonical pytest cases.
- moved key count is computed by diffing previous and current assignment maps.

## Explicit boundaries

- No membership epoch or gossip
- No actual data movement executor
- No replica placement or rack awareness
- No hotspot-aware routing
- Distribution evidence is sample-based (`3000` keys, loose `0.2 < share < 0.5` bounds), not a formal balance proof.
