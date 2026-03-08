# Legacy To Study Map

| Legacy source | Study destination | Action | Reason |
| --- | --- | --- | --- |
| `legacy/storage-engine/lsm-tree-core` | `study/database-internals/01-memtable-skiplist` | split | MemTable 자료구조를 독립 학습 단위로 분리 |
| `legacy/storage-engine/lsm-tree-core` | `study/database-internals/02-sstable-format` | split | 저장 형식과 footer parsing을 별도 프로젝트로 분리 |
| `legacy/storage-engine/lsm-tree-core` | `study/database-internals/03-mini-lsm-store` | split | flush lifecycle과 read path orchestration을 별도 프로젝트로 분리 |
| `legacy/storage-engine/wal-recovery` | `study/database-internals/04-wal-recovery` | keep | durability와 crash recovery 범위가 자족적 |
| `legacy/storage-engine/compaction` | `study/database-internals/05-leveled-compaction` | keep | level manager와 merge 정책이 명확한 독립 주제 |
| `legacy/storage-engine/index-filter` | `study/database-internals/06-index-filter` | keep | Bloom Filter와 Sparse Index의 결합 주제가 일관됨 |
| `legacy/transaction-engine/buffer-pool` | `study/database-internals/07-buffer-pool` | keep | page cache와 eviction 정책이 독립 학습 슬롯으로 적절 |
| `legacy/transaction-engine/mvcc` | `study/database-internals/08-mvcc` | keep | snapshot isolation과 conflict detection이 명확함 |
| `legacy/distributed-cluster/rpc-network` | `study/ddia-distributed-systems/01-rpc-framing` | keep | transport framing과 request/response lifecycle에 집중 |
| `legacy/distributed-cluster/replication` | `study/ddia-distributed-systems/02-leader-follower-replication` | keep | log shipping과 follower apply semantics가 분명함 |
| `legacy/distributed-cluster/sharding` | `study/ddia-distributed-systems/03-shard-routing` | keep | consistent hashing과 key routing 범위가 자족적 |
| `legacy/distributed-cluster/consensus` | `study/ddia-distributed-systems/04-raft-lite` | keep | synchronous Raft simulation 범위가 자족적 |
| none | `study/ddia-distributed-systems/05-clustered-kv-capstone` | add | 분산 모듈과 저장 엔진을 실제 흐름으로 연결하는 브리지 프로젝트 필요 |

## Shared Utilities

| Legacy source | Study destination | Action |
| --- | --- | --- |
| `legacy/common/serializer` | `study/shared/go/serializer` | re-implement |
| `legacy/common/hash` | `study/shared/go/hash` | re-implement |
| `legacy/common/file-io` | `study/shared/go/fileio` | re-implement |

