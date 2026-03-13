# BOJ 1167 — 개발 타임라인 (후반)

## Phase 2
### Session 3
- 목표: 입력 파싱과 edge case를 점검한다.
- 진행: 입력의 각 줄이 "노드번호 [인접노드 가중치] ... -1" 형태라 while 루프로 -1이 나올 때까지 읽어야 한다.
- 이슈: 노드가 하나뿐이면? bfs(1)에서 far_node가 1 자신이고, bfs(1)에서 다시 distance 0이 나온다. 답은 0. 정상.

### Session 4
- 검증: C++ 구현도 같은 two-pass BFS.

CLI:

```bash
$ make -C study/Core-0B-Graph-Tree/1167/problem run-cpp
$ make -C study/Core-0B-Graph-Tree/1167/problem test
```

```text
11
Test 1: PASS
Results: 1/1 passed, 0 failed
```

### Session 5
- 정리:
  - 트리 지름의 two-pass 알고리즘은 알고리즘 자체보다 "왜 맞는가"가 더 어렵다.
  - 처음엔 Dijkstra가 필요하다고 생각했는데, 트리에서는 경로가 유일하니까 BFS로 가중치 합을 누적하면 충분하다.
  - 입력 파싱이 다른 문제와 달라서(고정 개수가 아니라 -1 종료) 여기서 실수하면 올바른 트리가 안 만들어진다.
