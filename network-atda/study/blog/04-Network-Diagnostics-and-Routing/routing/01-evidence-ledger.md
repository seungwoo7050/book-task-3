# Distance-Vector Routing Evidence Ledger

## 이번에 읽은 자료

- 문제 사양: `study/04-Network-Diagnostics-and-Routing/routing/problem/README.md`
- 구현 엔트리: `study/04-Network-Diagnostics-and-Routing/routing/python/src/dv_routing.py`
- 보조 테스트: `study/04-Network-Diagnostics-and-Routing/routing/python/tests/test_dv_routing.py`
- 검증 스크립트: `study/04-Network-Diagnostics-and-Routing/routing/problem/script/test_routing.sh`

## 핵심 코드 근거

- `load_topology()`: JSON topology를 양방향 adjacency dict로 만든다.
- `DVNode.__init__()`: self cost `0`, direct neighbors cost `link cost`, others `INF`로 초기화한다.
- `receive_dv()`: cached neighbor DVs를 바탕으로 min cost와 next hop을 갱신한다.
- `simulate()`: 각 iteration에서 먼저 messages snapshot을 만들고, 그 snapshot만으로 phase-2 update를 수행한다.

## 테스트 근거

`make -C network-atda/study/04-Network-Diagnostics-and-Routing/routing/problem test`

결과:

- `3-node topology convergence` pass
- `x→z shortest path = 3 via y` pass
- `5-node topology convergence` pass
- `a→e shortest path = 5` pass

보조 실행:

- `python3 python/src/dv_routing.py problem/data/topology.json`
- 출력에서 `Converged after 2 iterations`
- final routing tables에서 `Node x: to z cost 3 via y`

## 이번에 고정한 해석

- 이 구현은 distributed routing을 설명하지만 messaging delay가 없는 teaching simulator다.
- convergence story의 핵심은 formula보다 `neighbor_dvs` snapshot을 round 단위로 고정하는 데 있다.
- next hop을 따로 저장하지 않으면 shortest path cost만 있고 실제 forwarding decision은 남지 않는다.
