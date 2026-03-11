# DDIA Distributed Systems Track

Go 분산 트랙은 RPC부터 replication, sharding, Raft-lite, clustered KV capstone을 거친 뒤, quorum consistency, leader election, failure-injected replication까지 확장되는 심화 경로입니다.

## 읽기 전에 알면 좋은 것

- 기본 네트워크와 분산 시스템 용어를 알고 있으면 좋습니다.
- 05 capstone 전까지는 transport, replication, routing, storage 연결을 먼저 잡습니다.
- 06 이후에는 consistency, authority, partial failure를 별도 질문으로 분해해 읽으면 좋습니다.

## 추천 순서

| 순서 | 프로젝트 | 이 단계에서 보는 질문 | 다음 단계 |
| --- | --- | --- | --- |
| 1 | [`01-rpc-framing`](01-rpc-framing/README.md) | TCP stream 위에서 request/response 경계를 복구하는 첫 분산 단계 | 02 Leader-Follower Replication |
| 2 | [`02-leader-follower-replication`](02-leader-follower-replication/README.md) | replication log와 follower catch-up을 배우는 단계 | 03 Shard Routing |
| 3 | [`03-shard-routing`](03-shard-routing/README.md) | consistent hashing과 rebalance 비용을 배우는 단계 | 04 Raft Lite |
| 4 | [`04-raft-lite`](04-raft-lite/README.md) | consensus의 핵심 안전 규칙을 보는 Go 심화 단계 | 05 Clustered KV Capstone |
| 5 | [`05-clustered-kv-capstone`](05-clustered-kv-capstone/README.md) | 지금까지 배운 저장 엔진·분산 개념을 하나로 묶는 캡스톤 | 06 Quorum and Consistency |
| 6 | [`06-quorum-and-consistency`](06-quorum-and-consistency/README.md) | 어떤 quorum 조합이 최신 읽기를 보장하고 stale read를 허용하는가 | 07 Heartbeat and Leader Election |
| 7 | [`07-heartbeat-and-leader-election`](07-heartbeat-and-leader-election/README.md) | 누가 authority를 가지며 split-brain을 어떻게 막는가 | 08 Failure-Injected Log Replication |
| 8 | [`08-failure-injected-log-replication`](08-failure-injected-log-replication/README.md) | partial failure 뒤에도 append/ack replication이 어떻게 수렴하는가 | 관찰성·membership·snapshotting 확장 |

## 이 트랙을 끝내면 남는 것

- 각 프로젝트가 어떤 설계 질문을 던지는지 한 번의 경로로 따라갈 수 있습니다.
- 각 README 마지막 섹션을 통해 공개용 포트폴리오로 확장할 수 있는 방향을 바로 확인할 수 있습니다.

## 다음 단계

분산 트랙을 끝내면 membership change, snapshotting, observability, benchmark/failure drill 프로젝트로 이어 가기 좋습니다.
