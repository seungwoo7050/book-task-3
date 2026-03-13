# Distance-Vector Routing 시리즈 지도

이 프로젝트를 한 줄로: JSON topology를 읽어 node마다 자신의 distance vector를 유지하게 하고, Bellman-Ford로 이웃 DV를 반영해 수렴까지 돌리는 분산 라우팅 시뮬레이션을 구현한 기록.

## 파일 구성

| 파일 | 역할 |
|------|------|
| `problem/code/dv_skeleton.py` | 제공된 스켈레톤 |
| `problem/data/topology.json` | 3노드 삼각형 |
| `problem/data/topology_5node.json` | 5노드 링 구조 |
| `python/src/dv_routing.py` | 직접 작성한 구현 |
| `python/tests/test_dv_routing.py` | 수렴 결과 단언 테스트 |
| `problem/Makefile` | `test` / `run-solution` 진입점 |

## canonical verification

```bash
# 비권한 단위 테스트
make -C study/04-Network-Diagnostics-and-Routing/routing/problem test

# 시뮬레이션 실행
make -C study/04-Network-Diagnostics-and-Routing/routing/problem run-solution
```

## 이 시리즈에서 따라갈 질문

1. `DVNode.__init__()`은 자신 / 이웃 / 나머지 노드에 각각 어떤 초기값을 넣는가?
2. `receive_dv()`의 Bellman-Ford는 `cost_via_v = link_cost + neighbor_dv.get(dest, INF)`를 어떻게 `best_hop`까지 연결하는가?
3. 2-phase simulate()는 메시지를 먼저 수집하고 나서 적용하는데, 이 순서가 중요한 이유는 무엇인가?
4. convergence 판정은 단순 라운드 수 제한인가, DV가 실제 변하지 않는 지점 판단인가?

## 글 파일

- [10-development-timeline.md](10-development-timeline.md)
