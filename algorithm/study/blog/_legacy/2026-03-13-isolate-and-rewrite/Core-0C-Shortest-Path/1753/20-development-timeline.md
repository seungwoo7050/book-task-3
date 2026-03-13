# BOJ 1753 — 개발 타임라인 (후반)

## Phase 2
### Session 3
- 목표: 출력 형식과 edge case를 점검한다.
- 진행: 도달 불가능한 노드는 dist가 INF로 남아 있으니 "INF" 문자열을 출력한다.
- 이슈: 같은 두 노드 사이에 간선이 여러 개일 수 있다. 인접 리스트에 전부 넣으면 Dijkstra가 자동으로 최소를 선택한다.

### Session 4
- 검증: C++ 구현도 같은 Dijkstra with lazy deletion.

CLI:

```bash
$ make -C study/Core-0C-Shortest-Path/1753/problem run-cpp
$ make -C study/Core-0C-Shortest-Path/1753/problem test
```

```text
Test 1: PASS
Results: 1/1 passed, 0 failed
```

### Session 5
- 정리:
  - Dijkstra에서 핵심은 lazy deletion이다. `if d > dist[u]: continue`를 빼먹으면 정확도는 보장되지만 속도가 극적으로 느려진다.
  - 이 문제는 1916(최소비용 구하기)과 달리 모든 정점까지의 거리를 출력하므로, 도달 불가능 처리가 추가된다.
  - Bellman-Ford(11657)와의 차이는 "음수 간선 허용 여부"다. 양수만이면 항상 Dijkstra가 효율적이다.
