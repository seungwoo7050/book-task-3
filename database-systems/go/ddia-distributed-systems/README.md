# DDIA Distributed Systems Track

Go 분산 시스템 심화 트랙입니다. RPC부터 replication, sharding, Raft-lite, quorum, leader election, failure injection까지 이어집니다.

## 누가 여기서 시작해야 하는가

- Python 분산 트랙을 끝낸 뒤 consensus-lite, quorum, failure handling까지 더 깊게 보고 싶은 사람에게 맞습니다.
- transport, routing, authority, consistency를 별도 실험 단위로 나눠 추적하고 싶은 사람에게 맞습니다.
- 각 행의 `문제`, `내 해법`, `검증`은 [전역 카탈로그](../../docs/catalog/project-catalog.md)와 같은 문구를 사용합니다.

## 이 트랙이 답하는 질문

- 분산 저장소는 transport, replication, routing, consensus, consistency를 어떤 경계로 나눠 이해해야 하는가
- partial failure와 authority 교체를 어떤 실험 단위로 검증할 수 있는가

## 프로젝트 표

| 프로젝트 | 문제 | 내 해법 | 검증 | 다음 단계 |
| --- | --- | --- | --- | --- |
| [01 RPC Framing](projects/01-rpc-framing/README.md) | 4-byte big-endian length prefix framing을 구현해야 합니다. | TCP stream에서 message boundary를 복구하는 방법을 익힙니다. | `go test ./...`<br>`go run ./cmd/rpc-framing` | Leader-Follower Replication |
| [02 Leader-Follower Replication](projects/02-leader-follower-replication/README.md) | 순차 offset을 갖는 mutation log를 유지해야 합니다. | leader가 local state와 append-only log를 어떻게 함께 유지하는지 익힙니다. | `go test ./...`<br>`go run ./cmd/replication` | Shard Routing |
| [03 Shard Routing](projects/03-shard-routing/README.md) | deterministic consistent hash ring을 구현해야 합니다. | consistent hash ring이 key를 물리 node에 매핑하는 방식을 익힙니다. | `go test ./...`<br>`go run ./cmd/shard-routing` | Raft Lite |
| [04 Raft Lite](projects/04-raft-lite/README.md) | leader election과 단일 leader 보장을 재현해야 합니다. | term과 election cycle이 leader 교체를 어떻게 제어하는지 익힙니다. | `go test ./...`<br>`go run ./cmd/raft-lite` | Clustered KV Capstone |
| [05 Clustered KV Capstone](projects/05-clustered-kv-capstone/README.md) | key를 shard로 라우팅하고 shard별 leader/follower group을 선택해야 합니다. | router, leader, follower, local store가 한 write pipeline 안에서 어떻게 연결되는지 익힙니다. | `go test ./...`<br>`go run ./cmd/clustered-kv` | Quorum and Consistency |
| [06 Quorum and Consistency](projects/06-quorum-and-consistency/README.md) | replica 3개를 가진 versioned register를 구현해야 합니다. | replica 일부가 뒤처져도 quorum read가 최신 버전을 고르는 조건을 익힙니다. | `go test ./...`<br>`go run ./cmd/quorum-demo` | Heartbeat and Leader Election |
| [07 Heartbeat and Leader Election](projects/07-heartbeat-and-leader-election/README.md) | leader가 주기적으로 heartbeat를 보내야 합니다. | heartbeat silence가 suspicion으로 바뀌고, 그 다음 election으로 이어지는 흐름을 익힙니다. | `go test ./...`<br>`go run ./cmd/leader-election` | Failure-Injected Log Replication |
| [08 Failure-Injected Log Replication](projects/08-failure-injected-log-replication/README.md) | single leader가 append-only log를 가지고 follower에게 entry를 보낼 수 있어야 합니다. | dropped append가 retry로 수렴하는 흐름을 익힙니다. | `go test ./...`<br>`go run ./cmd/failure-replication` | 자체 확장 프로젝트 |

## 다음 단계

- 각 프로젝트는 `README -> problem/README -> docs/README -> 구현 -> tests -> notion/README` 순서로 읽습니다.
- 이 트랙 뒤에는 membership change, snapshotting, observability, benchmark/failure drill 프로젝트를 붙이기 좋습니다.
