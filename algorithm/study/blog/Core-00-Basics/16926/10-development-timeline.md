# 배열 돌리기 1: 문제 계약에서 첫 구현까지

처음 절반의 역할은 “어떻게 시작했는가”를 복원하는 데 있다. 입력과 실행 경로를 먼저 잡고, 그다음 핵심 상태가 어떤 줄에서 생겼는지 차례대로 살핀다.

## 구현 순서 요약

- `problem/README.md`와 starter skeleton으로 입출력 계약을 먼저 잡는다.
- `python/src/solution.py`에서 `레이어 분해(layer decomposition) 후 각 테두리를 독립적으로 회전`를 실제 상태 전이로 옮긴다.
- 첫 실행을 다시 돌려 fixture가 바로 닫히는지 확인한다.

## Phase 1
### Session 1

- 당시 목표: 문제 전문을 다시 요약하기보다, 구현을 바로 시작할 수 있는 최소 계약을 세운다.
- 변경 단위: `problem/README.md`, `problem/code/starter.py`
- 처음 가설: starter가 비어 있어도 괜찮다. 대신 `run/test` 진입점이 먼저 고정돼 있어야 구현 순서를 잃지 않는다.
- 실제 조치: `problem/README.md`의 기준 명령과 fixture 위치를 먼저 읽고, starter의 빈 `main/solve`를 실제 구현이 들어갈 자리로 잡았다.

CLI 1:

```bash
$ make -C study/Core-00-Basics/16926/problem run-py
```

검증 신호:

- `3 4 8 12`, `2 11 10 16`, `1 7 6 15`, `5 9 13 14` 순서로 출력됐다.
- 첫 실행이 바로 돌아간다는 사실만으로도, 이후 구현을 어디에 붙일지 범위가 크게 줄어들었다.

핵심 코드 1:

```python
import sys
input = sys.stdin.readline

def solve():
    # 할 일: N, M, R과 배열을 읽는다
    # 할 일: 레이어로 분해하고 각 레이어를 회전한 뒤 다시 조립한다
    pass

if __name__ == "__main__":
    solve()
```

왜 이 코드가 중요했는가:

알고리즘은 아직 없지만 실행 계약은 이미 여기서 시작한다. 나중에 서사를 복원할 때도 이 빈 골격이 첫 기준점이 된다.

새로 배운 것:

- 실행 계약을 먼저 고정하면 구현 설명도 훨씬 짧고 정확해진다.

다음:

- Python 구현에서 어떤 상태와 반복이 먼저 굳었는지 본다.

## Phase 2
### Session 2

- 당시 목표: `레이어 분해(layer decomposition) 후 각 테두리를 독립적으로 회전`를 Python 한 파일에서 바로 읽히는 상태 전이로 만든다.
- 변경 단위: `python/src/solution.py`
- 처음 가설: `작은 입력을 안정적으로 읽고, 조건 분기를 코드와 문서로 함께 정리하는 감각`라면, 핵심 자료구조와 메인 루프를 먼저 정해야 다른 분기도 자연스럽게 따라온다.
- 실제 조치: setup에서 입력과 상태를 정리하고, 중심 루프에서 전이 순서와 guard를 함께 굳혔다.

CLI 2 (직접 Python 재실행):

```bash
$ cd study/Core-00-Basics/16926/problem && python3 ../python/src/solution.py < data/input2.txt
```

검증 신호:

- `2 3 4 8`, `1 7 11 12`, `5 6 10 16`, `9 13 14 15` 순서로 출력됐다.
- 이 단계의 관심사는 성능보다, 첫 구현이 fixture의 기대 출력과 곧바로 맞물리는지 확인하는 데 있었다.

핵심 코드 2:

```python
    N, M, R = map(int, input().split())
    arr = [list(map(int, input().split())) for _ in range(N)]

    layers = min(N, M) // 2

    for k in range(layers):
        # k번째 레이어를 1차원 리스트로 펼친다(시계 방향 순회)
        ring = []
```

왜 이 코드가 중요했는가:

이 구간에서 입력을 어떤 상태로 바꿔 두느냐가 뒤의 복잡도를 사실상 결정했다. `Core-00-Basics` 문제들이 특히 그런 경향이 강하다.

핵심 코드 3:

```python
    for k in range(layers):
        # k번째 레이어를 1차원 리스트로 펼친다(시계 방향 순회)
        ring = []
        # 윗줄: left에서 right까지
        for j in range(k, M - k):
            ring.append(arr[k][j])
        # 오른쪽 열: top+1에서 bottom까지
        for i in range(k + 1, N - k):
            ring.append(arr[i][M - 1 - k])
        # 아랫줄: right-1에서 left까지
```

왜 이 코드가 중요했는가:

이 부분이 풀리면서 문제는 훨씬 단순해졌다. `레이어 분해(layer decomposition) 후 각 테두리를 독립적으로 회전`를 지키는 데 필요한 반복 순서와 guard가 이 블록 안에서 같이 정리되기 때문이다.

새로 배운 것:

- 이번 구현에서 다시 확인한 건 `Layer Decomposition — Concept & Background`가 추상 설명에 머물지 않는다는 점이다. `작은 입력을 안정적으로 읽고, 조건 분기를 코드와 문서로 함께 정리하는 감각`를 코드로 옮기려면 결국 상태 이름과 순회를 먼저 고정해야 했다.

다음:

- 이제 `레이어 길이 계산에서 코너를 중복 포함하는 오류` 같은 실수 포인트가 실제로 어디서 막히는지 fixture 전체를 돌려 확인한다.
