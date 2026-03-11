# Curriculum Map

| 역사적 학습 주제 | 현재 Go 목적지 | 현재 Python 목적지 | 현재 처리 방식 | 재구성 이유 |
| --- | --- | --- | --- | --- |
| LSM Tree Core | `01-memtable-skiplist`, `02-sstable-format`, `03-mini-lsm-store` | `01-mini-lsm-store` | Go는 분리, Python은 통합 | Go는 단계적 이해를, Python은 빠른 진입을 우선했습니다. |
| WAL Recovery | `04-wal-recovery` | `02-wal-recovery` | 유지 | durability와 replay는 독립 주제로 학습 가치가 높습니다. |
| Compaction | `05-leveled-compaction` | 해당 없음 | Go 심화 유지 | compaction은 입문 경로보다 심화 경로에 더 적합합니다. |
| Index and Filter Optimization | `06-index-filter` | `03-index-filter` | 유지 | read-path 최적화 주제가 양쪽 트랙에서 모두 유효합니다. |
| Buffer Pool | `07-buffer-pool` | `04-buffer-pool` | 유지 | page cache와 eviction 정책은 백엔드 학습자에게도 중요합니다. |
| MVCC | `08-mvcc` | `05-mvcc` | 유지 | snapshot visibility와 conflict 규칙은 저장 엔진 마지막 단계로 적합합니다. |
| RPC Network | `01-rpc-framing` | `01-rpc-framing` | 유지 | 분산 트랙의 공통 transport 감각을 먼저 잡습니다. |
| Replication | `02-leader-follower-replication` | `02-leader-follower-replication` | 유지 | log shipping과 follower apply 의미가 명확합니다. |
| Sharding | `03-shard-routing` | `03-shard-routing` | 유지 | consistent hashing과 rebalance 비용을 독립적으로 보기 좋습니다. |
| Consensus / Raft | `04-raft-lite` | 해당 없음 | Go 심화 유지 | 합의는 입문 경로보다 Go 심화 경로에 두는 편이 학습 부담이 적습니다. |
| 저장 엔진 + 분산 시스템 브리지 | `05-clustered-kv-capstone` | `04-clustered-kv-capstone` | 신규 추가 | routing, replication, local storage를 한 요청 흐름으로 묶는 단계가 필요했습니다. |
| Quorum and Consistency | `06-quorum-and-consistency` | 해당 없음 | Go 심화 신규 추가 | replication 다음 단계의 consistency trade-off를 별도 register 실험으로 분리해 설명하기 위해 |
| Heartbeat and Leader Election | `07-heartbeat-and-leader-election` | 해당 없음 | Go 심화 신규 추가 | failure detector와 authority 교체를 full consensus와 분리해 먼저 다루기 위해 |
| Failure-Injected Log Replication | `08-failure-injected-log-replication` | 해당 없음 | Go 심화 신규 추가 | retry, idempotency, quorum commit을 partial failure 장면으로 재현하기 위해 |

## 공용 유틸리티

| 영역 | 현재 위치 | 역할 |
| --- | --- | --- |
| serializer | `go/shared/serializer` | 단순 binary record encoding 보조 |
| hash | `go/shared/hash` | CRC32, MurmurHash3 같은 공용 해시 기능 |
| file I/O | `go/shared/fileio` | 원자적 쓰기와 파일 관리 보조 |
