# 개수 세기: 문제 계약에서 첫 구현까지

처음 절반의 역할은 “어떻게 시작했는가”를 복원하는 데 있다. 입력과 실행 경로를 먼저 잡고, 그다음 핵심 상태가 어떤 줄에서 생겼는지 차례대로 살핀다.

## 구현 순서 요약

- `problem/README.md`와 starter skeleton으로 입출력 계약을 먼저 잡는다.
- `python/src/solution.py`에서 `단일 선형 스캔으로 목표 값 v의 출현 횟수를 집계`를 실제 상태 전이로 옮긴다.
- 첫 실행을 다시 돌려 fixture가 바로 닫히는지 확인한다.

## Phase 1
### Session 1

- 당시 목표: 문제 전문을 다시 요약하기보다, 구현을 바로 시작할 수 있는 최소 계약을 세운다.
- 변경 단위: `problem/README.md`, `problem/code/starter.py`
- 처음 가설: starter가 비어 있어도 괜찮다. 대신 `run/test` 진입점이 먼저 고정돼 있어야 구현 순서를 잃지 않는다.
- 실제 조치: `problem/README.md`의 기준 명령과 fixture 위치를 먼저 읽고, starter의 빈 `main/solve`를 실제 구현이 들어갈 자리로 잡았다.

CLI 1:

```bash
$ make -C study/Core-01-Array-List/10807/problem run-py
```

검증 신호:

- `3`가 그대로 나왔다.
- 첫 실행이 바로 돌아간다는 사실만으로도, 이후 구현을 어디에 붙일지 범위가 크게 줄어들었다.

핵심 코드 1:

```python
import sys
input = sys.stdin.readline

def solve():
    # 할 일: 구현한다
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

- 당시 목표: `단일 선형 스캔으로 목표 값 v의 출현 횟수를 집계`를 Python 한 파일에서 바로 읽히는 상태 전이로 만든다.
- 변경 단위: `python/src/solution.py`
- 처음 가설: `순차 자료구조를 선택하고 편집 연산의 비용 모델을 설명하는 연습`라면, 핵심 자료구조와 메인 루프를 먼저 정해야 다른 분기도 자연스럽게 따라온다.
- 실제 조치: setup에서 입력과 상태를 정리하고, 중심 루프에서 전이 순서와 guard를 함께 굳혔다.

CLI 2 (직접 Python 재실행):

```bash
$ cd study/Core-01-Array-List/10807/problem && python3 ../python/src/solution.py < data/input1.txt
```

검증 신호:

- `3`가 그대로 나왔다.
- 이 단계의 관심사는 성능보다, 첫 구현이 fixture의 기대 출력과 곧바로 맞물리는지 확인하는 데 있었다.

핵심 코드 2:

```python
    n = int(input())
    arr = list(map(int, input().split()))
    v = int(input())
    # 배열에서 v의 등장 횟수를 센다
    print(arr.count(v))

if __name__ == "__main__":
    solve()
```

왜 이 코드가 중요했는가:

이 구간에서 입력을 어떤 상태로 바꿔 두느냐가 뒤의 복잡도를 사실상 결정했다. `Core-01-Array-List` 문제들이 특히 그런 경향이 강하다.

핵심 코드 3:

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    arr = list(map(int, input().split()))
    v = int(input())
    # 배열에서 v의 등장 횟수를 센다
    print(arr.count(v))
```

왜 이 코드가 중요했는가:

핵심은 아이디어 이름이 아니라 순서다. 이 블록을 보면 왜 `입력 분리 과정에서 음수 기호를 잘못 처리하는 오류` 같은 실수가 같은 자리에서 함께 걸러지는지도 바로 드러난다.

새로 배운 것:

- 이번 구현에서 다시 확인한 건 `Array & Linear Search — Concept & Background`가 추상 설명에 머물지 않는다는 점이다. `순차 자료구조를 선택하고 편집 연산의 비용 모델을 설명하는 연습`를 코드로 옮기려면 결국 상태 이름과 순회를 먼저 고정해야 했다.

다음:

- 이제 `입력 분리 과정에서 음수 기호를 잘못 처리하는 오류` 같은 실수 포인트가 실제로 어디서 막히는지 fixture 전체를 돌려 확인한다.
