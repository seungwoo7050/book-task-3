# DDIA Distributed Systems

아래 표는 각 독립 프로젝트를 기존 초안과 분리한 뒤 source-first로 다시 쓴 시리즈 입구다.

| 프로젝트 | 시리즈 맵 | 재검증 신호 |
| --- | --- | --- |
| 01 RPC Framing | [00-series-map.md](01-rpc-framing/00-series-map.md) | `go test ok, 5 tests`, demo `pong:hello` |
| 02 Leader-Follower Replication | [00-series-map.md](02-leader-follower-replication/00-series-map.md) | `go test ok, 3 tests`, demo `beta=2 watermark=2` |
| 03 Shard Routing | [00-series-map.md](03-shard-routing/00-series-map.md) | `go test ok, 3 tests`, demo `gamma -> node-b` |
| 04 Raft Lite | [00-series-map.md](04-raft-lite/00-series-map.md) | `go test ok, 4 tests`, demo `leader=n1 commit=0 log_len=1` |
| 05 Clustered KV Capstone | [00-series-map.md](05-clustered-kv-capstone/00-series-map.md) | `go test ok, 3 tests`, demo `key=alpha shard=shard-a follower=node-2 value=1 ok=true` |
| 06 Quorum and Consistency | [00-series-map.md](06-quorum-and-consistency/00-series-map.md) | `go test ok, 4 tests`, demo `N=3 W=1 R=1 selected=v1:v1 responders=[replica-3=v1:v1]` |
| 07 Heartbeat and Leader Election | [00-series-map.md](07-heartbeat-and-leader-election/00-series-map.md) | `go test ok, 4 tests`, demo `recovered=node-1 state=follower term=2` |
| 08 Failure-Injected Log Replication | [00-series-map.md](08-failure-injected-log-replication/00-series-map.md) | `go test ok, 3 tests`, demo `recover tick commit=2 node-2=2 node-3=2` |
