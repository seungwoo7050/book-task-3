# 수 정렬하기: 검증, edge case, 마지막 설명 축

앞 절반이 출발점이었다면, 뒷 절반은 마무리 단계다. 테스트, edge case, 개념 정리를 같은 흐름으로 묶어 이 풀이가 어디에서 안정됐는지 보여 준다.

## 구현 순서 요약

- `make -C study/Core-06-Sorting/2750/problem test`로 fixture 전체를 다시 돌린다.
- `docs/references/approach.md`의 실수 포인트를 코드 분기와 연결한다.
- `정렬 개념 정리 — 수 정렬하기`를 붙여 마지막 판단 기준을 고정한다.

## Phase 3
### Session 3

- 당시 목표: 한두 개 입력이 맞는 수준을 넘어서 fixture 전체를 통과하는 구조로 묶는다.
- 변경 단위: `problem/script/test.sh`, `docs/references/approach.md`, `docs/concepts/edge-cases.md`
- 처음 가설: 실수 포인트를 문장으로만 남기면 다시 틀리기 쉽고, 테스트 루프와 함께 봐야 실제 방어선이 보인다.
- 실제 조치: `test.sh`의 PASS/FAIL 루프와 `approach.md`의 실수 체크리스트를 나란히 읽으며, 어떤 분기가 어디를 막는지 다시 맞췄다.

CLI 1:

```bash
$ make -C study/Core-06-Sorting/2750/problem test
```

검증 신호:

- `Test 1: PASS`, `Results: 1/1 passed, 0 failed` 순서로 출력됐다.
- 이번 단계에서 특히 다시 확인한 실수 포인트는 아래 셋이었다.

- 정수 입력을 문자열로 정렬하는 실수
- 출력 개행 누락
- N줄 입력 대신 한 줄 입력 가정 오류

핵심 코드 1:

```python
import sys
input = sys.stdin.readline

def main():
    N = int(input())
    nums = [int(input()) for _ in range(N)]
    nums.sort()
    print('\n'.join(map(str, nums)))

if __name__ == "__main__":
```

왜 이 코드가 중요했는가:

이 블록을 다시 보면 `정수 입력을 문자열로 정렬하는 실수`를 막는 자리가 어디인지 바로 보인다. 테스트가 통과했다는 사실을 코드로 다시 설명하는 데 가장 적절한 증거다.

새로 배운 것:

- 테스트를 다시 읽는 순간, “맞았다”보다 “어디서 안 틀리는가”를 더 분명하게 설명할 수 있었다.

다음:

- 마지막으로 개념 문서와 코드가 어느 지점에서 맞물리는지 정리한다.

## Phase 4
### Session 4

- 당시 목표: `정렬 개념 정리 — 수 정렬하기`를 실제 코드와 연결해 마지막 설명 축을 세운다.
- 변경 단위: `docs/concepts/*.md`, `python/src/solution.py`
- 처음 가설: 마지막 글에서 남겨야 할 것은 추상 개념이 아니라, 그 개념이 꼭 필요해진 줄이다.
- 실제 조치: 마지막 출력과 guard를 다시 읽으며 개념 설명이 어느 줄을 가리키는지 고정했다.

CLI 2:

```bash
$ cd study/Core-06-Sorting/2750/problem && python3 ../python/src/solution.py < data/input1.txt
```

검증 신호:

- 마지막 확인값은 `4`, `5`였다.
- 설명용 문서가 아니라 실제 실행 결과와 같은 답이 나온다는 점이 마지막 확인 포인트였다.

핵심 코드 2:

```python
    nums = [int(input()) for _ in range(N)]
    nums.sort()
    print('\n'.join(map(str, nums)))

if __name__ == "__main__":
    main()
```

왜 이 코드가 중요했는가:

이 블록 덕분에 개념 정리가 공중에 뜨지 않는다. `정수 입력을 문자열로 정렬하는 실수`를 막는 방식과 `입력 수열을 정렬해 오름차순으로 출력하는 기본 sorting`가 여기서 한 번에 맞물린다.

핵심 코드 3:

```python
    nums = [int(input()) for _ in range(N)]
    nums.sort()
    print('\n'.join(map(str, nums)))

if __name__ == "__main__":
    main()
```

왜 이 코드가 중요했는가:

이 문제는 마지막 한 줄까지 포함해 설명이 완성된다. 출력 정리와 종료 조건이 흐리면 서사도 같이 흐려진다.

새로 배운 것:

- 마지막에 남은 교훈은 `정렬 개념 정리 — 수 정렬하기`가 별도 이론 노트가 아니라는 점이었다. 실제 구현에서는 `정수 입력을 문자열로 정렬하는 실수`를 막는 줄이 곧 개념 설명의 중심이었다.
- 그래서 `Core-06-Sorting`의 질문인 `정렬 기준과 정렬 후 후처리를 어떻게 분리할까?`도 결과 요약이 아니라, 상태와 순서를 어떻게 붙잡는가의 문제로 읽히게 됐다.

다음:

- 이 시리즈는 여기서 닫히지만, 다음 문제를 읽을 때도 `문제 계약 -> 첫 상태 -> fixture 검증` 순서를 그대로 재사용할 수 있다.
