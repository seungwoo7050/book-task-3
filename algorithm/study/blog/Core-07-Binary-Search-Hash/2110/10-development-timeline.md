# 공유기 설치: 문제 계약에서 첫 구현까지

앞 절반에서는 답을 다 설명하기보다, 어디서부터 구현을 붙잡았는지 보여 주는 데 집중한다. 문제 계약을 정리한 다음 첫 상태와 핵심 루프가 어떤 순서로 굳었는지 따라가면 된다.

## 구현 순서 요약

- `problem/README.md`와 starter skeleton으로 입출력 계약을 먼저 잡는다.
- `python/src/solution.py`에서 `거리 D에 대한 가능성 판정을 이분 탐색하는 parametric search`를 실제 상태 전이로 옮긴다.
- 첫 실행을 다시 돌려 fixture가 바로 닫히는지 확인한다.

## Phase 1
### Session 1

- 당시 목표: 문제 전문을 다시 요약하기보다, 구현을 바로 시작할 수 있는 최소 계약을 세운다.
- 변경 단위: `problem/README.md`, `problem/code/starter.py`
- 처음 가설: starter가 비어 있어도 괜찮다. 대신 `run/test` 진입점이 먼저 고정돼 있어야 구현 순서를 잃지 않는다.
- 실제 조치: `problem/README.md`의 기준 명령과 fixture 위치를 먼저 읽고, starter의 빈 `main/solve`를 실제 구현이 들어갈 자리로 잡았다.

CLI 1:

```bash
$ make -C study/Core-07-Binary-Search-Hash/2110/problem run-py
```

검증 신호:

- `3`가 그대로 나왔다.
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

알고리즘은 아직 없지만 실행 계약은 이미 여기서 시작한다. 나중에 서사를 복원할 때도 이 빈 골격이 첫 기준점이 된다.

새로 배운 것:

- 실행 계약을 먼저 고정하면 구현 설명도 훨씬 짧고 정확해진다.

다음:

- Python 구현에서 어떤 상태와 반복이 먼저 굳었는지 본다.

## Phase 2
### Session 2

- 당시 목표: `거리 D에 대한 가능성 판정을 이분 탐색하는 parametric search`를 Python 한 파일에서 바로 읽히는 상태 전이로 만든다.
- 변경 단위: `python/src/solution.py`
- 처음 가설: `탐색 대상을 재정의하고 자료구조 또는 매개변수 탐색으로 문제를 다시 보는 연습`라면, 핵심 자료구조와 메인 루프를 먼저 정해야 다른 분기도 자연스럽게 따라온다.
- 실제 조치: setup에서 입력과 상태를 정리하고, 중심 루프에서 전이 순서와 guard를 함께 굳혔다.

CLI 2 (비교 구현 실행):

```bash
$ make -C study/Core-07-Binary-Search-Hash/2110/problem run-cpp
```

검증 신호:

- `3`가 그대로 나왔다.
- 이 단계의 관심사는 성능보다, 첫 구현이 fixture의 기대 출력과 곧바로 맞물리는지 확인하는 데 있었다.

핵심 코드 2:

```python
    N, C = map(int, input().split())
    houses = sorted(int(input()) for _ in range(N))

    def feasible(d):
        """Can we place C routers with min distance >= d?"""
        count = 1
        last = houses[0]
        for i in range(1, N):
```

왜 이 코드가 중요했는가:

문제를 단순하게 만든 건 화려한 알고리즘 이름보다 setup였다. 어떤 값을 오래 들고 갈지 정하는 순간 `거리 D에 대한 가능성 판정을 이분 탐색하는 parametric search`의 뼈대가 이미 보인다.

핵심 코드 3:

```python
        for i in range(1, N):
            if houses[i] - last >= d:
                count += 1
                last = houses[i]
                if count >= C:
                    return True
        return False

    lo, hi, ans = 1, houses[-1] - houses[0], 0
    while lo <= hi:
```

왜 이 코드가 중요했는가:

이 부분이 풀리면서 문제는 훨씬 단순해졌다. `거리 D에 대한 가능성 판정을 이분 탐색하는 parametric search`를 지키는 데 필요한 반복 순서와 guard가 이 블록 안에서 같이 정리되기 때문이다.

새로 배운 것:

- 개념 문서를 다시 읽으면서, `거리 D에 대한 가능성 판정을 이분 탐색하는 parametric search`가 정답 공식이 아니라 상태 설계 규칙이라는 점이 또렷해졌다. 그래서 `mid 갱신 시 lo/hi 경계 처리 오류` 같은 실수도 같은 자리에서 함께 막을 수 있었다.

다음:

- 이제 `mid 갱신 시 lo/hi 경계 처리 오류` 같은 실수 포인트가 실제로 어디서 막히는지 fixture 전체를 돌려 확인한다.
