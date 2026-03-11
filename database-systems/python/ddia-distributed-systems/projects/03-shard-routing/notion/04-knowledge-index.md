# 지식 인덱스

## 핵심 용어
- `consistent hashing`: 노드 변경 시 전체 key 재배치를 줄이기 위한 해시 기반 routing 방식입니다.
- `virtual node`: 한 실제 노드를 ring 위의 여러 점으로 표현해 분산을 고르게 만드는 기법입니다.
- `rebalance`: 노드 집합이 바뀐 뒤 key 소유권이 다시 배치되는 과정입니다.
- `ownership`: 특정 key를 어느 node가 담당하는지에 대한 관계입니다.
- `batch routing`: 여러 key의 대상 node를 한 번에 계산하는 helper입니다.

## 다시 볼 파일
- `../src/shard_routing/core.py`: ring 생성, ownership 계산, rebalance accounting이 한 파일 안에서 이어집니다.
- `../src/shard_routing/__main__.py`: `k1`~`k4` batch routing 결과를 바로 보여 주는 데모 진입점입니다.
- `../tests/test_shard_routing.py`: empty/single node, distribution, rebalance, batch routing을 검증합니다.
- `../docs/concepts/virtual-nodes.md`: virtual node가 왜 필요한지 먼저 복기할 때 좋습니다.

## 개념 문서
- `../docs/concepts/rebalance-accounting.md`: 노드 추가와 제거 후 실제로 얼마나 키가 이동하는지 계산하는 관점을 정리합니다.
- `../docs/concepts/virtual-nodes.md`: virtual node를 써서 분산을 고르게 만드는 이유를 설명합니다.

## 검증 앵커
- 확인일: 2026-03-11
- 테스트 파일: `../tests/test_shard_routing.py`
- 다시 돌릴 테스트 이름: `test_empty_and_single_node_routing`, `test_distribution_and_rebalance`, `test_batch_routing`
- 데모 경로: `../src/shard_routing/__main__.py`
- 데모가 보여 주는 장면: `k1`~`k4` batch routing 결과를 그대로 출력합니다.
- 더 긴 이전 기록은 `../notion-archive/`에 남겨 두고, 여기에는 다시 읽을 때 바로 필요한 정보만 남깁니다.
