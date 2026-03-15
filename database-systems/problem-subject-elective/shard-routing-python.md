# shard-routing-python 문제지

## 왜 중요한가

deterministic consistent hash ring을 구현해야 합니다. batch routing이 가능해야 합니다. add/remove 이후 reassignment count를 계산해야 합니다. empty ring, single node, multi-node 분산을 검증해야 합니다.

## 목표

시작 위치의 구현을 완성해 deterministic consistent hash ring을 구현해야 합니다, batch routing이 가능해야 합니다, add/remove 이후 reassignment count를 계산해야 합니다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../python/ddia-distributed-systems/projects/03-shard-routing/src/shard_routing/__init__.py`
- `../python/ddia-distributed-systems/projects/03-shard-routing/src/shard_routing/__main__.py`
- `../python/ddia-distributed-systems/projects/03-shard-routing/src/shard_routing/core.py`
- `../python/ddia-distributed-systems/projects/03-shard-routing/tests/test_shard_routing.py`
- `../python/ddia-distributed-systems/projects/03-shard-routing/pyproject.toml`

## starter code / 입력 계약

- `../python/ddia-distributed-systems/projects/03-shard-routing/src/shard_routing/__init__.py`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- deterministic consistent hash ring을 구현해야 합니다.
- batch routing이 가능해야 합니다.
- add/remove 이후 reassignment count를 계산해야 합니다.
- empty ring, single node, multi-node 분산을 검증해야 합니다.

## 제외 범위

- 같은 주제의 다른 runtime 구현을 섞어 읽지 않는다.

## 성공 체크리스트

- 핵심 흐름은 `hash_value`와 `RingEntry`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `test_empty_and_single_node_routing`와 `test_distribution_and_rebalance`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `cd /Users/woopinbell/work/book-task-3/database-systems/python/ddia-distributed-systems/projects/03-shard-routing && PYTHONPATH=src python3 -m pytest`가 통과한다.

## 검증 방법

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/python/ddia-distributed-systems/projects/03-shard-routing && PYTHONPATH=src python3 -m pytest
```

- 이 검증 명령을 직접 실행하려면 현재 셸에 `pytest`가 설치돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`shard-routing-python_answer.md`](shard-routing-python_answer.md)에서 확인한다.
