# BOJ 2110 — 개발 타임라인 (후반)

## Phase 2
### Session 3
- 목표: 정렬 전제 조건과 edge case를 점검한다.
- 진행: houses를 정렬하지 않으면 feasible 함수의 greedy 선택이 보장되지 않는다. "앞에서부터 가능한 한 멀리 건너뛰며 놓는" 전략은 정렬된 배열에서만 성립한다.
- 이슈: C=2이면 답은 항상 `houses[-1] - houses[0]`이다. 이걸 별도 분기 없이 이분 탐색이 정확하게 잡아내는지 확인했다.
- 판단: 정상 동작한다. lo=1, hi=houses[-1]-houses[0]에서 mid가 hi와 같아질 때 feasible이 True이므로 ans가 hi로 잡힌다.

### Session 4
- 검증: C++ 구현은 같은 이분 탐색 + greedy feasibility 구조.

CLI:

```bash
$ make -C study/Core-07-Binary-Search-Hash/2110/problem run-cpp
$ make -C study/Core-07-Binary-Search-Hash/2110/problem test
```

```text
3
Test 1: PASS
Results: 1/1 passed, 0 failed
```

### Session 5
- 정리:
  - parametric search의 핵심은 "답을 먼저 정하고 가능한지 판정한다"는 발상의 전환이다.
  - 처음엔 조합 탐색으로 접근하려 했는데, 판정 함수를 O(N)으로 구현할 수 있다는 걸 알고 나서야 이분 탐색이 가능하다고 확신했다.
  - Greedy feasibility가 성립하는 이유는 "정렬된 배열에서 가능한 한 먼 곳에 놓는 게 항상 이후 선택을 제한하지 않기 때문"이다. 이 증명을 스스로 써보지는 않았지만, 감각적으로는 맞다.
