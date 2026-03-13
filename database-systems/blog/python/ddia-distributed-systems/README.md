# DDIA Distributed Systems Blog Series

분산 시스템 입문 트랙을 "네트워크/복제/라우팅을 따로따로"가 아니라 "한 경계가 다음 경계를 어떻게 부르는가"라는 관점으로 정리한 인덱스다.

| 프로젝트 | 시리즈 입구 | 재검증 신호 |
| --- | --- | --- |
| 01 RPC Framing | [00-series-map.md](01-rpc-framing/00-series-map.md) | `5 passed`, demo `{'msg': 'hello'}` |
| 02 Leader-Follower Replication | [00-series-map.md](02-leader-follower-replication/00-series-map.md) | `3 passed`, demo `applied=1` |
| 03 Shard Routing | [00-series-map.md](03-shard-routing/00-series-map.md) | `3 passed`, demo batch routing |
| 04 Clustered KV Capstone | [00-series-map.md](04-clustered-kv-capstone/00-series-map.md) | `4 passed`, demo includes `shard_id` |

## 읽기 권장 순서

`01 -> 02 -> 03 -> 04`

framing으로 메시지 경계를 고정하고, log shipping을 붙이고, key-to-shard 라우팅을 붙인 다음, 마지막에 storage와 API boundary를 하나로 합친다.
