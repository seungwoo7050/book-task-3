# DDIA Distributed Systems Track

Python 분산 시스템 입문 트랙입니다. RPC, replication, sharding, clustered KV capstone까지를 self-contained하게 따라갑니다.

## 누가 여기서 시작해야 하는가

- 분산 시스템을 처음 공부하며 request 흐름, replication, routing, clustered KV를 먼저 한 바퀴 돌고 싶은 사람에게 맞습니다.
- consensus 이전의 골격을 self-contained 프로젝트로 먼저 고정하고 싶은 사람에게 맞습니다.
- 각 행의 `문제`, `내 해법`, `검증`은 [전역 카탈로그](../../docs/catalog/project-catalog.md)와 같은 문구를 사용합니다.

## 이 트랙이 답하는 질문

- 분산 시스템 입문에서 request 흐름, replication, routing을 어떤 순서로 연결해 볼 것인가
- consensus 이전에 clustered KV까지 어떤 골격을 먼저 고정해야 하는가
- source-first 관점에서 각 프로젝트의 wire contract와 write pipeline을 어떻게 다시 읽을 것인가

## 프로젝트 표

| 프로젝트 | 문제 | 내 해법 | 검증 | 다음 단계 |
| --- | --- | --- | --- | --- |
| [01 RPC Framing](projects/01-rpc-framing/README.md) | 4-byte big-endian length prefix framing을 구현해야 합니다. | TCP stream에서 message boundary를 복구하는 방법을 익힙니다. | `PYTHONPATH=src python -m pytest`<br>`PYTHONPATH=src python -m rpc_framing` | Leader-Follower Replication |
| [02 Leader-Follower Replication](projects/02-leader-follower-replication/README.md) | 순차 offset을 갖는 mutation log를 유지해야 합니다. | leader가 local state와 append-only log를 어떻게 함께 유지하는지 익힙니다. | `PYTHONPATH=src python -m pytest`<br>`PYTHONPATH=src python -m leader_follower` | Shard Routing |
| [03 Shard Routing](projects/03-shard-routing/README.md) | deterministic consistent hash ring을 구현해야 합니다. | consistent hash ring이 key를 물리 node에 매핑하는 방식을 익힙니다. | `PYTHONPATH=src python -m pytest`<br>`PYTHONPATH=src python -m shard_routing` | Clustered KV Capstone |
| [04 Clustered KV Capstone](projects/04-clustered-kv-capstone/README.md) | key를 shard로 라우팅하고 shard별 leader/follower group을 선택해야 합니다. | router, leader, follower, local store가 한 write pipeline 안에서 어떻게 연결되는지 익힙니다. | `python -m pip install -e '.[dev]'`<br>`PYTHONPATH=src python -m pytest && python -m clustered_kv` | Go 심화 슬롯 |

## 다음 단계

- 각 프로젝트는 `README -> problem/README -> docs/README -> 구현 -> tests -> notion/README` 순서로 읽습니다.
- source-first chronology로 다시 읽고 싶다면 [../../blog/python/ddia-distributed-systems/README.md](../../blog/python/ddia-distributed-systems/README.md)에서 각 프로젝트의 `00-series-map.md`로 이동합니다.
- 이 트랙을 끝낸 뒤 [Go 분산 트랙](../../go/ddia-distributed-systems/README.md)의 Raft-lite, quorum, election, failure handling 슬롯으로 넘어가면 authority와 consistency를 더 깊게 읽을 수 있습니다.
