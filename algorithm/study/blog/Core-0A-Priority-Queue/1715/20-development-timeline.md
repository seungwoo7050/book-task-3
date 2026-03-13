# 카드 정렬하기: 검증, edge case, 마지막 설명 축

뒷 절반에서는 “왜 맞는가”를 더 조밀하게 확인한다. fixture 전체를 다시 돌려 실수 포인트를 묶고, 마지막에는 개념 문서와 코드가 정확히 어디서 맞물리는지 정리한다.

## 구현 순서 요약

- `make -C study/Core-0A-Priority-Queue/1715/problem test`로 fixture 전체를 다시 돌린다.
- `docs/references/approach.md`의 실수 포인트를 코드 분기와 연결한다.
- `카드 합치기 개념 정리 — 허프만 코딩 패턴`와 `cpp/src/solution.cpp`를 붙여 마지막 판단 기준을 고정한다.

## Phase 3
### Session 3

- 당시 목표: 한두 개 입력이 맞는 수준을 넘어서 fixture 전체를 통과하는 구조로 묶는다.
- 변경 단위: `problem/script/test.sh`, `docs/references/approach.md`, `docs/concepts/edge-cases.md`
- 처음 가설: 실수 포인트를 문장으로만 남기면 다시 틀리기 쉽고, 테스트 루프와 함께 봐야 실제 방어선이 보인다.
- 실제 조치: `test.sh`의 PASS/FAIL 루프와 `approach.md`의 실수 체크리스트를 나란히 읽으며, 어떤 분기가 어디를 막는지 다시 맞췄다.

CLI 1:

```bash
$ make -C study/Core-0A-Priority-Queue/1715/problem test
```

검증 신호:

- `Test 1: PASS`, `Results: 1/1 passed, 0 failed` 순서로 출력됐다.
- 이번 단계에서 특히 다시 확인한 실수 포인트는 아래 셋이었다.

- N=1 예외 처리 누락
- 병합 비용을 총합에 누적하지 않는 실수
- 힙 초기화 누락

핵심 코드 1:

```python
    heap = [int(input()) for _ in range(n)]
    heapq.heapify(heap)
    total = 0
    while len(heap) > 1:
        a = heapq.heappop(heap)
        b = heapq.heappop(heap)
        s = a + b
        total += s
        heapq.heappush(heap, s)
    print(total)
```

왜 이 코드가 중요했는가:

이 블록을 다시 보면 `N=1 예외 처리 누락`를 막는 자리가 어디인지 바로 보인다. 테스트가 통과했다는 사실을 코드로 다시 설명하는 데 가장 적절한 증거다.

새로 배운 것:

- 테스트를 다시 읽는 순간, “맞았다”보다 “어디서 안 틀리는가”를 더 분명하게 설명할 수 있었다.

다음:

- 마지막으로 개념 문서와 코드가 어느 지점에서 맞물리는지 정리한다.

## Phase 4
### Session 4

- 당시 목표: `카드 합치기 개념 정리 — 허프만 코딩 패턴`를 실제 코드와 연결해 마지막 설명 축을 세운다.
- 변경 단위: `cpp/src/solution.cpp`, `docs/concepts/*.md`, `python/src/solution.py`
- 처음 가설: 마지막 글에서 남겨야 할 것은 추상 개념이 아니라, 그 개념이 꼭 필요해진 줄이다.
- 실제 조치: Python과 C++ 구현을 나란히 읽으며 같은 전이가 유지되는지 확인했다.

CLI 2:

```bash
$ make -C study/Core-0A-Priority-Queue/1715/problem run-cpp
```

검증 신호:

- `100`가 그대로 나왔다.
- 설명용 문서가 아니라 실제 실행 결과와 같은 답이 나온다는 점이 마지막 확인 포인트였다.

핵심 코드 2:

```cpp
    for(int i=0;i<n;i++){ long long x; cin >> x; pq.push(x); }
    long long total = 0;
    while(pq.size() > 1){
        long long a = pq.top(); pq.pop();
        long long b = pq.top(); pq.pop();
        total += a + b;
        pq.push(a + b);
    }
    cout << total << '\n';
    return 0;
```

왜 이 코드가 중요했는가:

여기서는 `카드 합치기 개념 정리 — 허프만 코딩 패턴`가 별도 해설이 아니라는 점이 분명해진다. `가장 작은 두 묶음을 반복 병합하는 Huffman-style greedy`를 끝까지 지키는 데 필요한 최소 단위가 바로 이 블록에 남아 있다.

핵심 코드 3:

```python
        total += s
        heapq.heappush(heap, s)
    print(total)

if __name__ == "__main__":
    main()
```

왜 이 코드가 중요했는가:

마지막 출력과 종료 조건은 사소해 보여도 최종 출력까지 닫는 부분이다. `카드 정렬하기`도 이 구간이 흐려지면 첫 구현은 맞아 보여도 최종 설명이 흔들린다.

새로 배운 것:

- Python과 C++를 나란히 보니 `가장 작은 두 묶음을 반복 병합하는 Huffman-style greedy`의 본질은 문법이 아니라 전이 순서에 있었다. `N=1 예외 처리 누락`를 막는 규칙이 두 구현에서 그대로 유지됐다.
- 그래서 `Core-0A-Priority-Queue`의 질문인 `힙이 필요한 문제 구조를 어떻게 구분할까?`도 결과 요약이 아니라, 상태와 순서를 어떻게 붙잡는가의 문제로 읽히게 됐다.

다음:

- 이 시리즈는 여기서 닫히지만, 다음 문제를 읽을 때도 `문제 계약 -> 첫 상태 -> fixture 검증` 순서를 그대로 재사용할 수 있다.
