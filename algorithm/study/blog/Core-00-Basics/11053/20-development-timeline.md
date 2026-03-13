# BOJ 11053 — 개발 타임라인 (후반)

## Phase 3
### Session 4
- 목표: C++ 비교 구현과 Python 구현이 같은 답을 내는지 확인한다.
- 진행: C++ 코드도 같은 이중 루프 구조다. 입출력 방식만 다르고 핵심 로직은 동일하다.
- 검증: 둘 다 fixture에서 4를 출력한다.

CLI:

```bash
$ make -C study/Core-00-Basics/11053/problem run-py
$ make -C study/Core-00-Basics/11053/problem run-cpp
$ make -C study/Core-00-Basics/11053/problem test
```

```text
4
4
Test 1: PASS
Results: 1/1 passed, 0 failed
```

### Session 5
- 정리:
  - 이 문제에서 가장 중요했던 판단은 상태 정의였다. `dp[i]`를 "i에서 끝나는 LIS 길이"로 잡는 순간 점화식이 자연스럽게 따라왔다.
  - 처음에 실수할 뻔한 지점이 둘 있었다. `dp[n-1]`을 답으로 착각한 것과, 비교 연산자를 `<=`로 쓸 뻔한 것.
  - 나중에 보니 이 O(N²) 풀이는 가장 기본적인 LIS이고, patience sorting 같은 O(N log N) 방법도 있다. 하지만 N ≤ 1000이면 이중 루프로 충분하다.
  - 다음에 DP 문제를 풀 때는 "무엇을 인덱스로 잡고, 그 인덱스에서 값이 뭘 의미하는지"를 먼저 적는 습관을 갖고 싶다.
