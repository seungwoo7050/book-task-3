# 가장 긴 증가하는 부분 수열: 검증, edge case, 마지막 설명 축

앞 절반이 출발점이었다면, 뒷 절반은 마무리 단계다. 테스트, edge case, 개념 정리를 같은 흐름으로 묶어 이 풀이가 어디에서 안정됐는지 보여 준다.

## 구현 순서 요약

- `make -C study/Core-00-Basics/11053/problem test`로 fixture 전체를 다시 돌린다.
- `docs/references/approach.md`의 실수 포인트를 코드 분기와 연결한다.
- `LIS (Longest Increasing Subsequence) — Concept & Background`와 `cpp/src/solution.cpp`를 붙여 마지막 판단 기준을 고정한다.

## Phase 3
### Session 3

- 당시 목표: 한두 개 입력이 맞는 수준을 넘어서 fixture 전체를 통과하는 구조로 묶는다.
- 변경 단위: `problem/script/test.sh`, `docs/references/approach.md`, `docs/concepts/edge-cases.md`
- 처음 가설: 실수 포인트를 문장으로만 남기면 다시 틀리기 쉽고, 테스트 루프와 함께 봐야 실제 방어선이 보인다.
- 실제 조치: `test.sh`의 PASS/FAIL 루프와 `approach.md`의 실수 체크리스트를 나란히 읽으며, 어떤 분기가 어디를 막는지 다시 맞췄다.

CLI 1:

```bash
$ make -C study/Core-00-Basics/11053/problem test
```

검증 신호:

- `Test 1: PASS`, `Results: 1/1 passed, 0 failed` 순서로 출력됐다.
- 이번 단계에서 특히 다시 확인한 실수 포인트는 아래 셋이었다.

- 엄격 증가(<) 대신 비엄격 증가(<=)를 써서 정답이 커지는 실수
- dp 초기값을 0으로 두어 길이 1 케이스를 놓치는 문제
- 최종 정답을 max(dp)로 집계하지 않는 누락

핵심 코드 1:

```python
    dp = [1] * n

    for i in range(1, n):
        for j in range(i):
            if a[j] < a[i]:
                dp[i] = max(dp[i], dp[j] + 1)

    print(max(dp))

if __name__ == "__main__":
```

왜 이 코드가 중요했는가:

이 블록을 다시 보면 `엄격 증가(<) 대신 비엄격 증가(<=)를 써서 정답이 커지는 실수`를 막는 자리가 어디인지 바로 보인다. 테스트가 통과했다는 사실을 코드로 다시 설명하는 데 가장 적절한 증거다.

새로 배운 것:

- 테스트를 다시 읽는 순간, “맞았다”보다 “어디서 안 틀리는가”를 더 분명하게 설명할 수 있었다.

다음:

- 마지막으로 개념 문서와 코드가 어느 지점에서 맞물리는지 정리한다.

## Phase 4
### Session 4

- 당시 목표: `LIS (Longest Increasing Subsequence) — Concept & Background`를 실제 코드와 연결해 마지막 설명 축을 세운다.
- 변경 단위: `cpp/src/solution.cpp`, `docs/concepts/*.md`, `python/src/solution.py`
- 처음 가설: 마지막 글에서 남겨야 할 것은 추상 개념이 아니라, 그 개념이 꼭 필요해진 줄이다.
- 실제 조치: Python과 C++ 구현을 나란히 읽으며 같은 전이가 유지되는지 확인했다.

CLI 2:

```bash
$ make -C study/Core-00-Basics/11053/problem run-cpp
```

검증 신호:

- `4`가 그대로 나왔다.
- 설명용 문서가 아니라 실제 실행 결과와 같은 답이 나온다는 점이 마지막 확인 포인트였다.

핵심 코드 2:

```cpp
    for (int i = 0; i < n; i++) cin >> a[i];

    // dp[i] = i에서 끝나는 LIS 길이
    vector<int> dp(n, 1);

    for (int i = 1; i < n; i++) {
        for (int j = 0; j < i; j++) {
            if (a[j] < a[i]) {
                dp[i] = max(dp[i], dp[j] + 1);
            }
```

왜 이 코드가 중요했는가:

여기서는 `LIS (Longest Increasing Subsequence) — Concept & Background`가 별도 해설이 아니라는 점이 분명해진다. `1차원 DP로 각 위치에서 끝나는 LIS 길이를 누적 계산`를 끝까지 지키는 데 필요한 최소 단위가 바로 이 블록에 남아 있다.

핵심 코드 3:

```python
                dp[i] = max(dp[i], dp[j] + 1)

    print(max(dp))

if __name__ == "__main__":
    solve()
```

왜 이 코드가 중요했는가:

이 문제는 마지막 한 줄까지 포함해 설명이 완성된다. 출력 정리와 종료 조건이 흐리면 서사도 같이 흐려진다.

새로 배운 것:

- C++ 쪽까지 다시 확인하고 나니, 이 문제에서 중요한 건 표현 방식이 아니라 `1차원 DP로 각 위치에서 끝나는 LIS 길이를 누적 계산`를 끝까지 보존하는 전이 순서라는 점이었다.
- 그래서 `Core-00-Basics`의 질문인 `작은 입력과 조건 분기를 어떻게 안정적으로 구현하고 검증할까?`도 결과 요약이 아니라, 상태와 순서를 어떻게 붙잡는가의 문제로 읽히게 됐다.

다음:

- 이 시리즈는 여기서 닫히지만, 다음 문제를 읽을 때도 `문제 계약 -> 첫 상태 -> fixture 검증` 순서를 그대로 재사용할 수 있다.
