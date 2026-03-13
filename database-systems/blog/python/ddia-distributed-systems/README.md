# DDIA Distributed Systems

RPC framing에서 출발해 replication, shard routing, leader election, clustered KV까지 분산 경로를 순서대로 잇습니다.

## 처음 읽는다면

- 가볍게 시작하고 싶다면: [01 RPC Framing](01-rpc-framing/00-series-map.md)
- replication과 leader 흐름부터 보고 싶다면: [02 Leader-Follower Replication](02-leader-follower-replication/00-series-map.md)
- capstone까지 바로 보고 싶다면: [04 Clustered KV Capstone](04-clustered-kv-capstone/00-series-map.md)

## 프로젝트 지도

| 프로젝트 | 한 줄 설명 | 재검증 신호 | 시리즈 |
| --- | --- | --- | --- |
| 01 RPC Framing | length-prefixed framing과 correlation id 기반 pending map으로 최소 RPC 계층을 구현합니다. | `5 passed`, demo `{'msg': 'hello'}` | [00-series-map.md](01-rpc-framing/00-series-map.md) |
| 02 Leader-Follower Replication | append-only mutation log와 watermark 기반 incremental sync로 leader-follower replication을 구현합니다. | `3 passed`, demo `{'applied': 1, 'value': '1'}` | [00-series-map.md](02-leader-follower-replication/00-series-map.md) |
| 03 Shard Routing | virtual node를 가진 consistent hash ring으로 key를 node에 배치하고 rebalance 비용을 측정합니다. | `3 passed`, demo `{'node-a': ['k1', 'k3', 'k4'], 'node-b': ['k2']}` | [00-series-map.md](03-shard-routing/00-series-map.md) |
| 04 Clustered KV Capstone | 정적 shard topology와 정적 leader 배치를 가진 작은 clustered KV store로 routing, replication, disk-backed storage를 한 흐름으로 연결합니다. | `4 passed`, demo `{'key': 'alpha', 'value': '1', 'found': True, 'shard_id': 'shard-b'}` | [00-series-map.md](04-clustered-kv-capstone/00-series-map.md) |
