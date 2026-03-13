# 수 찾기: 문제 계약에서 첫 구현까지

앞 절반에서는 답을 다 설명하기보다, 어디서부터 구현을 붙잡았는지 보여 주는 데 집중한다. 문제 계약을 정리한 다음 첫 상태와 핵심 루프가 어떤 순서로 굳었는지 따라가면 된다.

## 구현 순서 요약

- `problem/README.md`와 starter skeleton으로 입출력 계약을 먼저 잡는다.
- `python/src/solution.py`에서 `정렬된 배열에서 각 질의를 이분 탐색(binary search)으로 판정`를 실제 상태 전이로 옮긴다.
- 첫 실행을 다시 돌려 fixture가 바로 닫히는지 확인한다.

## Phase 1
### Session 1

- 당시 목표: 문제 전문을 다시 요약하기보다, 구현을 바로 시작할 수 있는 최소 계약을 세운다.
- 변경 단위: `problem/README.md`, `problem/code/starter.py`
- 처음 가설: starter가 비어 있어도 괜찮다. 대신 `run/test` 진입점이 먼저 고정돼 있어야 구현 순서를 잃지 않는다.
- 실제 조치: `problem/README.md`의 기준 명령과 fixture 위치를 먼저 읽고, starter의 빈 `main/solve`를 실제 구현이 들어갈 자리로 잡았다.

CLI 1:

```bash
$ make -C study/Core-07-Binary-Search-Hash/1920/problem run-py
```

검증 신호:

- 마지막 확인값은 `0`, `1`였다.
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

- 당시 목표: `정렬된 배열에서 각 질의를 이분 탐색(binary search)으로 판정`를 Python 한 파일에서 바로 읽히는 상태 전이로 만든다.
- 변경 단위: `python/src/solution.py`
- 처음 가설: `탐색 대상을 재정의하고 자료구조 또는 매개변수 탐색으로 문제를 다시 보는 연습`라면, 핵심 자료구조와 메인 루프를 먼저 정해야 다른 분기도 자연스럽게 따라온다.
- 실제 조치: setup에서 입력과 상태를 정리하고, 중심 루프에서 전이 순서와 guard를 함께 굳혔다.

CLI 2 (직접 Python 재실행):

```bash
$ cd study/Core-07-Binary-Search-Hash/1920/problem && python3 ../python/src/solution.py < data/input1.txt
```

검증 신호:

- 마지막 확인값은 `0`, `1`였다.
- 이 단계의 관심사는 성능보다, 첫 구현이 fixture의 기대 출력과 곧바로 맞물리는지 확인하는 데 있었다.

핵심 코드 2:

```python
    N = int(input())
    A = set(map(int, input().split()))
    M = int(input())
    queries = list(map(int, input().split()))

    out = []
    for q in queries:
        out.append('1' if q in A else '0')
```

왜 이 코드가 중요했는가:

이 setup에서 어떤 상태를 이름 붙였는지가 뒤의 분기 전체를 결정했다. `탐색 대상을 재정의하고 자료구조 또는 매개변수 탐색으로 문제를 다시 보는 연습`를 실제 코드로 바꿀 때 가장 먼저 굳는 것도 늘 이 부분이다.

핵심 코드 3:

```python
    for q in queries:
        out.append('1' if q in A else '0')
    print('\n'.join(out))

if __name__ == "__main__":
    main()
```

왜 이 코드가 중요했는가:

핵심은 아이디어 이름이 아니라 순서다. 이 블록을 보면 왜 `mid 업데이트에서 무한 루프` 같은 실수가 같은 자리에서 함께 걸러지는지도 바로 드러난다.

새로 배운 것:

- 이번 구현에서 다시 확인한 건 `이진 탐색 / 해시 개념 정리 — 수 찾기`가 추상 설명에 머물지 않는다는 점이다. `탐색 대상을 재정의하고 자료구조 또는 매개변수 탐색으로 문제를 다시 보는 연습`를 코드로 옮기려면 결국 상태 이름과 순회를 먼저 고정해야 했다.

다음:

- 이제 `mid 업데이트에서 무한 루프` 같은 실수 포인트가 실제로 어디서 막히는지 fixture 전체를 돌려 확인한다.
