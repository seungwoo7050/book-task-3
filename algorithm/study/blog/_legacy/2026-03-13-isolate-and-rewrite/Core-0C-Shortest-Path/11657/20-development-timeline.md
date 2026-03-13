# BOJ 11657 — 개발 타임라인 (후반)

## Phase 2
### Session 3
- 목표: 음수 사이클 검출 범위를 확인한다.
- 진행: `dist[a] != INF` 조건 덕분에 시작점에서 도달 불가능한 노드는 아예 완화되지 않는다. 따라서 그 쪽에 음수 사이클이 있어도 검출되지 않는다.
- 이슈: 이 문제는 "1번 도시에서 나머지 도시로"의 최단 경로이므로, 1번에서 도달 불가능한 음수 사이클은 무시해야 맞다.
- 판단: 구현이 요구 사항에 맞다.

### Session 4
- 검증: C++ 구현은 같은 Bellman-Ford 구조.

CLI:

```bash
$ make -C study/Core-0C-Shortest-Path/11657/problem run-cpp
$ make -C study/Core-0C-Shortest-Path/11657/problem test
```

```text
Test 1: PASS
Results: 1/1 passed, 0 failed
```

### Session 5
- 정리:
  - Bellman-Ford의 핵심은 "V-1번 완화하면 최단 경로가 확정되고, V번째에 완화가 되면 음수 사이클"이라는 성질이다.
  - `dist[a] != INF` 가드를 빼먹으면 도달 불가능한 노드에서 음수 간선을 타고 잘못된 갱신이 발생한다. 이거 하나 때문에 처음에 WA가 났다.
  - Dijkstra와 Bellman-Ford 중 무엇을 쓸지의 기준은 결국 "음수 간선이 있는가"다. 이 문제가 바로 그 분기점을 보여준다.
