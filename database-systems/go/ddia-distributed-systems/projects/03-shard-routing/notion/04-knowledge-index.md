# 지식 인덱스

## 핵심 용어
- `consistent hashing`: 노드 변경 시 전체 key 재배치를 줄이기 위한 해시 기반 routing 방식입니다.
- `virtual node`: 한 실제 노드를 ring 위의 여러 점으로 표현해 분산을 고르게 만드는 기법입니다.
- `rebalance`: 노드 집합이 바뀐 뒤 key 소유권이 다시 배치되는 과정입니다.
- `ownership`: 특정 key를 어느 node가 담당하는지에 대한 관계입니다.
- `batch routing`: 여러 key의 대상 node를 한 번에 계산하는 helper입니다.

## 다시 볼 파일
- `../internal/routing/routing.go`: consistent hash ring, virtual node 생성, routing 계산이 모두 들어 있습니다. 이 구현은 MurmurHash3 기반 hash를 사용합니다.
- `../tests/routing_test.go`: empty/single node, distribution, rebalance, batch routing을 검증합니다.
- `../cmd/shard-routing/main.go`: 몇 개의 sample key가 어느 node로 가는지 빠르게 보여 주는 데모입니다.
- `../docs/concepts/virtual-nodes.md`: virtual node가 왜 필요한지 요약한 개념 문서입니다.

## 개념 문서
- `../docs/concepts/rebalance-accounting.md`: 노드 추가와 제거 후 실제로 얼마나 키가 이동하는지 계산하는 관점을 정리합니다.
- `../docs/concepts/virtual-nodes.md`: virtual node를 써서 분산을 고르게 만드는 이유를 설명합니다.

## 검증 앵커
- 확인일: 2026-03-11
- 테스트 파일: `../tests/routing_test.go`
- 다시 돌릴 테스트 이름: `TestEmptyAndSingleNodeRouting`, `TestDistributionAndRebalance`, `TestBatchRouting`
- 데모 경로: `../cmd/shard-routing/main.go`
- 데모가 보여 주는 장면: 몇 개의 sample key가 어느 node로 가는지 출력합니다.

- 더 긴 이전 기록은 `../notion-archive/`에 남겨 두고, 여기에는 다시 읽을 때 바로 쓸 정보만 남깁니다.
