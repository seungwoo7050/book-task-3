# 타임머신: 검증, edge case, 마지막 설명 축

이제는 구현을 끝냈다고 말하는 단계가 아니라, 어떤 근거로 끝났다고 말할 수 있는지를 정리하는 단계다. 테스트 루프와 마지막 설명 축이 여기서 닫힌다.

## 구현 순서 요약

- `make -C study/Core-0C-Shortest-Path/11657/problem test`로 fixture 전체를 다시 돌린다.
- `docs/references/approach.md`의 실수 포인트를 코드 분기와 연결한다.
- `벨만-포드 개념 정리 — 타임머신`와 `cpp/src/solution.cpp`를 붙여 마지막 판단 기준을 고정한다.

## Phase 3
### Session 3

- 당시 목표: 한두 개 입력이 맞는 수준을 넘어서 fixture 전체를 통과하는 구조로 묶는다.
- 변경 단위: `problem/script/test.sh`, `docs/references/approach.md`, `docs/concepts/edge-cases.md`
- 처음 가설: 실수 포인트를 문장으로만 남기면 다시 틀리기 쉽고, 테스트 루프와 함께 봐야 실제 방어선이 보인다.
- 실제 조치: `test.sh`의 PASS/FAIL 루프와 `approach.md`의 실수 체크리스트를 나란히 읽으며, 어떤 분기가 어디를 막는지 다시 맞췄다.

CLI 1:

```bash
$ make -C study/Core-0C-Shortest-Path/11657/problem test
```

검증 신호:

- `Test 1: PASS`, `Results: 1/1 passed, 0 failed` 순서로 출력됐다.
- 이번 단계에서 특히 다시 확인한 실수 포인트는 아래 셋이었다.

- 시작점 도달 불가 정점 완화 조건 누락
- 음수 사이클 검사 라운드 누락
- 출력에서 시작점 제외 범위 처리 오류

핵심 코드 1:

```python
    for _ in range(m):
        a, b, c = map(int, input().split())
        edges.append((a, b, c))
    dist = [INF] * (n + 1)
    dist[1] = 0
    for i in range(n):
        for a, b, c in edges:
            if dist[a] != INF and dist[a] + c < dist[b]:
                if i == n - 1:
                    print(-1)
```

왜 이 코드가 중요했는가:

이 블록을 다시 보면 `시작점 도달 불가 정점 완화 조건 누락`를 막는 자리가 어디인지 바로 보인다. 테스트가 통과했다는 사실을 코드로 다시 설명하는 데 가장 적절한 증거다.

새로 배운 것:

- 테스트를 다시 읽는 순간, “맞았다”보다 “어디서 안 틀리는가”를 더 분명하게 설명할 수 있었다.

다음:

- 마지막으로 개념 문서와 코드가 어느 지점에서 맞물리는지 정리한다.

## Phase 4
### Session 4

- 당시 목표: `벨만-포드 개념 정리 — 타임머신`를 실제 코드와 연결해 마지막 설명 축을 세운다.
- 변경 단위: `cpp/src/solution.cpp`, `docs/concepts/*.md`, `python/src/solution.py`
- 처음 가설: 마지막 글에서 남겨야 할 것은 추상 개념이 아니라, 그 개념이 꼭 필요해진 줄이다.
- 실제 조치: Python과 C++ 구현을 나란히 읽으며 같은 전이가 유지되는지 확인했다.

CLI 2:

```bash
$ make -C study/Core-0C-Shortest-Path/11657/problem run-cpp
```

검증 신호:

- `4`, `3` 순서로 출력됐다.
- 설명용 문서가 아니라 실제 실행 결과와 같은 답이 나온다는 점이 마지막 확인 포인트였다.

핵심 코드 2:

```cpp
    for(auto &e:edges) cin >> e.u >> e.v >> e.w;
    const long long INF = 1e18;
    vector<long long> dist(n+1, INF);
    dist[1]=0;
    for(int i=0;i<n;i++){
        for(auto &[u,v,w]:edges){
            if(dist[u]!=INF && dist[u]+w < dist[v]){
                if(i==n-1){ cout << -1 << '\n'; return 0; }
                dist[v]=dist[u]+w;
            }
```

왜 이 코드가 중요했는가:

마지막 전환점은 이 코드였다. `벨만-포드 개념 정리 — 타임머신`를 붙여 읽으면, 왜 이 문제의 설명이 결국 이 줄로 수렴하는지 자연스럽게 보인다.

핵심 코드 3:

```python
    for i in range(2, n + 1):
        out.append(str(dist[i]) if dist[i] != INF else '-1')
    sys.stdout.write('\n'.join(out) + '\n')

if __name__ == "__main__":
    main()
```

왜 이 코드가 중요했는가:

이 문제는 마지막 한 줄까지 포함해 설명이 완성된다. 출력 정리와 종료 조건이 흐리면 서사도 같이 흐려진다.

새로 배운 것:

- C++ 쪽까지 다시 확인하고 나니, 이 문제에서 중요한 건 표현 방식이 아니라 `N-1회 완화 + 추가 1회 검사로 음수 사이클을 판정하는 Bellman-Ford`를 끝까지 보존하는 전이 순서라는 점이었다.
- 그래서 `Core-0C-Shortest-Path`의 질문인 `가중치 조건에 따라 어떤 최단 경로 알고리즘을 골라야 할까?`도 결과 요약이 아니라, 상태와 순서를 어떻게 붙잡는가의 문제로 읽히게 됐다.

다음:

- 이 시리즈는 여기서 닫히지만, 다음 문제를 읽을 때도 `문제 계약 -> 첫 상태 -> fixture 검증` 순서를 그대로 재사용할 수 있다.
