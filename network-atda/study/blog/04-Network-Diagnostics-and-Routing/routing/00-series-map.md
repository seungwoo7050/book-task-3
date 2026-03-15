# Distance-Vector Routing 시리즈 맵

이 lab의 중심 질문은 "Bellman-Ford 식이 실제 node-local routing table update로 내려오면 어떤 state와 round structure가 필요해지는가"다. 현재 구현은 `distance_vector`, `next_hop`, `neighbor_dvs`를 각 node에 들고, simulation loop에서는 먼저 모든 node의 DV snapshot을 모은 뒤 그 snapshot으로만 갱신한다. 즉 shortest path computation을 centralized algorithm이 아니라, distributed but synchronous exchange로 읽게 만든다.

## 이 lab를 읽는 질문

- 왜 `receive_dv()`는 sender 하나의 DV를 받을 때마다 전체 destination set을 다시 훑는가
- synchronous 2-phase loop가 없으면 어떤 self-feedback 문제가 생길 수 있는가
- `distance_vector`와 `next_hop`를 함께 관리해야 실제 routing table이 완성되는 이유는 무엇인가

## 이번에 사용한 근거

- `problem/README.md`
- `python/src/dv_routing.py`
- `python/tests/test_dv_routing.py`
- `problem/script/test_routing.sh`
- 2026-03-14 재실행한 solution output

## 이번 재실행에서 고정한 사실

- `load_topology()`는 undirected edge를 양방향 adjacency로 풀어 낸다.
- `receive_dv()`는 `c(x,v) + D_v(y)`를 모든 neighbor에 대해 비교해 best cost와 next hop을 갱신한다.
- 3-node topology에서 node `x`의 `z` cost는 initial `7`에서 `3 via y`로 바뀐다.
- 5-node topology test는 `a -> d = 4`, `a -> e = 5` 수렴을 고정한다.
