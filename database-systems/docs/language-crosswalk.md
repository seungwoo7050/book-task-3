# Language Crosswalk

| Python project | Go equivalent | Main reference | Notes |
| --- | --- | --- | --- |
| `python/database-internals/01-mini-lsm-store` | `go/database-internals/01-memtable-skiplist`, `02-sstable-format`, `03-mini-lsm-store` | `Database Internals` | Python 입문을 위해 memtable/SSTable prerequisite를 접음 |
| `python/database-internals/02-wal-recovery` | `go/database-internals/04-wal-recovery` | `Database Internals` | 같은 개념 범위 |
| `python/database-internals/03-index-filter` | `go/database-internals/06-index-filter` | `Database Internals` | 같은 개념 범위 |
| `python/database-internals/04-buffer-pool` | `go/database-internals/07-buffer-pool` | `Database Internals` | 같은 개념 범위 |
| `python/database-internals/05-mvcc` | `go/database-internals/08-mvcc` | `Database Internals` | 같은 개념 범위 |
| `python/ddia-distributed-systems/01-rpc-framing` | `go/ddia-distributed-systems/01-rpc-framing` | `DDIA` | 같은 개념 범위 |
| `python/ddia-distributed-systems/02-leader-follower-replication` | `go/ddia-distributed-systems/02-leader-follower-replication` | `DDIA` | 같은 개념 범위 |
| `python/ddia-distributed-systems/03-shard-routing` | `go/ddia-distributed-systems/03-shard-routing` | `DDIA` | 같은 개념 범위 |
| `python/ddia-distributed-systems/04-clustered-kv-capstone` | `go/ddia-distributed-systems/05-clustered-kv-capstone` | `DDIA`, `Database Internals` | Python은 static topology + synchronous replication만 포함 |
