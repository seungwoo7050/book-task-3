# 단어 정렬: 문제 계약에서 첫 구현까지

처음 절반의 역할은 “어떻게 시작했는가”를 복원하는 데 있다. 입력과 실행 경로를 먼저 잡고, 그다음 핵심 상태가 어떤 줄에서 생겼는지 차례대로 살핀다.

## 구현 순서 요약

- `problem/README.md`와 starter skeleton으로 입출력 계약을 먼저 잡는다.
- `python/src/solution.py`에서 `중복 제거 후 (길이, 사전순) 복합 키로 정렬`를 실제 상태 전이로 옮긴다.
- 첫 실행을 다시 돌려 fixture가 바로 닫히는지 확인한다.

## Phase 1
### Session 1

- 당시 목표: 문제 전문을 다시 요약하기보다, 구현을 바로 시작할 수 있는 최소 계약을 세운다.
- 변경 단위: `problem/README.md`, `problem/code/starter.py`
- 처음 가설: starter가 비어 있어도 괜찮다. 대신 `run/test` 진입점이 먼저 고정돼 있어야 구현 순서를 잃지 않는다.
- 실제 조치: `problem/README.md`의 기준 명령과 fixture 위치를 먼저 읽고, starter의 빈 `main/solve`를 실제 구현이 들어갈 자리로 잡았다.

CLI 1:

```bash
$ make -C study/Core-06-Sorting/1181/problem run-py
```

검증 신호:

- 마지막 확인값은 `cannot`, `hesitate`였다.
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

문제의 핵심 아이디어가 아직 등장하지 않아도 괜찮다. 이 빈 skeleton이 있어야 뒤의 구현이 어떤 약속 위에 올라갔는지 설명할 수 있다.

새로 배운 것:

- 실행 계약을 먼저 고정하면 구현 설명도 훨씬 짧고 정확해진다.

다음:

- Python 구현에서 어떤 상태와 반복이 먼저 굳었는지 본다.

## Phase 2
### Session 2

- 당시 목표: `중복 제거 후 (길이, 사전순) 복합 키로 정렬`를 Python 한 파일에서 바로 읽히는 상태 전이로 만든다.
- 변경 단위: `python/src/solution.py`
- 처음 가설: `정렬 기준을 설계하고, 정렬 이후의 후처리 로직을 분리해 설명하는 연습`라면, 핵심 자료구조와 메인 루프를 먼저 정해야 다른 분기도 자연스럽게 따라온다.
- 실제 조치: setup에서 입력과 상태를 정리하고, 중심 루프에서 전이 순서와 guard를 함께 굳혔다.

CLI 2 (직접 Python 재실행):

```bash
$ cd study/Core-06-Sorting/1181/problem && python3 ../python/src/solution.py < data/input1.txt
```

검증 신호:

- 마지막 확인값은 `cannot`, `hesitate`였다.
- 이 단계의 관심사는 성능보다, 첫 구현이 fixture의 기대 출력과 곧바로 맞물리는지 확인하는 데 있었다.

핵심 코드 2:

```python
    N = int(input())
    words = set(input().strip() for _ in range(N))
    # 길이 우선, 같으면 사전순으로 정렬
    result = sorted(words, key=lambda w: (len(w), w))
    print('\n'.join(result))

if __name__ == "__main__":
    main()
```

왜 이 코드가 중요했는가:

문제를 단순하게 만든 건 화려한 알고리즘 이름보다 setup였다. 어떤 값을 오래 들고 갈지 정하는 순간 `중복 제거 후 (길이, 사전순) 복합 키로 정렬`의 뼈대가 이미 보인다.

핵심 코드 3:

```python
import sys
input = sys.stdin.readline

def main():
    N = int(input())
    words = set(input().strip() for _ in range(N))
    # 길이 우선, 같으면 사전순으로 정렬
    result = sorted(words, key=lambda w: (len(w), w))
    print('\n'.join(result))
```

왜 이 코드가 중요했는가:

이 루프에서 `중복 제거 후 (길이, 사전순) 복합 키로 정렬`가 설명 문장에서 실제 전이 규칙으로 바뀐다. 구현의 무게중심이 어디였는지 가장 짧게 보여 주는 블록이다.

새로 배운 것:

- `다중 키 정렬 개념 정리 — 단어 정렬`를 다시 보니, `중복 제거 후 (길이, 사전순) 복합 키로 정렬`의 핵심은 아이디어를 많이 추가하는 데 있지 않았다. `중복 제거 시 입력 순서 보존을 잘못 기대하는 문제`를 피할 수 있는 상태를 먼저 정하는 쪽이 더 중요했다.

다음:

- 이제 `중복 제거 시 입력 순서 보존을 잘못 기대하는 문제` 같은 실수 포인트가 실제로 어디서 막히는지 fixture 전체를 돌려 확인한다.
