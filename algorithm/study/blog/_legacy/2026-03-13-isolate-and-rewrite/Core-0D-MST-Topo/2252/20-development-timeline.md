# BOJ 2252 — 개발 타임라인 (후반)

## Phase 2
### Session 3
- 목표: 사이클과 edge case를 점검한다.
- 진행: 이 문제는 "모순되는 입력이 없다"고 가정하므로 사이클 체크가 필수는 아니다. 하지만 만약 사이클이 있으면 result 길이가 N보다 작아진다.
- 이슈: M=0이면 순서 제약이 없으니까 1, 2, ..., N 순서로 나온다. 진입차수가 전부 0이니까 초기 큐에 모든 노드가 들어간다.

### Session 4
- 검증: C++ 구현도 같은 Kahn 알고리즘.

CLI:

```bash
$ make -C study/Core-0D-MST-Topo/2252/problem run-cpp
$ make -C study/Core-0D-MST-Topo/2252/problem test
```

```text
Test 1: PASS
Results: 1/1 passed, 0 failed
```

### Session 5
- 정리:
  - 위상 정렬을 처음 써봤다. 진입차수 개념이 명확하면 BFS와 거의 같다.
  - "답이 유일하지 않다"는 조건 덕분에 구현이 단순해졌다. 만약 유일한 순서를 요구했다면 추가 제약이 필요했을 것이다.
  - Kahn vs DFS 기반 중에 Kahn을 고른 이유는 큐 기반이라 BFS와 패턴이 같으니까 실수할 확률이 적다고 판단했기 때문이다.
