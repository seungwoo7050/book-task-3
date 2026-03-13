# N-Queen: 검증, edge case, 마지막 설명 축

앞 절반이 출발점이었다면, 뒷 절반은 마무리 단계다. 테스트, edge case, 개념 정리를 같은 흐름으로 묶어 이 풀이가 어디에서 안정됐는지 보여 준다.

## 구현 순서 요약

- `make -C study/Core-04-Recursion-Backtracking/9663/problem test`로 fixture 전체를 다시 돌린다.
- `docs/references/approach.md`의 실수 포인트를 코드 분기와 연결한다.
- `N-Queen 개념 정리`와 `cpp/src/solution.cpp`를 붙여 마지막 판단 기준을 고정한다.

## Phase 3
### Session 3

- 당시 목표: 한두 개 입력이 맞는 수준을 넘어서 fixture 전체를 통과하는 구조로 묶는다.
- 변경 단위: `problem/script/test.sh`, `docs/references/approach.md`, `docs/concepts/edge-cases.md`
- 처음 가설: 실수 포인트를 문장으로만 남기면 다시 틀리기 쉽고, 테스트 루프와 함께 봐야 실제 방어선이 보인다.
- 실제 조치: `test.sh`의 PASS/FAIL 루프와 `approach.md`의 실수 체크리스트를 나란히 읽으며, 어떤 분기가 어디를 막는지 다시 맞췄다.

CLI 1:

```bash
$ make -C study/Core-04-Recursion-Backtracking/9663/problem test
```

검증 신호:

- `Test 1: PASS`, `Results: 1/1 passed, 0 failed` 순서로 출력됐다.
- 이번 단계에서 특히 다시 확인한 실수 포인트는 아래 셋이었다.

- 좌상/우상 대각선 인덱스 변환 오류
- 해를 찾은 뒤 카운트 증가 누락
- 상태 복원 순서 오류

핵심 코드 1:

```python
        for c in range(n):
            if not col[c] and not diag1[row - c + n - 1] and not diag2[row + c]:
                col[c] = diag1[row - c + n - 1] = diag2[row + c] = True
                place(row + 1)
                col[c] = diag1[row - c + n - 1] = diag2[row + c] = False

    place(0)
    print(count)

if __name__ == "__main__":
```

왜 이 코드가 중요했는가:

이 블록을 다시 보면 `좌상/우상 대각선 인덱스 변환 오류`를 막는 자리가 어디인지 바로 보인다. 테스트가 통과했다는 사실을 코드로 다시 설명하는 데 가장 적절한 증거다.

새로 배운 것:

- 테스트를 다시 읽는 순간, “맞았다”보다 “어디서 안 틀리는가”를 더 분명하게 설명할 수 있었다.

다음:

- 마지막으로 개념 문서와 코드가 어느 지점에서 맞물리는지 정리한다.

## Phase 4
### Session 4

- 당시 목표: `N-Queen 개념 정리`를 실제 코드와 연결해 마지막 설명 축을 세운다.
- 변경 단위: `cpp/src/solution.cpp`, `docs/concepts/*.md`, `python/src/solution.py`
- 처음 가설: 마지막 글에서 남겨야 할 것은 추상 개념이 아니라, 그 개념이 꼭 필요해진 줄이다.
- 실제 조치: Python과 C++ 구현을 나란히 읽으며 같은 전이가 유지되는지 확인했다.

CLI 2:

```bash
$ make -C study/Core-04-Recursion-Backtracking/9663/problem run-cpp
```

검증 신호:

- `92`가 그대로 나왔다.
- 설명용 문서가 아니라 실제 실행 결과와 같은 답이 나온다는 점이 마지막 확인 포인트였다.

핵심 코드 2:

```cpp
    for (int c = 0; c < n; c++) {
        if (!col_used[c] && !diag1[row - c + n - 1] && !diag2[row + c]) {
            col_used[c] = diag1[row - c + n - 1] = diag2[row + c] = true;
            place(row + 1);
            col_used[c] = diag1[row - c + n - 1] = diag2[row + c] = false;
        }
    }
}

int main() {
```

왜 이 코드가 중요했는가:

이 블록 덕분에 개념 정리가 공중에 뜨지 않는다. `좌상/우상 대각선 인덱스 변환 오류`를 막는 방식과 `열/대각선 점유 배열을 이용한 N-Queen backtracking`가 여기서 한 번에 맞물린다.

핵심 코드 3:

```python
    place(0)
    print(count)

if __name__ == "__main__":
    solve()
```

왜 이 코드가 중요했는가:

마지막 출력과 종료 조건은 사소해 보여도 최종 출력까지 닫는 부분이다. `N-Queen`도 이 구간이 흐려지면 첫 구현은 맞아 보여도 최종 설명이 흔들린다.

새로 배운 것:

- C++ 쪽까지 다시 확인하고 나니, 이 문제에서 중요한 건 표현 방식이 아니라 `열/대각선 점유 배열을 이용한 N-Queen backtracking`를 끝까지 보존하는 전이 순서라는 점이었다.
- 그래서 `Core-04-Recursion-Backtracking`의 질문인 `재귀 호출 구조와 상태 복원을 어디까지 명시해야 할까?`도 결과 요약이 아니라, 상태와 순서를 어떻게 붙잡는가의 문제로 읽히게 됐다.

다음:

- 이 시리즈는 여기서 닫히지만, 다음 문제를 읽을 때도 `문제 계약 -> 첫 상태 -> fixture 검증` 순서를 그대로 재사용할 수 있다.
