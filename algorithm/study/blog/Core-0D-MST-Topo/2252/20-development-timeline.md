# 줄 세우기: 검증, edge case, 마지막 설명 축

이제는 구현을 끝냈다고 말하는 단계가 아니라, 어떤 근거로 끝났다고 말할 수 있는지를 정리하는 단계다. 테스트 루프와 마지막 설명 축이 여기서 닫힌다.

## 구현 순서 요약

- `make -C study/Core-0D-MST-Topo/2252/problem test`로 fixture 전체를 다시 돌린다.
- `docs/references/approach.md`의 실수 포인트를 코드 분기와 연결한다.
- `위상 정렬 개념 정리 — 줄 세우기`와 `cpp/src/solution.cpp`를 붙여 마지막 판단 기준을 고정한다.

## Phase 3
### Session 3

- 당시 목표: 한두 개 입력이 맞는 수준을 넘어서 fixture 전체를 통과하는 구조로 묶는다.
- 변경 단위: `problem/script/test.sh`, `docs/references/approach.md`, `docs/concepts/edge-cases.md`
- 처음 가설: 실수 포인트를 문장으로만 남기면 다시 틀리기 쉽고, 테스트 루프와 함께 봐야 실제 방어선이 보인다.
- 실제 조치: `test.sh`의 PASS/FAIL 루프와 `approach.md`의 실수 체크리스트를 나란히 읽으며, 어떤 분기가 어디를 막는지 다시 맞췄다.

CLI 1:

```bash
$ make -C study/Core-0D-MST-Topo/2252/problem test
```

검증 신호:

- `Test 1: PASS`, `Results: 1/1 passed, 0 failed` 순서로 출력됐다.
- 이번 단계에서 특히 다시 확인한 실수 포인트는 아래 셋이었다.

- indegree 감소 누락
- 초기 0차수 노드 큐 삽입 누락
- 출력 노드 수 검증 누락

핵심 코드 1:

```python
    for _ in range(m):
        a, b = map(int, input().split())
        adj[a].append(b)
        indeg[b] += 1
    q = deque()
    for i in range(1, n + 1):
        if indeg[i] == 0:
            q.append(i)
    result = []
    while q:
```

왜 이 코드가 중요했는가:

이 블록을 다시 보면 `indegree 감소 누락`를 막는 자리가 어디인지 바로 보인다. 테스트가 통과했다는 사실을 코드로 다시 설명하는 데 가장 적절한 증거다.

새로 배운 것:

- 테스트를 다시 읽는 순간, “맞았다”보다 “어디서 안 틀리는가”를 더 분명하게 설명할 수 있었다.

다음:

- 마지막으로 개념 문서와 코드가 어느 지점에서 맞물리는지 정리한다.

## Phase 4
### Session 4

- 당시 목표: `위상 정렬 개념 정리 — 줄 세우기`를 실제 코드와 연결해 마지막 설명 축을 세운다.
- 변경 단위: `cpp/src/solution.cpp`, `docs/concepts/*.md`, `python/src/solution.py`
- 처음 가설: 마지막 글에서 남겨야 할 것은 추상 개념이 아니라, 그 개념이 꼭 필요해진 줄이다.
- 실제 조치: Python과 C++ 구현을 나란히 읽으며 같은 전이가 유지되는지 확인했다.

CLI 2:

```bash
$ make -C study/Core-0D-MST-Topo/2252/problem run-cpp
```

검증 신호:

- `1 2 3`가 그대로 나왔다.
- 설명용 문서가 아니라 실제 실행 결과와 같은 답이 나온다는 점이 마지막 확인 포인트였다.

핵심 코드 2:

```cpp
    for(int i=0;i<m;i++){
        int a,b; cin >> a >> b;
        adj[a].push_back(b);
        indeg[b]++;
    }
    queue<int> q;
    for(int i=1;i<=n;i++) if(indeg[i]==0) q.push(i);
    bool first=true;
    while(!q.empty()){
        int u=q.front(); q.pop();
```

왜 이 코드가 중요했는가:

마지막 전환점은 이 코드였다. `위상 정렬 개념 정리 — 줄 세우기`를 붙여 읽으면, 왜 이 문제의 설명이 결국 이 줄로 수렴하는지 자연스럽게 보인다.

핵심 코드 3:

```python
            if indeg[v] == 0:
                q.append(v)
    print(' '.join(result))

if __name__ == "__main__":
    main()
```

왜 이 코드가 중요했는가:

끝을 어떻게 닫느냐가 생각보다 중요했다. `줄 세우기`에서는 마지막 출력 정리가 구현의 완성도를 가장 직접적으로 드러냈다.

새로 배운 것:

- 비교 구현을 함께 읽으니 `위상 정렬 개념 정리 — 줄 세우기`가 더 선명해졌다. 언어가 달라도 `진입차수(indegree) 기반 Kahn 알고리즘으로 위상정렬 수행`를 지탱하는 상태 규칙은 거의 바뀌지 않았다.
- 그래서 `Core-0D-MST-Topo`의 질문인 `그래프 전체 구조나 순서를 만드는 규칙을 어떻게 설명할까?`도 결과 요약이 아니라, 상태와 순서를 어떻게 붙잡는가의 문제로 읽히게 됐다.

다음:

- 이 시리즈는 여기서 닫히지만, 다음 문제를 읽을 때도 `문제 계약 -> 첫 상태 -> fixture 검증` 순서를 그대로 재사용할 수 있다.
