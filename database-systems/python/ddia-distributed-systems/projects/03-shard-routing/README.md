# 03 Shard Routing

virtual node를 가진 consistent hash ring으로 key를 node에 배치하고 rebalance 비용을 측정합니다.

## 문제

- deterministic consistent hash ring을 구현해야 합니다.
- batch routing이 가능해야 합니다.
- add/remove 이후 reassignment count를 계산해야 합니다.
- empty ring, single node, multi-node 분산을 검증해야 합니다.

## 내 해법

- consistent hash ring이 key를 물리 node에 매핑하는 방식을 익힙니다.
- virtual node가 분산도와 hotspot 완화에 어떤 도움을 주는지 이해합니다.
- node 추가/제거 시 몇 개의 key가 이동하는지 계량하는 방법을 확인합니다.

## 검증

```bash
cd python/ddia-distributed-systems/projects/03-shard-routing
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -U pytest
PYTHONPATH=src python -m pytest
PYTHONPATH=src python -m shard_routing
```

## 코드 지도

- `problem/README.md`: 문제 정의, 제약, 제공 자료, provenance를 확인하는 시작점입니다.
- `docs/README.md`: 개념 메모와 참고자료 인덱스를 먼저 훑는 문서입니다.
- `src/`: 핵심 구현 패키지와 `__main__` entry point가 들어 있습니다.
- `tests/`: pytest 기반 회귀 테스트를 모아 둔 위치입니다.
- `../../../../blog/python/ddia-distributed-systems/03-shard-routing/00-series-map.md`: `src/tests`와 실제 재검증 CLI만으로 다시 구성한 source-first blog 시리즈 입구입니다.
- `notion/README.md`: 현재 공개용 학습 노트와 설계 로그의 입구입니다.
- `notion-archive/README.md`: 이전 세대 문서를 보존하는 아카이브입니다.

## 읽는 순서

- `problem/README.md`로 문제 해석과 현재 범위를 먼저 확인합니다.
- `docs/README.md`와 개념 노트를 읽어, 코드에 들어가기 전 핵심 용어를 맞춥니다.
- `src/`와 `tests/`를 함께 읽고, 마지막에 패키지 entry point를 실행해 전체 흐름을 확인합니다.
- `notion/README.md`와 `notion/01-approach-log.md`로 설계 판단과 학습 메모를 확인합니다.

## 한계와 확장

- 현재 범위 밖: dynamic membership protocol과 gossip은 포함하지 않습니다.
- 현재 범위 밖: 실제 데이터 이동과 rebalancing execution은 capstone 이후 확장 범위입니다.
- 확장 아이디어: membership service, hotspot detector, shard movement visualizer를 추가하면 분산 시스템 포트폴리오로 확장하기 좋습니다.
- 확장 아이디어: replication factor와 rack-awareness까지 고려하면 더 현실적인 router가 됩니다.
