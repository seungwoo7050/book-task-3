# RGB거리: 문제 계약에서 첫 구현까지

처음 절반의 역할은 “어떻게 시작했는가”를 복원하는 데 있다. 입력과 실행 경로를 먼저 잡고, 그다음 핵심 상태가 어떤 줄에서 생겼는지 차례대로 살핀다.

## 구현 순서 요약

- `problem/README.md`와 starter skeleton으로 입출력 계약을 먼저 잡는다.
- `python/src/solution.py`에서 `집 i를 색 c로 칠할 때 최소 비용을 이전 색 전이로 누적하는 DP`를 실제 상태 전이로 옮긴다.
- 첫 실행을 다시 돌려 fixture가 바로 닫히는지 확인한다.

## Phase 1
### Session 1

- 당시 목표: 문제 전문을 다시 요약하기보다, 구현을 바로 시작할 수 있는 최소 계약을 세운다.
- 변경 단위: `problem/README.md`, `problem/code/starter.py`
- 처음 가설: starter가 비어 있어도 괜찮다. 대신 `run/test` 진입점이 먼저 고정돼 있어야 구현 순서를 잃지 않는다.
- 실제 조치: `problem/README.md`의 기준 명령과 fixture 위치를 먼저 읽고, starter의 빈 `main/solve`를 실제 구현이 들어갈 자리로 잡았다.

CLI 1:

```bash
$ make -C study/Core-08-DP/1149/problem run-py
```

검증 신호:

- `96`가 그대로 나왔다.
- 첫 실행이 바로 돌아간다는 사실만으로도, 이후 구현을 어디에 붙일지 범위가 크게 줄어들었다.

핵심 코드 1:

```python
import sys

def main():
    # 할 일: 풀이를 구현한다
    pass

if __name__ == "__main__":
    main()
```

왜 이 코드가 중요했는가:

starter는 비어 있지만, 그래서 오히려 입력을 어디서 읽고 어떤 함수가 진입점이 되는지 더 또렷하게 보여 준다. 구현 전의 기준선을 남겨 두는 역할을 한다.

새로 배운 것:

- 실행 계약을 먼저 고정하면 구현 설명도 훨씬 짧고 정확해진다.

다음:

- Python 구현에서 어떤 상태와 반복이 먼저 굳었는지 본다.

## Phase 2
### Session 2

- 당시 목표: `집 i를 색 c로 칠할 때 최소 비용을 이전 색 전이로 누적하는 DP`를 Python 한 파일에서 바로 읽히는 상태 전이로 만든다.
- 변경 단위: `python/src/solution.py`
- 처음 가설: `상태와 전이를 명시적으로 정의하고 표나 배열 의미를 끝까지 유지하는 연습`라면, 핵심 자료구조와 메인 루프를 먼저 정해야 다른 분기도 자연스럽게 따라온다.
- 실제 조치: setup에서 입력과 상태를 정리하고, 중심 루프에서 전이 순서와 guard를 함께 굳혔다.

CLI 2 (직접 Python 재실행):

```bash
$ cd study/Core-08-DP/1149/problem && python3 ../python/src/solution.py < data/input1.txt
```

검증 신호:

- `96`가 그대로 나왔다.
- 이 단계의 관심사는 성능보다, 첫 구현이 fixture의 기대 출력과 곧바로 맞물리는지 확인하는 데 있었다.

핵심 코드 2:

```python
    N = int(input())
    # prev[c] = 이전 집까지 칠했을 때 마지막 색이 c인 최소 비용
    prev = list(map(int, input().split()))

    for _ in range(N - 1):
        cost = list(map(int, input().split()))
        curr = [
            cost[0] + min(prev[1], prev[2]),
```

왜 이 코드가 중요했는가:

이 구간에서 입력을 어떤 상태로 바꿔 두느냐가 뒤의 복잡도를 사실상 결정했다. `Core-08-DP` 문제들이 특히 그런 경향이 강하다.

핵심 코드 3:

```python
    for _ in range(N - 1):
        cost = list(map(int, input().split()))
        curr = [
            cost[0] + min(prev[1], prev[2]),
            cost[1] + min(prev[0], prev[2]),
            cost[2] + min(prev[0], prev[1]),
        ]
        prev = curr

    print(min(prev))
```

왜 이 코드가 중요했는가:

이 루프에서 `집 i를 색 c로 칠할 때 최소 비용을 이전 색 전이로 누적하는 DP`가 설명 문장에서 실제 전이 규칙으로 바뀐다. 구현의 무게중심이 어디였는지 가장 짧게 보여 주는 블록이다.

새로 배운 것:

- 개념 문서를 다시 읽으면서, `집 i를 색 c로 칠할 때 최소 비용을 이전 색 전이로 누적하는 DP`가 정답 공식이 아니라 상태 설계 규칙이라는 점이 또렷해졌다. 그래서 `같은 색 전이를 허용하는 실수` 같은 실수도 같은 자리에서 함께 막을 수 있었다.

다음:

- 이제 `같은 색 전이를 허용하는 실수` 같은 실수 포인트가 실제로 어디서 막히는지 fixture 전체를 돌려 확인한다.
