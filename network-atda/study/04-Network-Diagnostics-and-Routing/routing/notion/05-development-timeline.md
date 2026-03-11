# 05 개발 타임라인

이 문서는 `Distance-Vector Routing`을 처음 재현하는 학생을 위한 실행 가이드다. 핵심은 작은 토폴로지에서 수렴을 눈으로 본 뒤, 테스트로 결과를 고정하는 것이다.

## 준비
- `python3`
- `pytest`
- 작업 위치: 저장소 루트 `/Users/woopinbell/work/book-task-3/network-atda`

## 단계 1. 문제와 제공물 확인
먼저 아래 파일을 읽는다.
- [`../problem/README.md`](../problem/README.md)
- [`../problem/data/topology.json`](../problem/data/topology.json)
- [`../problem/data/topology_5node.json`](../problem/data/topology_5node.json)
- [`../problem/code/dv_skeleton.py`](../problem/code/dv_skeleton.py)

여기서 확인할 질문:
- 노드는 무엇을 알고 있고 무엇을 모르는가
- 입력 토폴로지는 어떤 형식으로 들어오는가
- 수렴은 어떤 시점에 끝났다고 보는가

## 단계 2. 구현과 테스트 기준을 먼저 본다
- [`../python/src/dv_routing.py`](../python/src/dv_routing.py)
- [`../python/tests/test_dv_routing.py`](../python/tests/test_dv_routing.py)

이 단계에서 볼 포인트:
- 초기 DV와 `next_hop`을 어디서 잡는가
- iteration을 왜 2-phase로 나눴는가
- `deepcopy`가 왜 필요한가

## 단계 3. 자동 검증 먼저 실행
아래 명령으로 현재 상태를 먼저 고정한다.

```bash
make -C study/04-Network-Diagnostics-and-Routing/routing/problem test
```

기대 결과:
- 여러 토폴로지에 대한 검증이 통과한다.
- 수렴 조건과 출력 형식이 스크립트 기준을 만족한다.

세부 테스트는 아래로 확인한다.

```bash
cd study/04-Network-Diagnostics-and-Routing/routing/python/tests
python3 -m pytest test_dv_routing.py -v
```

## 단계 4. 토폴로지를 직접 돌려 본다
아래 두 명령을 차례대로 실행한다.

```bash
make -C study/04-Network-Diagnostics-and-Routing/routing/problem run-solution TOPO=data/topology.json
make -C study/04-Network-Diagnostics-and-Routing/routing/problem run-solution TOPO=data/topology_5node.json
```

기대 결과:
- iteration별 DV 변화가 출력된다.
- 3노드 토폴로지에서는 `x -> z` 비용이 직접 링크 `7`이 아니라 `y` 경유 `3`으로 수렴한다.
- 마지막에는 목적지별 비용과 next-hop을 읽을 수 있다.

## 단계 5. 실패하면 가장 먼저 볼 곳
- 결과가 실행 순서에 따라 달라지면 2-phase 수집/업데이트가 섞였는지 확인한다.
- 값이 이상하게 공유되면 `deepcopy` 여부를 먼저 본다.
- self-route가 깨지면 초기화 규칙과 self cost `0` 유지 여부를 확인한다.
- 관련 근거는 [`02-debug-log.md`](02-debug-log.md)에 정리했다.

## 단계 6. 완료 판정
아래 조건을 만족하면 이 프로젝트는 재현한 것으로 본다.
- `make test`가 통과한다.
- 두 토폴로지를 직접 돌려 수렴 출력을 봤다.
- Bellman-Ford 식을 코드 변수와 연결해 설명할 수 있다.
- 비용과 next-hop을 왜 같이 저장해야 하는지 설명할 수 있다.
