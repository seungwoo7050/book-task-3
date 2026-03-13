# 숫자 카드 2: 검증, edge case, 마지막 설명 축

뒷 절반에서는 “왜 맞는가”를 더 조밀하게 확인한다. fixture 전체를 다시 돌려 실수 포인트를 묶고, 마지막에는 개념 문서와 코드가 정확히 어디서 맞물리는지 정리한다.

## 구현 순서 요약

- `make -C study/Core-07-Binary-Search-Hash/10816/problem test`로 fixture 전체를 다시 돌린다.
- `docs/references/approach.md`의 실수 포인트를 코드 분기와 연결한다.
- `Counter / 해시맵 개념 정리 — 숫자 카드 2`를 붙여 마지막 판단 기준을 고정한다.

## Phase 3
### Session 3

- 당시 목표: 한두 개 입력이 맞는 수준을 넘어서 fixture 전체를 통과하는 구조로 묶는다.
- 변경 단위: `problem/script/test.sh`, `docs/references/approach.md`, `docs/concepts/edge-cases.md`
- 처음 가설: 실수 포인트를 문장으로만 남기면 다시 틀리기 쉽고, 테스트 루프와 함께 봐야 실제 방어선이 보인다.
- 실제 조치: `test.sh`의 PASS/FAIL 루프와 `approach.md`의 실수 체크리스트를 나란히 읽으며, 어떤 분기가 어디를 막는지 다시 맞췄다.

CLI 1:

```bash
$ make -C study/Core-07-Binary-Search-Hash/10816/problem test
```

검증 신호:

- `Test 1: PASS`, `Results: 1/1 passed, 0 failed` 순서로 출력됐다.
- 이번 단계에서 특히 다시 확인한 실수 포인트는 아래 셋이었다.

- 기본값 0 처리 누락(KeyError)
- 입출력 버퍼링 누락
- 질의 순서대로 출력하지 않는 문제

핵심 코드 1:

```python
import sys
from collections import Counter
input = sys.stdin.readline

def main():
    N = int(input())
    cards = list(map(int, input().split()))
    M = int(input())
    queries = list(map(int, input().split()))
```

왜 이 코드가 중요했는가:

검증의 핵심은 통과 여부보다 방어선의 위치를 확인하는 데 있다. 이 블록은 어떤 분기가 edge case를 실제로 막아 주는지 보여 준다.

새로 배운 것:

- 테스트를 다시 읽는 순간, “맞았다”보다 “어디서 안 틀리는가”를 더 분명하게 설명할 수 있었다.

다음:

- 마지막으로 개념 문서와 코드가 어느 지점에서 맞물리는지 정리한다.

## Phase 4
### Session 4

- 당시 목표: `Counter / 해시맵 개념 정리 — 숫자 카드 2`를 실제 코드와 연결해 마지막 설명 축을 세운다.
- 변경 단위: `docs/concepts/*.md`, `python/src/solution.py`
- 처음 가설: 마지막 글에서 남겨야 할 것은 추상 개념이 아니라, 그 개념이 꼭 필요해진 줄이다.
- 실제 조치: 마지막 출력과 guard를 다시 읽으며 개념 설명이 어느 줄을 가리키는지 고정했다.

CLI 2:

```bash
$ cd study/Core-07-Binary-Search-Hash/10816/problem && python3 ../python/src/solution.py < data/input1.txt
```

검증 신호:

- `3 0 0 1 2 0 0 2`가 그대로 나왔다.
- 설명용 문서가 아니라 실제 실행 결과와 같은 답이 나온다는 점이 마지막 확인 포인트였다.

핵심 코드 2:

```python
    cnt = Counter(cards)
    print(' '.join(str(cnt[q]) for q in queries))

if __name__ == "__main__":
    main()
```

왜 이 코드가 중요했는가:

이 블록 덕분에 개념 정리가 공중에 뜨지 않는다. `기본값 0 처리 누락(KeyError)`를 막는 방식과 `빈도 해시맵(counter)으로 카드 개수를 누적하고 질의별 출력`가 여기서 한 번에 맞물린다.

핵심 코드 3:

```python
    cnt = Counter(cards)
    print(' '.join(str(cnt[q]) for q in queries))

if __name__ == "__main__":
    main()
```

왜 이 코드가 중요했는가:

마지막 출력과 종료 조건은 사소해 보여도 최종 출력까지 닫는 부분이다. `숫자 카드 2`도 이 구간이 흐려지면 첫 구현은 맞아 보여도 최종 설명이 흔들린다.

새로 배운 것:

- 이 프로젝트를 다시 정리하면서, `Counter / 해시맵 개념 정리 — 숫자 카드 2`에서 말한 원리가 결국 `빈도 해시맵(counter)으로 카드 개수를 누적하고 질의별 출력` 한 줄로 수렴한다는 점이 선명해졌다.
- 그래서 `Core-07-Binary-Search-Hash`의 질문인 `탐색 대상을 어떻게 재정의해 선형 탐색을 벗어날까?`도 결과 요약이 아니라, 상태와 순서를 어떻게 붙잡는가의 문제로 읽히게 됐다.

다음:

- 이 시리즈는 여기서 닫히지만, 다음 문제를 읽을 때도 `문제 계약 -> 첫 상태 -> fixture 검증` 순서를 그대로 재사용할 수 있다.
