# 카드2: 검증, edge case, 마지막 설명 축

앞 절반이 출발점이었다면, 뒷 절반은 마무리 단계다. 테스트, edge case, 개념 정리를 같은 흐름으로 묶어 이 풀이가 어디에서 안정됐는지 보여 준다.

## 구현 순서 요약

- `make -C study/Core-02-Stack-Queue/2164/problem test`로 fixture 전체를 다시 돌린다.
- `docs/references/approach.md`의 실수 포인트를 코드 분기와 연결한다.
- `큐(Queue) 개념 정리 — Card2`를 붙여 마지막 판단 기준을 고정한다.

## Phase 3
### Session 3

- 당시 목표: 한두 개 입력이 맞는 수준을 넘어서 fixture 전체를 통과하는 구조로 묶는다.
- 변경 단위: `problem/script/test.sh`, `docs/references/approach.md`, `docs/concepts/edge-cases.md`
- 처음 가설: 실수 포인트를 문장으로만 남기면 다시 틀리기 쉽고, 테스트 루프와 함께 봐야 실제 방어선이 보인다.
- 실제 조치: `test.sh`의 PASS/FAIL 루프와 `approach.md`의 실수 체크리스트를 나란히 읽으며, 어떤 분기가 어디를 막는지 다시 맞췄다.

CLI 1:

```bash
$ make -C study/Core-02-Stack-Queue/2164/problem test
```

검증 신호:

- `Test 1: PASS`, `Results: 1/1 passed, 0 failed` 순서로 출력됐다.
- 이번 단계에서 특히 다시 확인한 실수 포인트는 아래 셋이었다.

- 카드 1장 케이스 예외 처리 누락
- remove/append 순서 반전으로 오답
- while 조건을 잘못 잡아 마지막 카드 이전에 종료

핵심 코드 1:

```python
    while len(q) > 1:
        q.popleft()          # 맨 위 카드를 버린다
        q.append(q.popleft()) # 다음 카드를 맨 아래로 보낸다

    print(q[0])

if __name__ == "__main__":
    solve()
```

왜 이 코드가 중요했는가:

검증의 핵심은 통과 여부보다 방어선의 위치를 확인하는 데 있다. 이 블록은 어떤 분기가 edge case를 실제로 막아 주는지 보여 준다.

새로 배운 것:

- 테스트를 다시 읽는 순간, “맞았다”보다 “어디서 안 틀리는가”를 더 분명하게 설명할 수 있었다.

다음:

- 마지막으로 개념 문서와 코드가 어느 지점에서 맞물리는지 정리한다.

## Phase 4
### Session 4

- 당시 목표: `큐(Queue) 개념 정리 — Card2`를 실제 코드와 연결해 마지막 설명 축을 세운다.
- 변경 단위: `docs/concepts/*.md`, `python/src/solution.py`
- 처음 가설: 마지막 글에서 남겨야 할 것은 추상 개념이 아니라, 그 개념이 꼭 필요해진 줄이다.
- 실제 조치: 마지막 출력과 guard를 다시 읽으며 개념 설명이 어느 줄을 가리키는지 고정했다.

CLI 2:

```bash
$ cd study/Core-02-Stack-Queue/2164/problem && python3 ../python/src/solution.py < data/input1.txt
```

검증 신호:

- `4`가 그대로 나왔다.
- 설명용 문서가 아니라 실제 실행 결과와 같은 답이 나온다는 점이 마지막 확인 포인트였다.

핵심 코드 2:

```python
        q.append(q.popleft()) # 다음 카드를 맨 아래로 보낸다

    print(q[0])

if __name__ == "__main__":
    solve()
```

왜 이 코드가 중요했는가:

여기서는 `큐(Queue) 개념 정리 — Card2`가 별도 해설이 아니라는 점이 분명해진다. `큐에서 앞 원소 제거 후 다음 원소를 뒤로 보내는 카드 시뮬레이션`를 끝까지 지키는 데 필요한 최소 단위가 바로 이 블록에 남아 있다.

핵심 코드 3:

```python
        q.append(q.popleft()) # 다음 카드를 맨 아래로 보낸다

    print(q[0])

if __name__ == "__main__":
    solve()
```

왜 이 코드가 중요했는가:

끝을 어떻게 닫느냐가 생각보다 중요했다. `카드2`에서는 마지막 출력 정리가 구현의 완성도를 가장 직접적으로 드러냈다.

새로 배운 것:

- `큐(Queue) 개념 정리 — Card2`를 다시 읽고 나니, 이 문제의 핵심은 `큐에서 앞 원소 제거 후 다음 원소를 뒤로 보내는 카드 시뮬레이션`를 끝까지 흔들리지 않게 유지하는 데 있었다.
- 그래서 `Core-02-Stack-Queue`의 질문인 `명령 규칙을 LIFO/FIFO/덱 모델로 어떻게 옮길까?`도 결과 요약이 아니라, 상태와 순서를 어떻게 붙잡는가의 문제로 읽히게 됐다.

다음:

- 이 시리즈는 여기서 닫히지만, 다음 문제를 읽을 때도 `문제 계약 -> 첫 상태 -> fixture 검증` 순서를 그대로 재사용할 수 있다.
