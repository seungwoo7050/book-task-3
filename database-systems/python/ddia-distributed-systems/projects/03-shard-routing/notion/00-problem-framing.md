# 문제 프레이밍

## 왜 이 프로젝트를 하는가
replication 전에 먼저 이 key는 어느 노드가 맡는가를 설명하기 위해 consistent hashing 기반 shard routing을 분리한 단계입니다.

## 커리큘럼 안에서의 위치
- 트랙: DDIA Distributed Systems / Python
- 이전 단계: 02 Leader-Follower Replication
- 다음 단계: 04 Clustered KV Capstone
- 지금 답하려는 질문: 노드가 추가되거나 제거되어도 전체 key 재배치를 최소화하려면 routing 계층은 어떤 ring 구조를 가져야 하는가?

## 이번 구현에서 성공으로 보는 것
- 빈 ring과 single-node ring에서도 routing이 예측 가능해야 합니다.
- virtual node를 사용해 key 분포가 한쪽으로 치우치지 않아야 합니다.
- node 추가와 제거 후 이동하는 key 수를 대략적으로 확인할 수 있어야 합니다.
- batch routing이 여러 key의 대상 node를 한 번에 설명해 줄 수 있어야 합니다.
- routing 규칙이 replication 정책과 독립적으로 읽혀야 합니다.

## 먼저 열어 둘 파일
- `../src/shard_routing/core.py`: ring 생성, virtual node 배치, ownership 계산이 한 파일 안에서 어떻게 이어지는지 확인합니다.
- `../src/shard_routing/__main__.py`: `k1`~`k4` batch routing 결과를 가장 짧게 보여 주는 데모 진입점입니다.
- `../tests/test_shard_routing.py`: empty/single node, distribution, rebalance, batch routing이 어디서 깨지는지 바로 확인합니다.
- `../docs/concepts/virtual-nodes.md`: virtual node가 왜 필요한지 먼저 복기합니다.

## 의도적으로 남겨 둔 범위 밖 항목
- 동적 membership protocol이나 health check는 구현하지 않습니다.
- multi-replica placement와 hot-key mitigation도 아직 없습니다.

## 데모에서 바로 확인할 장면
- `k1`~`k4` batch routing 결과를 그대로 출력합니다.
