# 학습 노트 안내

replication 전에 먼저 “이 key는 어느 노드가 맡는가”를 설명하기 위해 consistent hashing 기반 shard routing을 분리한 단계입니다.

## 이 노트를 읽기 전에 잡을 질문
- 노드가 추가되거나 제거되어도 전체 key 재배치를 최소화하려면 routing 계층은 어떤 ring 구조를 가져야 하는가?
- 다음 단계 `04 Clustered KV Capstone`에 무엇을 넘기는가?

## 권장 읽기 순서
1. `../problem/README.md`로 요구와 범위를 먼저 확인합니다.
2. `../src/shard_routing/core.py`, `../tests/test_shard_routing.py`, `../src/shard_routing/__main__.py`를 열어 실제 구현 표면을 먼저 잡습니다.
3. `../tests/`에서 이 프로젝트가 무엇을 보장하는지 확인합니다. 핵심 테스트는 `test_empty_and_single_node_routing`, `test_distribution_and_rebalance`, `test_batch_routing`입니다.
4. 데모 경로 `../src/shard_routing/__main__.py`를 실행해 전체 흐름을 빠르게 눈으로 확인합니다.
5. 마지막으로 `./00-problem-framing.md`부터 `./04-knowledge-index.md`까지 읽으며 판단과 연결 지점을 정리합니다.

## 이번 노트가 담는 것
- `00-problem-framing.md`: 노드가 추가되거나 제거되어도 전체 key 재배치를 최소화하려면 routing 계층은 어떤 ring 구조를 가져야 하는가?에 대한 범위와 성공 기준을 정리합니다.
- `01-approach-log.md`: consistent hash ring을 routing 계층으로 독립시킨다, virtual node를 적극적으로 사용한다 같은 실제 구현 선택을 기록합니다.
- `02-debug-log.md`: 빈 ring이나 단일 노드 경계 조건이 깨지는 경우, virtual node 분포가 치우치는 경우처럼 다시 깨질 수 있는 지점을 모아 둡니다.
- `03-retrospective.md`: 이 단계에서 얻은 것, 남긴 단순화, 다음 확장 방향을 정리합니다.
- `04-knowledge-index.md`: 용어, 핵심 파일, 개념 문서, 검증 앵커를 빠르게 다시 찾는 인덱스입니다.

## 검증 앵커
- 테스트: `test_empty_and_single_node_routing`, `test_distribution_and_rebalance`, `test_batch_routing`
- 데모 경로: `../src/shard_routing/__main__.py`
- 데모가 보여 주는 장면: Go 데모는 `alpha`, `beta`, `gamma`가 어느 node로 가는지 출력합니다. Python 데모는 `k1`~`k4` batch routing 결과를 그대로 print합니다.
- 개념 문서: `../docs/concepts/rebalance-accounting.md`, `../docs/concepts/virtual-nodes.md`

- 이전 장문 기록은 `../notion-archive/`에 보존돼 있습니다.
