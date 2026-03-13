# 회의실 배정: 검증, edge case, 마지막 설명 축

이제는 구현을 끝냈다고 말하는 단계가 아니라, 어떤 근거로 끝났다고 말할 수 있는지를 정리하는 단계다. 테스트 루프와 마지막 설명 축이 여기서 닫힌다.

## 구현 순서 요약

- `make -C study/Core-09-Greedy/1931/problem test`로 fixture 전체를 다시 돌린다.
- `docs/references/approach.md`의 실수 포인트를 코드 분기와 연결한다.
- `활동 선택 문제 개념 정리 — 회의실 배정`를 붙여 마지막 판단 기준을 고정한다.

## Phase 3
### Session 3

- 당시 목표: 한두 개 입력이 맞는 수준을 넘어서 fixture 전체를 통과하는 구조로 묶는다.
- 변경 단위: `problem/script/test.sh`, `docs/references/approach.md`, `docs/concepts/edge-cases.md`
- 처음 가설: 실수 포인트를 문장으로만 남기면 다시 틀리기 쉽고, 테스트 루프와 함께 봐야 실제 방어선이 보인다.
- 실제 조치: `test.sh`의 PASS/FAIL 루프와 `approach.md`의 실수 체크리스트를 나란히 읽으며, 어떤 분기가 어디를 막는지 다시 맞췄다.

CLI 1:

```bash
$ make -C study/Core-09-Greedy/1931/problem test
```

검증 신호:

- `Test 1: PASS`, `Results: 1/1 passed, 0 failed` 순서로 출력됐다.
- 이번 단계에서 특히 다시 확인한 실수 포인트는 아래 셋이었다.

- 종료 시간 tie-breaker(시작 시간) 누락
- 선택 가능 조건을 >로 둬서 경계 누락
- 정렬 후 첫 회의 초기화 누락

핵심 코드 1:

```python
    for start, end in meetings:
        if start >= last_end:
            count += 1
            last_end = end

    print(count)

if __name__ == "__main__":
    main()
```

왜 이 코드가 중요했는가:

이 코드는 정답을 만드는 줄이면서 동시에 체크리스트를 만족시키는 줄이다. 그래서 `approach.md`의 실수 포인트와 가장 잘 연결된다.

새로 배운 것:

- 테스트를 다시 읽는 순간, “맞았다”보다 “어디서 안 틀리는가”를 더 분명하게 설명할 수 있었다.

다음:

- 마지막으로 개념 문서와 코드가 어느 지점에서 맞물리는지 정리한다.

## Phase 4
### Session 4

- 당시 목표: `활동 선택 문제 개념 정리 — 회의실 배정`를 실제 코드와 연결해 마지막 설명 축을 세운다.
- 변경 단위: `docs/concepts/*.md`, `python/src/solution.py`
- 처음 가설: 마지막 글에서 남겨야 할 것은 추상 개념이 아니라, 그 개념이 꼭 필요해진 줄이다.
- 실제 조치: 마지막 출력과 guard를 다시 읽으며 개념 설명이 어느 줄을 가리키는지 고정했다.

CLI 2:

```bash
$ cd study/Core-09-Greedy/1931/problem && python3 ../python/src/solution.py < data/input1.txt
```

검증 신호:

- `4`가 그대로 나왔다.
- 설명용 문서가 아니라 실제 실행 결과와 같은 답이 나온다는 점이 마지막 확인 포인트였다.

핵심 코드 2:

```python
            last_end = end

    print(count)

if __name__ == "__main__":
    main()
```

왜 이 코드가 중요했는가:

여기서는 `활동 선택 문제 개념 정리 — 회의실 배정`가 별도 해설이 아니라는 점이 분명해진다. `종료 시간 우선 정렬 후 가능한 회의를 순차 선택하는 activity selection`를 끝까지 지키는 데 필요한 최소 단위가 바로 이 블록에 남아 있다.

핵심 코드 3:

```python
            last_end = end

    print(count)

if __name__ == "__main__":
    main()
```

왜 이 코드가 중요했는가:

이 문제는 마지막 한 줄까지 포함해 설명이 완성된다. 출력 정리와 종료 조건이 흐리면 서사도 같이 흐려진다.

새로 배운 것:

- `활동 선택 문제 개념 정리 — 회의실 배정`를 다시 읽고 나니, 이 문제의 핵심은 `종료 시간 우선 정렬 후 가능한 회의를 순차 선택하는 activity selection`를 끝까지 흔들리지 않게 유지하는 데 있었다.
- 그래서 `Core-09-Greedy`의 질문인 `탐욕 선택이 전체 최적과 맞는 이유를 어떻게 설명할까?`도 결과 요약이 아니라, 상태와 순서를 어떻게 붙잡는가의 문제로 읽히게 됐다.

다음:

- 이 시리즈는 여기서 닫히지만, 다음 문제를 읽을 때도 `문제 계약 -> 첫 상태 -> fixture 검증` 순서를 그대로 재사용할 수 있다.
