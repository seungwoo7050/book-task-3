# 토마토: 검증, edge case, 마지막 설명 축

이제는 구현을 끝냈다고 말하는 단계가 아니라, 어떤 근거로 끝났다고 말할 수 있는지를 정리하는 단계다. 테스트 루프와 마지막 설명 축이 여기서 닫힌다.

## 구현 순서 요약

- `make -C study/Core-03-BFS-DFS/7576/problem test`로 fixture 전체를 다시 돌린다.
- `docs/references/approach.md`의 실수 포인트를 코드 분기와 연결한다.
- `다중 소스 BFS(Multi-Source BFS) 개념 정리`와 `cpp/src/solution.cpp`를 붙여 마지막 판단 기준을 고정한다.

## Phase 3
### Session 3

- 당시 목표: 한두 개 입력이 맞는 수준을 넘어서 fixture 전체를 통과하는 구조로 묶는다.
- 변경 단위: `problem/script/test.sh`, `docs/references/approach.md`, `docs/concepts/edge-cases.md`
- 처음 가설: 실수 포인트를 문장으로만 남기면 다시 틀리기 쉽고, 테스트 루프와 함께 봐야 실제 방어선이 보인다.
- 실제 조치: `test.sh`의 PASS/FAIL 루프와 `approach.md`의 실수 체크리스트를 나란히 읽으며, 어떤 분기가 어디를 막는지 다시 맞췄다.

CLI 1:

```bash
$ make -C study/Core-03-BFS-DFS/7576/problem test
```

검증 신호:

- `Test 1: PASS`, `Results: 1/1 passed, 0 failed` 순서로 출력됐다.
- 이번 단계에서 특히 다시 확인한 실수 포인트는 아래 셋이었다.

- 초기 큐 시드(익은 토마토) 누락
- -1(빈 칸) 처리 실수
- 최종 미익음 검사 누락으로 -1 판정 실패

핵심 코드 1:

```python
    for i in range(N):
        row = list(map(int, input().split()))
        grid.append(row)
        for j in range(M):
            if row[j] == 1:
                q.append((i, j, 0))  # 행, 열, 경과일

    dx = [0, 0, 1, -1]
    dy = [1, -1, 0, 0]
    ans = 0
```

왜 이 코드가 중요했는가:

검증의 핵심은 통과 여부보다 방어선의 위치를 확인하는 데 있다. 이 블록은 어떤 분기가 edge case를 실제로 막아 주는지 보여 준다.

새로 배운 것:

- 테스트를 다시 읽는 순간, “맞았다”보다 “어디서 안 틀리는가”를 더 분명하게 설명할 수 있었다.

다음:

- 마지막으로 개념 문서와 코드가 어느 지점에서 맞물리는지 정리한다.

## Phase 4
### Session 4

- 당시 목표: `다중 소스 BFS(Multi-Source BFS) 개념 정리`를 실제 코드와 연결해 마지막 설명 축을 세운다.
- 변경 단위: `cpp/src/solution.cpp`, `docs/concepts/*.md`, `python/src/solution.py`
- 처음 가설: 마지막 글에서 남겨야 할 것은 추상 개념이 아니라, 그 개념이 꼭 필요해진 줄이다.
- 실제 조치: Python과 C++ 구현을 나란히 읽으며 같은 전이가 유지되는지 확인했다.

CLI 2:

```bash
$ make -C study/Core-03-BFS-DFS/7576/problem run-cpp
```

검증 신호:

- `8`가 그대로 나왔다.
- 설명용 문서가 아니라 실제 실행 결과와 같은 답이 나온다는 점이 마지막 확인 포인트였다.

핵심 코드 2:

```cpp
    for (int i = 0; i < N; i++)
        for (int j = 0; j < M; j++) {
            cin >> grid[i][j];
            if (grid[i][j] == 1) q.push({i, j, 0});
        }

    int dx[] = {0, 0, 1, -1};
    int dy[] = {1, -1, 0, 0};
    int ans = 0;
```

왜 이 코드가 중요했는가:

마지막 전환점은 이 코드였다. `다중 소스 BFS(Multi-Source BFS) 개념 정리`를 붙여 읽으면, 왜 이 문제의 설명이 결국 이 줄로 수렴하는지 자연스럽게 보인다.

핵심 코드 3:

```python
            return

    print(ans)

if __name__ == "__main__":
    solve()
```

왜 이 코드가 중요했는가:

마지막 출력과 종료 조건은 사소해 보여도 최종 출력까지 닫는 부분이다. `토마토`도 이 구간이 흐려지면 첫 구현은 맞아 보여도 최종 설명이 흔들린다.

새로 배운 것:

- 비교 구현을 함께 읽으니 `다중 소스 BFS(Multi-Source BFS) 개념 정리`가 더 선명해졌다. 언어가 달라도 `다중 시작점(multi-source) BFS로 토마토 익는 날짜를 레벨 단위 전파`를 지탱하는 상태 규칙은 거의 바뀌지 않았다.
- 그래서 `Core-03-BFS-DFS`의 질문인 `그래프 표현과 방문 순서를 어떻게 고정할까?`도 결과 요약이 아니라, 상태와 순서를 어떻게 붙잡는가의 문제로 읽히게 됐다.

다음:

- 이 시리즈는 여기서 닫히지만, 다음 문제를 읽을 때도 `문제 계약 -> 첫 상태 -> fixture 검증` 순서를 그대로 재사용할 수 있다.
