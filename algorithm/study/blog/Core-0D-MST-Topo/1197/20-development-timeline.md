# BOJ 1197 — 개발 타임라인 (후반)

## Phase 2
### Session 3
- 목표: edge case와 성능을 점검한다.
- 진행: 문제 조건상 그래프가 연결이므로 MST가 항상 존재한다. cnt == v-1에서 조기 종료하면 불필요한 간선 검사를 줄일 수 있다.
- 이슈: 가중치가 음수일 수 있다. Kruskal은 가중치 부호와 무관하게 동작한다.

### Session 4
- 검증: C++ 구현도 같은 Kruskal + union-find.

CLI:

```bash
$ make -C study/Core-0D-MST-Topo/1197/problem run-cpp
$ make -C study/Core-0D-MST-Topo/1197/problem test
```

```text
3
Test 1: PASS
Results: 1/1 passed, 0 failed
```

### Session 5
- 정리:
  - Kruskal의 핵심은 "가장 싼 간선부터 사이클 없이 추가"라는 단순한 규칙이다.
  - 유니온파인드를 Core-Bridges(1717)에서 먼저 연습한 덕분에 여기서는 바로 적용할 수 있었다.
  - path compression의 반복적 구현(할아버지 포인터)은 Python 재귀 제한을 피하는 실용적 선택이다.
