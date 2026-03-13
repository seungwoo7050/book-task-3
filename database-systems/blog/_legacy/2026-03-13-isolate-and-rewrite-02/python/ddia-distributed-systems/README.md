# DDIA Distributed Systems

아래 표는 각 독립 프로젝트를 기존 초안과 분리한 뒤 source-first로 다시 쓴 시리즈 입구다.

| 프로젝트 | 시리즈 맵 | 재검증 신호 |
| --- | --- | --- |
| 01 RPC Framing | [00-series-map.md](01-rpc-framing/00-series-map.md) | `5 passed`, demo `{'msg': 'hello'}` |
| 02 Leader-Follower Replication | [00-series-map.md](02-leader-follower-replication/00-series-map.md) | `3 passed`, demo `{'applied': 1, 'value': '1'}` |
| 03 Shard Routing | [00-series-map.md](03-shard-routing/00-series-map.md) | `3 passed`, demo `{'node-a': ['k1', 'k3', 'k4'], 'node-b': ['k2']}` |
| 04 Clustered KV Capstone | [00-series-map.md](04-clustered-kv-capstone/00-series-map.md) | `4 passed`, demo `{'key': 'alpha', 'value': '1', 'found': True, 'shard_id': 'shard-b'}` |
