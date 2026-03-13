# 트리의 지름: 검증, edge case, 마지막 설명 축

뒷 절반에서는 “왜 맞는가”를 더 조밀하게 확인한다. fixture 전체를 다시 돌려 실수 포인트를 묶고, 마지막에는 개념 문서와 코드가 정확히 어디서 맞물리는지 정리한다.

## 구현 순서 요약

- `make -C study/Core-0B-Graph-Tree/1167/problem test`로 fixture 전체를 다시 돌린다.
- `docs/references/approach.md`의 실수 포인트를 코드 분기와 연결한다.
- `트리의 지름 개념 정리`와 `cpp/src/solution.cpp`를 붙여 마지막 판단 기준을 고정한다.

## Phase 3
### Session 3

- 당시 목표: 한두 개 입력이 맞는 수준을 넘어서 fixture 전체를 통과하는 구조로 묶는다.
- 변경 단위: `problem/script/test.sh`, `docs/references/approach.md`, `docs/concepts/edge-cases.md`
- 처음 가설: 실수 포인트를 문장으로만 남기면 다시 틀리기 쉽고, 테스트 루프와 함께 봐야 실제 방어선이 보인다.
- 실제 조치: `test.sh`의 PASS/FAIL 루프와 `approach.md`의 실수 체크리스트를 나란히 읽으며, 어떤 분기가 어디를 막는지 다시 맞췄다.

CLI 1:

```bash
$ make -C study/Core-0B-Graph-Tree/1167/problem test
```

검증 신호:

- `Test 1: PASS`, `Results: 1/1 passed, 0 failed` 순서로 출력됐다.
- 이번 단계에서 특히 다시 확인한 실수 포인트는 아래 셋이었다.

- 입력 라인의 -1 종결 처리 누락
- 가중치 누적 대신 간선 수만 세는 실수
- 재방문 체크 누락

핵심 코드 1:

```python
    for _ in range(v):
        data = list(map(int, input().split()))
        node = data[0]
        i = 1
        while data[i] != -1:
            neighbor, weight = data[i], data[i + 1]
            adj[node].append((neighbor, weight))
            i += 2

    def bfs(start):
```

왜 이 코드가 중요했는가:

검증의 핵심은 통과 여부보다 방어선의 위치를 확인하는 데 있다. 이 블록은 어떤 분기가 edge case를 실제로 막아 주는지 보여 준다.

새로 배운 것:

- 테스트를 다시 읽는 순간, “맞았다”보다 “어디서 안 틀리는가”를 더 분명하게 설명할 수 있었다.

다음:

- 마지막으로 개념 문서와 코드가 어느 지점에서 맞물리는지 정리한다.

## Phase 4
### Session 4

- 당시 목표: `트리의 지름 개념 정리`를 실제 코드와 연결해 마지막 설명 축을 세운다.
- 변경 단위: `cpp/src/solution.cpp`, `docs/concepts/*.md`, `python/src/solution.py`
- 처음 가설: 마지막 글에서 남겨야 할 것은 추상 개념이 아니라, 그 개념이 꼭 필요해진 줄이다.
- 실제 조치: Python과 C++ 구현을 나란히 읽으며 같은 전이가 유지되는지 확인했다.

CLI 2:

```bash
$ make -C study/Core-0B-Graph-Tree/1167/problem run-cpp
```

검증 신호:

- `11`가 그대로 나왔다.
- 설명용 문서가 아니라 실제 실행 결과와 같은 답이 나온다는 점이 마지막 확인 포인트였다.

핵심 코드 2:

```cpp
    while(!q.empty()){
        int u=q.front(); q.pop();
        for(auto [v,w]:adj[u]){
            if(dist[v]==-1){
                dist[v]=dist[u]+w;
                q.push(v);
                if(dist[v]>far_dist){ far_dist=dist[v]; far_node=v; }
            }
        }
    }
```

왜 이 코드가 중요했는가:

마지막 전환점은 이 코드였다. `트리의 지름 개념 정리`를 붙여 읽으면, 왜 이 문제의 설명이 결국 이 줄로 수렴하는지 자연스럽게 보인다.

핵심 코드 3:

```python
    u, _ = bfs(1)
    _, diameter = bfs(u)
    print(diameter)

if __name__ == "__main__":
    main()
```

왜 이 코드가 중요했는가:

이 문제는 마지막 한 줄까지 포함해 설명이 완성된다. 출력 정리와 종료 조건이 흐리면 서사도 같이 흐려진다.

새로 배운 것:

- C++ 쪽까지 다시 확인하고 나니, 이 문제에서 중요한 건 표현 방식이 아니라 `임의 정점에서 최원점 탐색 후 한 번 더 탐색하는 트리 지름(two-pass)`를 끝까지 보존하는 전이 순서라는 점이었다.
- 그래서 `Core-0B-Graph-Tree`의 질문인 `트리 성질을 이용해 탐색과 누적 계산을 어떻게 단순화할까?`도 결과 요약이 아니라, 상태와 순서를 어떻게 붙잡는가의 문제로 읽히게 됐다.

다음:

- 이 시리즈는 여기서 닫히지만, 다음 문제를 읽을 때도 `문제 계약 -> 첫 상태 -> fixture 검증` 순서를 그대로 재사용할 수 있다.
