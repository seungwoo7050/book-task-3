# BOJ 14891 — 개발 타임라인 (후반)

## Phase 2
### Session 3
- 목표: deque 회전과 점수 계산을 확인한다.
- 진행: 시계 방향 회전 = "맨 뒤 원소를 맨 앞으로" = `appendleft(pop())`. 반시계 = "맨 앞 원소를 맨 뒤로" = `append(popleft())`.
- 이슈: 처음엔 시계/반시계를 반대로 구현했다. deque의 회전 방향과 톱니바퀴의 물리적 회전 방향을 혼동한 것이다.

### Session 4
- 검증: fixture 통과.

CLI:

```bash
$ make -C study/Core-05-Simulation/14891/problem test
```

```text
Test 1: PASS
Test 2: PASS
Results: 2/2 passed, 0 failed
```

### Session 5
- 정리:
  - "판정과 실행을 분리"하는 게 이 문제의 전부다. 동시에 돌아가는 현상을 순차 코드로 표현하려면 방향을 먼저 다 결정해야 한다.
  - 인덱스 2와 6을 혼동하는 실수는 문제 그림을 다시 들여다보고 해결했다.
  - deque 회전을 `rotate()` 메서드로도 할 수 있지만, appendleft/pop이 개념적으로 더 명확하다.
