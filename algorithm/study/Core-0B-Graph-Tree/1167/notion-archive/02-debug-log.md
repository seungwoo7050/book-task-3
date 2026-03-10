# BOJ 1167 — 디버깅 기록

## 함정 1: 입력 파싱

**증상**: 인덱스 오류

**원인**: 각 줄이 `노드 이웃 가중치 이웃 가중치 ... -1` 형식으로, 2씩 건너뛰어야 함

**해결**: `while data[i] != -1: ... i += 2`

## 함정 2: 재귀 깊이 (DFS 사용시)

**증상**: RecursionError

**원인**: $V \leq 100,000$에서 DFS 재귀 시 스택 오버플로

**해결**: BFS(deque) 사용. 또는 `sys.setrecursionlimit` 설정 (코드에 200000으로 설정됨)

## 함정 3: 양방향 간선

무방향 트리이므로 `adj[node].append`와 `adj[neighbor].append` 둘 다 필요... 하지만 이 문제는 입력 자체가 각 노드 기준으로 모든 인접 점을 나열하므로 한 방향만 넣으면 됨.

## 확인 과정

```bash
make -C problem test
make -C problem run-cpp
```

PASS.
