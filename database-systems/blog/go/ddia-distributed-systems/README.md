# DDIA Distributed Systems

RPC framing에서 출발해 replication, shard routing, leader election, clustered KV까지 분산 경로를 순서대로 잇습니다.

## 처음 읽는다면

- 가볍게 시작하고 싶다면: [01 RPC Framing](01-rpc-framing/00-series-map.md)
- replication과 leader 흐름부터 보고 싶다면: [04 Raft Lite](04-raft-lite/00-series-map.md)
- capstone까지 바로 보고 싶다면: [05 Clustered KV Capstone](05-clustered-kv-capstone/00-series-map.md)

## 프로젝트 지도

| 프로젝트 | 한 줄 설명 | 재검증 신호 | 시리즈 |
| --- | --- | --- | --- |
| 01 RPC Framing | length-prefixed framing과 correlation id 기반 pending map으로 최소 RPC 계층을 구현합니다. | `go test ok, 5 tests`, demo `pong:hello` | [00-series-map.md](01-rpc-framing/00-series-map.md) |
| 02 Leader-Follower Replication | append-only mutation log와 watermark 기반 incremental sync로 leader-follower replication을 구현합니다. | `go test ok, 3 tests`, demo `beta=2 watermark=2` | [00-series-map.md](02-leader-follower-replication/00-series-map.md) |
| 03 Shard Routing | virtual node를 가진 consistent hash ring으로 key를 node에 배치하고 rebalance 비용을 측정합니다. | `go test ok, 3 tests`, demo `gamma -> node-b` | [00-series-map.md](03-shard-routing/00-series-map.md) |
| 04 Raft Lite | leader election, vote rule, AppendEntries consistency, majority commit이 드러나는 작은 동기 Raft 시뮬레이터를 구현합니다. | `go test ok, 4 tests`, demo `leader=n1 commit=0 log_len=1` | [00-series-map.md](04-raft-lite/00-series-map.md) |
| 05 Clustered KV Capstone | 정적 shard topology와 정적 leader 배치를 가진 작은 clustered KV store로 routing, replication, disk-backed storage를 한 흐름으로 연결합니다. | `go test ok, 3 tests`, demo `key=alpha shard=shard-a follower=node-2 value=1 ok=true` | [00-series-map.md](05-clustered-kv-capstone/00-series-map.md) |
| 06 Quorum and Consistency | quorum read/write와 versioned register를 이용해 `W + R > N`이 최신 읽기를 어떻게 보장하고, `W + R <= N`일 때 어떤 stale read가 생기는지 재현합니다. | `go test ok, 4 tests`, demo `N=3 W=1 R=1 selected=v1:v1 responders=[replica-3=v1:v1]` | [00-series-map.md](06-quorum-and-consistency/00-series-map.md) |
| 07 Heartbeat and Leader Election | heartbeat 기반 failure detector와 majority vote만으로 leader failover를 재현하는 작은 election lab을 구현합니다. | `go test ok, 4 tests`, demo `recovered=node-1 state=follower term=2` | [00-series-map.md](07-heartbeat-and-leader-election/00-series-map.md) |
| 08 Failure-Injected Log Replication | drop, duplicate, pause가 들어가는 작은 네트워크 하네스 위에서 append/ack 로그 복제와 quorum commit, follower catch-up을 재현합니다. | `go test ok, 3 tests`, demo `recover tick commit=2 node-2=2 node-3=2` | [00-series-map.md](08-failure-injected-log-replication/00-series-map.md) |
