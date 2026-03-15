# Evidence Ledger

## Primary sources

- [`problem/README.md`](/Users/woopinbell/work/book-task-3/database-systems/python/ddia-distributed-systems/projects/02-leader-follower-replication/problem/README.md)
- [`README.md`](/Users/woopinbell/work/book-task-3/database-systems/python/ddia-distributed-systems/projects/02-leader-follower-replication/README.md)
- [`docs/README.md`](/Users/woopinbell/work/book-task-3/database-systems/python/ddia-distributed-systems/projects/02-leader-follower-replication/docs/README.md)
- [`docs/concepts/log-shipping.md`](/Users/woopinbell/work/book-task-3/database-systems/python/ddia-distributed-systems/projects/02-leader-follower-replication/docs/concepts/log-shipping.md)
- [`docs/concepts/idempotent-follower.md`](/Users/woopinbell/work/book-task-3/database-systems/python/ddia-distributed-systems/projects/02-leader-follower-replication/docs/concepts/idempotent-follower.md)
- [`src/leader_follower/core.py`](/Users/woopinbell/work/book-task-3/database-systems/python/ddia-distributed-systems/projects/02-leader-follower-replication/src/leader_follower/core.py)
- [`src/leader_follower/__main__.py`](/Users/woopinbell/work/book-task-3/database-systems/python/ddia-distributed-systems/projects/02-leader-follower-replication/src/leader_follower/__main__.py)
- [`tests/test_replication.py`](/Users/woopinbell/work/book-task-3/database-systems/python/ddia-distributed-systems/projects/02-leader-follower-replication/tests/test_replication.py)

## Re-run commands

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/python/ddia-distributed-systems/projects/02-leader-follower-replication
PYTHONPATH=src python3 -m pytest
PYTHONPATH=src python3 -m leader_follower
PYTHONPATH=src python3 - <<'PY'
from leader_follower.core import Leader, Follower, replicate_once, LogEntry
leader = Leader(); follower = Follower()
leader.put('a', '1'); leader.put('b', '2')
print('initial_apply', replicate_once(leader, follower), follower.watermark(), follower.store)
print('duplicate_apply', follower.apply(leader.log_from(0)), follower.watermark(), follower.store)
leader.delete('a'); leader.put('b', '3')
print('incremental_apply', replicate_once(leader, follower), follower.watermark(), follower.store)
manual = [LogEntry(1, 'put', 'b', '2'), LogEntry(2, 'delete', 'a', None), LogEntry(3, 'put', 'b', '3')]
print('replay_batch', follower.apply(manual), follower.watermark(), follower.store)
PY
```

## Observed outputs

- `pytest`: `3 passed, 1 warning in 0.02s`
- demo: `{'applied': 1, 'value': '1'}`
- incremental/idempotent snippet:
  - `initial_apply 2 1 {'a': '1', 'b': '2'}`
  - `duplicate_apply 0 1 {'a': '1', 'b': '2'}`
  - `incremental_apply 2 3 {'b': '3'}`
  - `replay_batch 0 3 {'b': '3'}`

## Source-grounded claims

- `ReplicationLog.append()` assigns offsets from `len(self.entries)`.
- `replicate_once()` fetches from `follower.watermark() + 1`.
- `Follower.apply()` enforces idempotency with `entry.offset <= self.last_applied_offset`.
- delete replication is encoded as `operation="delete", value=None`.

## Explicit boundaries

- No leader election or consensus
- No quorum acknowledgement
- No log truncation or snapshot install
- No durability layer beyond in-memory Python structures
