# 03 Shard Routing

virtual node를 가진 consistent hash ring으로 key를 node에 배치하고 rebalance 비용을 측정합니다.

## 이 프로젝트에서 배우는 것

- consistent hash ring이 key를 물리 node에 매핑하는 방식을 익힙니다.
- virtual node가 분산도와 hotspot 완화에 어떤 도움을 주는지 이해합니다.
- node 추가/제거 시 몇 개의 key가 이동하는지 계량하는 방법을 확인합니다.

## 먼저 알고 있으면 좋은 것

- 해시 함수와 기본 분산 개념을 알고 있으면 좋습니다.
- replication이나 routing이 여러 노드에 분산된다는 감각이 있으면 읽기 쉽습니다.

## 추천 읽기 순서

1. `problem/README.md`로 문제 해석과 현재 범위를 먼저 확인합니다.
2. `docs/README.md`와 개념 노트를 읽어, 코드에 들어가기 전 핵심 용어를 맞춥니다.
3. `src/`와 `tests/`를 함께 읽고, 마지막에 패키지 entry point를 실행해 전체 흐름을 확인합니다.
4. `notion/README.md`와 `notion/01-approach-log.md`로 설계 판단과 학습 메모를 확인합니다.

## 구현 표면

- `problem/`: 현재 프로젝트 문제 해석과 제공 자료
- `docs/`: 개념 메모와 설명형 참고자료 목록
- `src/shard_routing/`, `tests/`: 실제 구현과 검증 코드
- `notion/`: 현재 공개용 학습 노트
- `notion-archive/`: 이전 세대 문서 보관본

## 검증 명령

```bash
cd python/ddia-distributed-systems/03-shard-routing
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -U pytest
PYTHONPATH=src python -m pytest
PYTHONPATH=src python -m shard_routing
```

## 구현에서 집중할 포인트

- empty ring, single node, multi-node 상황에서 모두 deterministic routing이 되는지 확인합니다.
- node membership 변화 후 reassignment count가 기대 범위에 드는지 봅니다.
- virtual node 개수가 분산도에 어떤 영향을 주는지 테스트를 읽어 봅니다.

## 포트폴리오로 발전시키려면

- membership service, hotspot detector, shard movement visualizer를 추가하면 분산 시스템 포트폴리오로 확장하기 좋습니다.
- replication factor와 rack-awareness까지 고려하면 더 현실적인 router가 됩니다.
