# BOJ 9663 — 개발 타임라인 (후반)

## Phase 2
### Session 3
- 목표: 상태 복원이 올바른지, Python에서 시간 제한 이내인지 확인한다.
- 진행: 상태 복원은 재귀 호출 전후로 `True/False`를 대칭으로 세팅하면 된다. 처음엔 `diag1` 인덱스를 복원할 때 계산식을 다르게 써서 버그가 났다. 세팅할 때와 해제할 때 인덱스 식이 같아야 한다.
- 이슈: Python에서 N=15면 시간이 빠듯하다. C++로 비교해 보면 속도 차이가 극적이다.

### Session 4
- 검증: C++ 구현은 같은 백트래킹 구조인데 Python 대비 수십 배 빠르다. fixture는 당연히 같은 답을 낸다.

CLI:

```bash
$ make -C study/Core-04-Recursion-Backtracking/9663/problem run-cpp
$ make -C study/Core-04-Recursion-Backtracking/9663/problem test
```

```text
92
Test 1: PASS
Results: 1/1 passed, 0 failed
```

### Session 5
- 정리:
  - N-Queen의 핵심은 "어떤 상태를 기록하고 어떻게 복원하느냐"다. 열 점유, 두 대각선 점유 — 이 세 배열을 정확하게 관리하면 매 칸 체크가 O(1)이 된다.
  - 처음엔 대각선 인덱스 계산에서 막혔다. `row - col`과 `row + col`이 왜 대각선을 식별하는지 2x2 격자에서 손으로 그려보고 나서야 납득했다.
  - 재귀적 backtracking은 "놓고 → 재귀 → 빼기"의 대칭을 반드시 지켜야 한다. 한쪽만 빼먹으면 이후 모든 탐색이 오염된다.
