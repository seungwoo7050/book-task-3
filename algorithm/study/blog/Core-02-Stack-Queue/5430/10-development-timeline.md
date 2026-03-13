# AC: 문제 계약에서 첫 구현까지

이 문서의 초점은 정답 설명보다 출발점이다. `Phase 1`에서 실행 계약을 세우고, `Phase 2`에서 그 계약이 어떤 상태와 루프로 바뀌는지 이어서 본다.

## 구현 순서 요약

- `problem/README.md`와 starter skeleton으로 입출력 계약을 먼저 잡는다.
- `python/src/solution.py`에서 `함수 문자열을 reverse flag + deque 양끝 제거로 lazy evaluation`를 실제 상태 전이로 옮긴다.
- 첫 실행을 다시 돌려 fixture가 바로 닫히는지 확인한다.

## Phase 1
### Session 1

- 당시 목표: 문제 전문을 다시 요약하기보다, 구현을 바로 시작할 수 있는 최소 계약을 세운다.
- 변경 단위: `problem/README.md`, `problem/code/starter.py`
- 처음 가설: starter가 비어 있어도 괜찮다. 대신 `run/test` 진입점이 먼저 고정돼 있어야 구현 순서를 잃지 않는다.
- 실제 조치: `problem/README.md`의 기준 명령과 fixture 위치를 먼저 읽고, starter의 빈 `main/solve`를 실제 구현이 들어갈 자리로 잡았다.

CLI 1:

```bash
$ make -C study/Core-02-Stack-Queue/5430/problem run-py
```

검증 신호:

- `[2,1]`, `error`, `[1,2,3,5,8]`, `error` 순서로 출력됐다.
- 첫 실행이 바로 돌아간다는 사실만으로도, 이후 구현을 어디에 붙일지 범위가 크게 줄어들었다.

핵심 코드 1:

```python
import sys
input = sys.stdin.readline
def solve():
    pass
if __name__ == "__main__":
    solve()
```

왜 이 코드가 중요했는가:

문제의 핵심 아이디어가 아직 등장하지 않아도 괜찮다. 이 빈 skeleton이 있어야 뒤의 구현이 어떤 약속 위에 올라갔는지 설명할 수 있다.

새로 배운 것:

- 실행 계약을 먼저 고정하면 구현 설명도 훨씬 짧고 정확해진다.

다음:

- Python 구현에서 어떤 상태와 반복이 먼저 굳었는지 본다.

## Phase 2
### Session 2

- 당시 목표: `함수 문자열을 reverse flag + deque 양끝 제거로 lazy evaluation`를 Python 한 파일에서 바로 읽히는 상태 전이로 만든다.
- 변경 단위: `python/src/solution.py`
- 처음 가설: `명령 기반 자료구조 문제를 상태 전이 규칙으로 정리하는 연습`라면, 핵심 자료구조와 메인 루프를 먼저 정해야 다른 분기도 자연스럽게 따라온다.
- 실제 조치: setup에서 입력과 상태를 정리하고, 중심 루프에서 전이 순서와 guard를 함께 굳혔다.

CLI 2 (비교 구현 실행):

```bash
$ make -C study/Core-02-Stack-Queue/5430/problem run-cpp
```

검증 신호:

- `[2,1]`, `error`, `[1,2,3,5,8]`, `error` 순서로 출력됐다.
- 이 단계의 관심사는 성능보다, 첫 구현이 fixture의 기대 출력과 곧바로 맞물리는지 확인하는 데 있었다.

핵심 코드 2:

```python
    t = int(sys.stdin.readline())
    for _ in range(t):
        p = sys.stdin.readline().strip()
        n = int(sys.stdin.readline())
        arr_str = sys.stdin.readline().strip()

        # `[x1,x2,...,xn]` 배열 문자열을 파싱
        if n == 0:
```

왜 이 코드가 중요했는가:

문제를 단순하게 만든 건 화려한 알고리즘 이름보다 setup였다. 어떤 값을 오래 들고 갈지 정하는 순간 `함수 문자열을 reverse flag + deque 양끝 제거로 lazy evaluation`의 뼈대가 이미 보인다.

핵심 코드 3:

```python
    for _ in range(t):
        p = sys.stdin.readline().strip()
        n = int(sys.stdin.readline())
        arr_str = sys.stdin.readline().strip()

        # `[x1,x2,...,xn]` 배열 문자열을 파싱
        if n == 0:
            dq = deque()
        else:
            dq = deque(arr_str[1:-1].split(','))
```

왜 이 코드가 중요했는가:

핵심은 아이디어 이름이 아니라 순서다. 이 블록을 보면 왜 `빈 배열에서 D 실행 시 error 처리 누락` 같은 실수가 같은 자리에서 함께 걸러지는지도 바로 드러난다.

새로 배운 것:

- 개념 문서를 다시 읽으면서, `함수 문자열을 reverse flag + deque 양끝 제거로 lazy evaluation`가 정답 공식이 아니라 상태 설계 규칙이라는 점이 또렷해졌다. 그래서 `빈 배열에서 D 실행 시 error 처리 누락` 같은 실수도 같은 자리에서 함께 막을 수 있었다.

다음:

- 이제 `빈 배열에서 D 실행 시 error 처리 누락` 같은 실수 포인트가 실제로 어디서 막히는지 fixture 전체를 돌려 확인한다.
