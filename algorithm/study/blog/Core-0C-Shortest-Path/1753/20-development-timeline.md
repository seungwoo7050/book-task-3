# 최단경로: 검증, edge case, 마지막 설명 축

앞 절반이 출발점이었다면, 뒷 절반은 마무리 단계다. 테스트, edge case, 개념 정리를 같은 흐름으로 묶어 이 풀이가 어디에서 안정됐는지 보여 준다.

## 구현 순서 요약

- `make -C study/Core-0C-Shortest-Path/1753/problem test`로 fixture 전체를 다시 돌린다.
- `docs/references/approach.md`의 실수 포인트를 코드 분기와 연결한다.
- `다익스트라 — 전체 최단 경로`와 `cpp/src/solution.cpp`를 붙여 마지막 판단 기준을 고정한다.

## Phase 3
### Session 3

- 당시 목표: 한두 개 입력이 맞는 수준을 넘어서 fixture 전체를 통과하는 구조로 묶는다.
- 변경 단위: `problem/script/test.sh`, `docs/references/approach.md`, `docs/concepts/edge-cases.md`
- 처음 가설: 실수 포인트를 문장으로만 남기면 다시 틀리기 쉽고, 테스트 루프와 함께 봐야 실제 방어선이 보인다.
- 실제 조치: `test.sh`의 PASS/FAIL 루프와 `approach.md`의 실수 체크리스트를 나란히 읽으며, 어떤 분기가 어디를 막는지 다시 맞췄다.

CLI 1:

```bash
$ make -C study/Core-0C-Shortest-Path/1753/problem test
```

검증 신호:

- `Test 1: PASS`, `Results: 1/1 passed, 0 failed` 순서로 출력됐다.
- 이번 단계에서 특히 다시 확인한 실수 포인트는 아래 셋이었다.

- INF 출력 문자열 처리 누락
- 1-based 정점 인덱스 오류
- 힙 push 조건 누락

핵심 코드 1:

```python
    for _ in range(e):
        u, nv, w = map(int, input().split())
        adj[u].append((nv, w))
    dist = [INF] * (v + 1)
    dist[k] = 0
    hq = [(0, k)]
    while hq:
        d, u = heapq.heappop(hq)
        if d > dist[u]:
            continue
```

왜 이 코드가 중요했는가:

검증의 핵심은 통과 여부보다 방어선의 위치를 확인하는 데 있다. 이 블록은 어떤 분기가 edge case를 실제로 막아 주는지 보여 준다.

새로 배운 것:

- 테스트를 다시 읽는 순간, “맞았다”보다 “어디서 안 틀리는가”를 더 분명하게 설명할 수 있었다.

다음:

- 마지막으로 개념 문서와 코드가 어느 지점에서 맞물리는지 정리한다.

## Phase 4
### Session 4

- 당시 목표: `다익스트라 — 전체 최단 경로`를 실제 코드와 연결해 마지막 설명 축을 세운다.
- 변경 단위: `cpp/src/solution.cpp`, `docs/concepts/*.md`, `python/src/solution.py`
- 처음 가설: 마지막 글에서 남겨야 할 것은 추상 개념이 아니라, 그 개념이 꼭 필요해진 줄이다.
- 실제 조치: Python과 C++ 구현을 나란히 읽으며 같은 전이가 유지되는지 확인했다.

CLI 2:

```bash
$ make -C study/Core-0C-Shortest-Path/1753/problem run-cpp
```

검증 신호:

- 마지막 확인값은 `7`, `INF`였다.
- 설명용 문서가 아니라 실제 실행 결과와 같은 답이 나온다는 점이 마지막 확인 포인트였다.

핵심 코드 2:

```cpp
    for(int i=0;i<E;i++){
        int u,v,w; cin >> u >> v >> w;
        adj[u].push_back({v,w});
    }
    const long long INF = 1e18;
    vector<long long> dist(V+1, INF);
    dist[K]=0;
    priority_queue<pair<long long,int>, vector<pair<long long,int>>, greater<>> pq;
    pq.push({0,K});
    while(!pq.empty()){
```

왜 이 코드가 중요했는가:

마지막 전환점은 이 코드였다. `다익스트라 — 전체 최단 경로`를 붙여 읽으면, 왜 이 문제의 설명이 결국 이 줄로 수렴하는지 자연스럽게 보인다.

핵심 코드 3:

```python
    for i in range(1, v + 1):
        out.append(str(dist[i]) if dist[i] != INF else 'INF')
    sys.stdout.write('\n'.join(out) + '\n')

if __name__ == "__main__":
    main()
```

왜 이 코드가 중요했는가:

마지막 출력과 종료 조건은 사소해 보여도 최종 출력까지 닫는 부분이다. `최단경로`도 이 구간이 흐려지면 첫 구현은 맞아 보여도 최종 설명이 흔들린다.

새로 배운 것:

- 비교 구현을 함께 읽으니 `다익스트라 — 전체 최단 경로`가 더 선명해졌다. 언어가 달라도 `단일 시작점에서 모든 정점까지 Dijkstra 최단거리 계산`를 지탱하는 상태 규칙은 거의 바뀌지 않았다.
- 그래서 `Core-0C-Shortest-Path`의 질문인 `가중치 조건에 따라 어떤 최단 경로 알고리즘을 골라야 할까?`도 결과 요약이 아니라, 상태와 순서를 어떻게 붙잡는가의 문제로 읽히게 됐다.

다음:

- 이 시리즈는 여기서 닫히지만, 다음 문제를 읽을 때도 `문제 계약 -> 첫 상태 -> fixture 검증` 순서를 그대로 재사용할 수 있다.
