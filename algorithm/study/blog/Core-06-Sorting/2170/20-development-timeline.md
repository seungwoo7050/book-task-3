# 선 긋기: 검증, edge case, 마지막 설명 축

뒷 절반에서는 “왜 맞는가”를 더 조밀하게 확인한다. fixture 전체를 다시 돌려 실수 포인트를 묶고, 마지막에는 개념 문서와 코드가 정확히 어디서 맞물리는지 정리한다.

## 구현 순서 요약

- `make -C study/Core-06-Sorting/2170/problem test`로 fixture 전체를 다시 돌린다.
- `docs/references/approach.md`의 실수 포인트를 코드 분기와 연결한다.
- `구간 병합(Interval Merge) 개념 정리 — 선 긋기`와 `cpp/src/solution.cpp`를 붙여 마지막 판단 기준을 고정한다.

## Phase 3
### Session 3

- 당시 목표: 한두 개 입력이 맞는 수준을 넘어서 fixture 전체를 통과하는 구조로 묶는다.
- 변경 단위: `problem/script/test.sh`, `docs/references/approach.md`, `docs/concepts/edge-cases.md`
- 처음 가설: 실수 포인트를 문장으로만 남기면 다시 틀리기 쉽고, 테스트 루프와 함께 봐야 실제 방어선이 보인다.
- 실제 조치: `test.sh`의 PASS/FAIL 루프와 `approach.md`의 실수 체크리스트를 나란히 읽으며, 어떤 분기가 어디를 막는지 다시 맞췄다.

CLI 1:

```bash
$ make -C study/Core-06-Sorting/2170/problem test
```

검증 신호:

- `Test 1: PASS`, `Results: 1/1 passed, 0 failed` 순서로 출력됐다.
- 이번 단계에서 특히 다시 확인한 실수 포인트는 아래 셋이었다.

- 끝점 포함/배타 해석 혼동
- 현재 병합 구간 업데이트 순서 오류
- 정렬 키를 끝점으로만 두어 오동작

핵심 코드 1:

```python
    for s, e in segments[1:]:
        if s <= cur_end:
            # 겹치거나 맞닿으면 현재 구간을 늘린다
            cur_end = max(cur_end, e)
        else:
            # 빈 구간이 생기면 현재 구간을 확정한다
            total += cur_end - cur_start
            cur_start, cur_end = s, e

    # 마지막 구간을 더한다.
```

왜 이 코드가 중요했는가:

검증의 핵심은 통과 여부보다 방어선의 위치를 확인하는 데 있다. 이 블록은 어떤 분기가 edge case를 실제로 막아 주는지 보여 준다.

새로 배운 것:

- 테스트를 다시 읽는 순간, “맞았다”보다 “어디서 안 틀리는가”를 더 분명하게 설명할 수 있었다.

다음:

- 마지막으로 개념 문서와 코드가 어느 지점에서 맞물리는지 정리한다.

## Phase 4
### Session 4

- 당시 목표: `구간 병합(Interval Merge) 개념 정리 — 선 긋기`를 실제 코드와 연결해 마지막 설명 축을 세운다.
- 변경 단위: `cpp/src/solution.cpp`, `docs/concepts/*.md`, `python/src/solution.py`
- 처음 가설: 마지막 글에서 남겨야 할 것은 추상 개념이 아니라, 그 개념이 꼭 필요해진 줄이다.
- 실제 조치: Python과 C++ 구현을 나란히 읽으며 같은 전이가 유지되는지 확인했다.

CLI 2:

```bash
$ make -C study/Core-06-Sorting/2170/problem run-cpp
```

검증 신호:

- `5`가 그대로 나왔다.
- 설명용 문서가 아니라 실제 실행 결과와 같은 답이 나온다는 점이 마지막 확인 포인트였다.

핵심 코드 2:

```cpp
    for(int i = 0; i < N; i++) cin >> seg[i].first >> seg[i].second;
    sort(seg.begin(), seg.end());

    long long total = 0;
    int curS = seg[0].first, curE = seg[0].second;

    for(int i = 1; i < N; i++){
        if(seg[i].first <= curE){
            curE = max(curE, seg[i].second);
        } else {
```

왜 이 코드가 중요했는가:

마지막 전환점은 이 코드였다. `구간 병합(Interval Merge) 개념 정리 — 선 긋기`를 붙여 읽으면, 왜 이 문제의 설명이 결국 이 줄로 수렴하는지 자연스럽게 보인다.

핵심 코드 3:

```python
    # 마지막 구간을 더한다.
    total += cur_end - cur_start
    print(total)

if __name__ == "__main__":
    main()
```

왜 이 코드가 중요했는가:

끝을 어떻게 닫느냐가 생각보다 중요했다. `선 긋기`에서는 마지막 출력 정리가 구현의 완성도를 가장 직접적으로 드러냈다.

새로 배운 것:

- C++ 쪽까지 다시 확인하고 나니, 이 문제에서 중요한 건 표현 방식이 아니라 `구간을 시작점 기준 정렬 후 병합해 총 길이 계산`를 끝까지 보존하는 전이 순서라는 점이었다.
- 그래서 `Core-06-Sorting`의 질문인 `정렬 기준과 정렬 후 후처리를 어떻게 분리할까?`도 결과 요약이 아니라, 상태와 순서를 어떻게 붙잡는가의 문제로 읽히게 됐다.

다음:

- 이 시리즈는 여기서 닫히지만, 다음 문제를 읽을 때도 `문제 계약 -> 첫 상태 -> fixture 검증` 순서를 그대로 재사용할 수 있다.
