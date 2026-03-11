# DDIA Distributed Systems Track

Python 분산 트랙은 Raft를 제외하고, 분산 시스템의 핵심 흐름을 capstone까지 self-contained하게 보여 주는 입문 경로입니다.

## 읽기 전에 알면 좋은 것

- 분산 시스템을 처음 접하는 학습자에게 적합합니다.
- 입문 경로인 만큼 consensus보다 request 흐름과 topology 연결 이해를 우선합니다.

## 추천 순서

| 순서 | 프로젝트 | 이 단계에서 보는 질문 | 다음 단계 |
| --- | --- | --- | --- |
| 1 | [`01-rpc-framing`](01-rpc-framing/README.md) | TCP stream 위에서 request/response 경계를 복구하는 첫 분산 단계 | 02 Leader-Follower Replication |
| 2 | [`02-leader-follower-replication`](02-leader-follower-replication/README.md) | replication log와 follower catch-up을 배우는 단계 | 03 Shard Routing |
| 3 | [`03-shard-routing`](03-shard-routing/README.md) | consistent hashing과 rebalance 비용을 배우는 단계 | 04 Clustered KV Capstone |
| 4 | [`04-clustered-kv-capstone`](04-clustered-kv-capstone/README.md) | 지금까지 배운 저장 엔진·분산 개념을 하나로 묶는 캡스톤 | Go DDIA track의 04~08 심화 슬롯 또는 FastAPI 기반 확장판 |

## 이 트랙을 끝내면 남는 것

- 각 프로젝트가 어떤 설계 질문을 던지는지 한 번의 경로로 따라갈 수 있습니다.
- 각 README 마지막 섹션을 통해 공개용 포트폴리오로 확장할 수 있는 방향을 바로 확인할 수 있습니다.

## 다음 단계

이 트랙을 끝낸 뒤 Go 분산 트랙의 `04-raft-lite`, `06-quorum-and-consistency`, `07-heartbeat-and-leader-election`, `08-failure-injected-log-replication`으로 넘어가면 authority, consistency, partial failure를 더 세밀하게 읽을 수 있습니다.
