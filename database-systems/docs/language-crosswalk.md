# Language Crosswalk

Python 트랙은 빠른 진입을 위한 입문 경로이고, Go 트랙은 세분화된 정본 경로입니다. 아래 표는 Python 프로젝트를 읽다가 “Go에서는 이 주제가 어디로 더 자세히 나뉘는가?”를 바로 찾도록 돕습니다.

| Python 프로젝트 | 대응하는 Go 프로젝트 | 주 참조 주제 | 읽는 팁 |
| --- | --- | --- | --- |
| `python/database-internals/01-mini-lsm-store` | `go/database-internals/01-memtable-skiplist`, `02-sstable-format`, `03-mini-lsm-store` | `Database Internals` | Python으로 큰 흐름을 잡은 뒤 Go 세 프로젝트로 내려가면 자료구조·포맷·오케스트레이션이 분리되어 보입니다. |
| `python/database-internals/02-wal-recovery` | `go/database-internals/04-wal-recovery` | `Database Internals` | durability 흐름은 거의 같은 개념 범위입니다. |
| `python/database-internals/03-index-filter` | `go/database-internals/06-index-filter` | `Database Internals` | Bloom filter와 sparse index를 비교하며 읽기 좋습니다. |
| `python/database-internals/04-buffer-pool` | `go/database-internals/07-buffer-pool` | `Database Internals` | page cache 개념은 동일하고 구현 표면만 다릅니다. |
| `python/database-internals/05-mvcc` | `go/database-internals/08-mvcc` | `Database Internals` | transaction visibility 규칙을 언어별로 비교하기 좋습니다. |
| `python/ddia-distributed-systems/01-rpc-framing` | `go/ddia-distributed-systems/01-rpc-framing` | `DDIA` | framing과 pending map 개념은 거의 1:1입니다. |
| `python/ddia-distributed-systems/02-leader-follower-replication` | `go/ddia-distributed-systems/02-leader-follower-replication` | `DDIA` | replication log와 follower catch-up을 같은 질문으로 비교하면 됩니다. |
| `python/ddia-distributed-systems/03-shard-routing` | `go/ddia-distributed-systems/03-shard-routing` | `DDIA` | consistent hashing과 reassignment accounting을 언어별로 비교할 수 있습니다. |
| `python/ddia-distributed-systems/04-clustered-kv-capstone` | `go/ddia-distributed-systems/05-clustered-kv-capstone` | `DDIA` + `Database Internals` | Python은 static topology + FastAPI boundary, Go는 더 넓은 심화 경로로 이어집니다. |
