# 최소비용 구하기: 검증, edge case, 마지막 설명 축

이제는 구현을 끝냈다고 말하는 단계가 아니라, 어떤 근거로 끝났다고 말할 수 있는지를 정리하는 단계다. 테스트 루프와 마지막 설명 축이 여기서 닫힌다.

## 구현 순서 요약

- `make -C study/Core-0C-Shortest-Path/1916/problem test`로 fixture 전체를 다시 돌린다.
- `docs/references/approach.md`의 실수 포인트를 코드 분기와 연결한다.
- `다익스트라 개념 정리 — 최소비용 구하기`를 붙여 마지막 판단 기준을 고정한다.

## Phase 3
### Session 3

- 당시 목표: 한두 개 입력이 맞는 수준을 넘어서 fixture 전체를 통과하는 구조로 묶는다.
- 변경 단위: `problem/script/test.sh`, `docs/references/approach.md`, `docs/concepts/edge-cases.md`
- 처음 가설: 실수 포인트를 문장으로만 남기면 다시 틀리기 쉽고, 테스트 루프와 함께 봐야 실제 방어선이 보인다.
- 실제 조치: `test.sh`의 PASS/FAIL 루프와 `approach.md`의 실수 체크리스트를 나란히 읽으며, 어떤 분기가 어디를 막는지 다시 맞췄다.

CLI 1:

```bash
$ make -C study/Core-0C-Shortest-Path/1916/problem test
```

검증 신호:

- `Test 1: PASS`, `Results: 1/1 passed, 0 failed` 순서로 출력됐다.
- 이번 단계에서 특히 다시 확인한 실수 포인트는 아래 셋이었다.

- dist 초기값 INF 설정 누락
- 힙에서 꺼낸 값이 구버전인지 검사 누락
- 인접 리스트 방향성 처리 오류

핵심 코드 1:

```python
    for _ in range(m):
        u, v, w = map(int, input().split())
        adj[u].append((v, w))
    s, e = map(int, input().split())
    dist = [INF] * (n + 1)
    dist[s] = 0
    hq = [(0, s)]
    while hq:
        d, u = heapq.heappop(hq)
        if d > dist[u]:
```

왜 이 코드가 중요했는가:

검증의 핵심은 통과 여부보다 방어선의 위치를 확인하는 데 있다. 이 블록은 어떤 분기가 edge case를 실제로 막아 주는지 보여 준다.

새로 배운 것:

- 테스트를 다시 읽는 순간, “맞았다”보다 “어디서 안 틀리는가”를 더 분명하게 설명할 수 있었다.

다음:

- 마지막으로 개념 문서와 코드가 어느 지점에서 맞물리는지 정리한다.

## Phase 4
### Session 4

- 당시 목표: `다익스트라 개념 정리 — 최소비용 구하기`를 실제 코드와 연결해 마지막 설명 축을 세운다.
- 변경 단위: `docs/concepts/*.md`, `python/src/solution.py`
- 처음 가설: 마지막 글에서 남겨야 할 것은 추상 개념이 아니라, 그 개념이 꼭 필요해진 줄이다.
- 실제 조치: 마지막 출력과 guard를 다시 읽으며 개념 설명이 어느 줄을 가리키는지 고정했다.

CLI 2:

```bash
$ cd study/Core-0C-Shortest-Path/1916/problem && python3 ../python/src/solution.py < data/input1.txt
```

검증 신호:

- `4`가 그대로 나왔다.
- 설명용 문서가 아니라 실제 실행 결과와 같은 답이 나온다는 점이 마지막 확인 포인트였다.

핵심 코드 2:

```python
                dist[v] = nd
                heapq.heappush(hq, (nd, v))
    print(dist[e])

if __name__ == "__main__":
    main()
```

왜 이 코드가 중요했는가:

이 블록 덕분에 개념 정리가 공중에 뜨지 않는다. `dist 초기값 INF 설정 누락`를 막는 방식과 `우선순위 큐 기반 Dijkstra로 시작-도착 최소 비용 계산`가 여기서 한 번에 맞물린다.

핵심 코드 3:

```python
                dist[v] = nd
                heapq.heappush(hq, (nd, v))
    print(dist[e])

if __name__ == "__main__":
    main()
```

왜 이 코드가 중요했는가:

이 문제는 마지막 한 줄까지 포함해 설명이 완성된다. 출력 정리와 종료 조건이 흐리면 서사도 같이 흐려진다.

새로 배운 것:

- `다익스트라 개념 정리 — 최소비용 구하기`를 다시 읽고 나니, 이 문제의 핵심은 `우선순위 큐 기반 Dijkstra로 시작-도착 최소 비용 계산`를 끝까지 흔들리지 않게 유지하는 데 있었다.
- 그래서 `Core-0C-Shortest-Path`의 질문인 `가중치 조건에 따라 어떤 최단 경로 알고리즘을 골라야 할까?`도 결과 요약이 아니라, 상태와 순서를 어떻게 붙잡는가의 문제로 읽히게 됐다.

다음:

- 이 시리즈는 여기서 닫히지만, 다음 문제를 읽을 때도 `문제 계약 -> 첫 상태 -> fixture 검증` 순서를 그대로 재사용할 수 있다.
