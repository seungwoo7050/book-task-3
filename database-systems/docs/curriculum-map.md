# Curriculum Map

| Legacy source | Go destination | Python destination | Action | Reason |
| --- | --- | --- | --- | --- |
| `legacy/storage-engine/lsm-tree-core` | `go/database-internals/01-memtable-skiplist` | folded into `python/database-internals/01-mini-lsm-store` | split/fold | Go는 세분화, Python은 입문 난이도 조절을 위해 통합 |
| `legacy/storage-engine/lsm-tree-core` | `go/database-internals/02-sstable-format` | folded into `python/database-internals/01-mini-lsm-store` | split/fold | 같은 이유 |
| `legacy/storage-engine/lsm-tree-core` | `go/database-internals/03-mini-lsm-store` | `python/database-internals/01-mini-lsm-store` | keep/fold | Python 시작점을 self-contained하게 유지 |
| `legacy/storage-engine/wal-recovery` | `go/database-internals/04-wal-recovery` | `python/database-internals/02-wal-recovery` | keep | durability와 replay 주제가 자족적 |
| `legacy/storage-engine/compaction` | `go/database-internals/05-leveled-compaction` | none | keep | compaction은 Go 심화로 유지 |
| `legacy/storage-engine/index-filter` | `go/database-internals/06-index-filter` | `python/database-internals/03-index-filter` | keep | read-path 최적화 주제가 일관됨 |
| `legacy/transaction-engine/buffer-pool` | `go/database-internals/07-buffer-pool` | `python/database-internals/04-buffer-pool` | keep | page cache 주제가 백엔드 입문에 유효 |
| `legacy/transaction-engine/mvcc` | `go/database-internals/08-mvcc` | `python/database-internals/05-mvcc` | keep | snapshot isolation 주제가 자족적 |
| `legacy/distributed-cluster/rpc-network` | `go/ddia-distributed-systems/01-rpc-framing` | `python/ddia-distributed-systems/01-rpc-framing` | keep | framing과 request lifecycle이 분명함 |
| `legacy/distributed-cluster/replication` | `go/ddia-distributed-systems/02-leader-follower-replication` | `python/ddia-distributed-systems/02-leader-follower-replication` | keep | log shipping과 follower apply 의미가 분명함 |
| `legacy/distributed-cluster/sharding` | `go/ddia-distributed-systems/03-shard-routing` | `python/ddia-distributed-systems/03-shard-routing` | keep | consistent hashing 범위가 자족적 |
| `legacy/distributed-cluster/consensus` | `go/ddia-distributed-systems/04-raft-lite` | none | keep | 합의는 Go 심화로 유지 |
| none | `go/ddia-distributed-systems/05-clustered-kv-capstone` | `python/ddia-distributed-systems/04-clustered-kv-capstone` | add | 분산 모듈과 저장 엔진을 실제 흐름으로 연결하는 브리지 프로젝트 필요 |

## Shared Utilities

| Legacy source | Go destination | Action |
| --- | --- | --- |
| `legacy/common/serializer` | `go/shared/serializer` | re-implement |
| `legacy/common/hash` | `go/shared/hash` | re-implement |
| `legacy/common/file-io` | `go/shared/fileio` | re-implement |
