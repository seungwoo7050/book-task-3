# 수 묶기: 검증, edge case, 마지막 설명 축

이제는 구현을 끝냈다고 말하는 단계가 아니라, 어떤 근거로 끝났다고 말할 수 있는지를 정리하는 단계다. 테스트 루프와 마지막 설명 축이 여기서 닫힌다.

## 구현 순서 요약

- `make -C study/Core-09-Greedy/1744/problem test`로 fixture 전체를 다시 돌린다.
- `docs/references/approach.md`의 실수 포인트를 코드 분기와 연결한다.
- `수 묶기 그리디 개념 정리`와 `cpp/src/solution.cpp`를 붙여 마지막 판단 기준을 고정한다.

## Phase 3
### Session 3

- 당시 목표: 한두 개 입력이 맞는 수준을 넘어서 fixture 전체를 통과하는 구조로 묶는다.
- 변경 단위: `problem/script/test.sh`, `docs/references/approach.md`, `docs/concepts/edge-cases.md`
- 처음 가설: 실수 포인트를 문장으로만 남기면 다시 틀리기 쉽고, 테스트 루프와 함께 봐야 실제 방어선이 보인다.
- 실제 조치: `test.sh`의 PASS/FAIL 루프와 `approach.md`의 실수 체크리스트를 나란히 읽으며, 어떤 분기가 어디를 막는지 다시 맞췄다.

CLI 1:

```bash
$ make -C study/Core-09-Greedy/1744/problem test
```

검증 신호:

- `Test 1: PASS`, `Results: 1/1 passed, 0 failed` 순서로 출력됐다.
- 이번 단계에서 특히 다시 확인한 실수 포인트는 아래 셋이었다.

- 1을 곱해버려 합이 감소하는 실수
- 남는 음수와 0 상쇄 누락
- 양수 내림차순 정렬 누락

핵심 코드 1:

```python
    for _ in range(N):
        x = int(input())
        if x > 1:
            pos.append(x)
        elif x == 1:
            ones += 1
        elif x == 0:
            zeros += 1
        else:
            neg.append(x)
```

왜 이 코드가 중요했는가:

이 블록을 다시 보면 `1을 곱해버려 합이 감소하는 실수`를 막는 자리가 어디인지 바로 보인다. 테스트가 통과했다는 사실을 코드로 다시 설명하는 데 가장 적절한 증거다.

새로 배운 것:

- 테스트를 다시 읽는 순간, “맞았다”보다 “어디서 안 틀리는가”를 더 분명하게 설명할 수 있었다.

다음:

- 마지막으로 개념 문서와 코드가 어느 지점에서 맞물리는지 정리한다.

## Phase 4
### Session 4

- 당시 목표: `수 묶기 그리디 개념 정리`를 실제 코드와 연결해 마지막 설명 축을 세운다.
- 변경 단위: `cpp/src/solution.cpp`, `docs/concepts/*.md`, `python/src/solution.py`
- 처음 가설: 마지막 글에서 남겨야 할 것은 추상 개념이 아니라, 그 개념이 꼭 필요해진 줄이다.
- 실제 조치: Python과 C++ 구현을 나란히 읽으며 같은 전이가 유지되는지 확인했다.

CLI 2:

```bash
$ make -C study/Core-09-Greedy/1744/problem run-cpp
```

검증 신호:

- `6`가 그대로 나왔다.
- 설명용 문서가 아니라 실제 실행 결과와 같은 답이 나온다는 점이 마지막 확인 포인트였다.

핵심 코드 2:

```cpp
    for(int i = 0; i < N; i++){
        int x; cin >> x;
        if(x > 1) pos.push_back(x);
        else if(x == 1) ones++;
        else if(x == 0) zeros++;
        else neg.push_back(x);
    }

    long long total = ones;
```

왜 이 코드가 중요했는가:

이 블록 덕분에 개념 정리가 공중에 뜨지 않는다. `1을 곱해버려 합이 감소하는 실수`를 막는 방식과 `양수/음수/1/0을 분리해 곱셈 이득이 큰 쌍을 우선 결합`가 여기서 한 번에 맞물린다.

핵심 코드 3:

```python
            total += neg[-1]

    print(total)

if __name__ == "__main__":
    main()
```

왜 이 코드가 중요했는가:

이 문제는 마지막 한 줄까지 포함해 설명이 완성된다. 출력 정리와 종료 조건이 흐리면 서사도 같이 흐려진다.

새로 배운 것:

- Python과 C++를 나란히 보니 `양수/음수/1/0을 분리해 곱셈 이득이 큰 쌍을 우선 결합`의 본질은 문법이 아니라 전이 순서에 있었다. `1을 곱해버려 합이 감소하는 실수`를 막는 규칙이 두 구현에서 그대로 유지됐다.
- 그래서 `Core-09-Greedy`의 질문인 `탐욕 선택이 전체 최적과 맞는 이유를 어떻게 설명할까?`도 결과 요약이 아니라, 상태와 순서를 어떻게 붙잡는가의 문제로 읽히게 됐다.

다음:

- 이 시리즈는 여기서 닫히지만, 다음 문제를 읽을 때도 `문제 계약 -> 첫 상태 -> fixture 검증` 순서를 그대로 재사용할 수 있다.
