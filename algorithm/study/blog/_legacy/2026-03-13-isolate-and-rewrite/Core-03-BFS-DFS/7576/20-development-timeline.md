# BOJ 7576 — 개발 타임라인 (후반)

## Phase 2
### Session 3
- 목표: grid를 직접 수정하는 방문 처리가 안전한지 확인한다.
- 진행: BFS에서 0인 칸을 1로 바꾸면서 방문 처리를 겸한다. 별도 visited 배열이 필요 없다. 하지만 처음엔 "grid를 변경하면 입력이 오염되지 않나" 걱정이 있었다.
- 판단: 이 문제에서는 grid를 한 번만 읽고 BFS도 한 번만 돌기 때문에 안전하다. 오히려 메모리를 아끼는 좋은 패턴이다.

### Session 4
- 진행: C++ 구현에서도 같은 구조 — vector<vector<int>> grid를 직접 수정하면서 BFS를 돌린다.
- 검증: 두 구현 모두 동일 fixture 통과.

CLI:

```bash
$ make -C study/Core-03-BFS-DFS/7576/problem run-cpp
$ make -C study/Core-03-BFS-DFS/7576/problem test
```

```text
8
Test 1: PASS
Results: 1/1 passed, 0 failed
```

### Session 5
- 정리:
  - multi-source BFS의 핵심은 "시작점이 여러 개"라는 사실을 큐 초기화로 표현하는 것이다. 알고리즘 자체는 단일 BFS와 완전히 같다.
  - 처음엔 각 토마토에서 BFS를 따로 돌려야 한다고 생각했다. 그 가설이 틀린 이유는 "동시에 퍼지는 현상"을 BFS 레벨로 자연스럽게 모델링할 수 있기 때문이다.
  - 마지막 스캔(0이 남아 있는지 확인)을 빼먹으면 도달 불가능한 영역을 놓친다. 이걸 깜빡 안 한 이유는 예제에 -1 케이스가 포함되어 있어서 일찍 잡혔다.
