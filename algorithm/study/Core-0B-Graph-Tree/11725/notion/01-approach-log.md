# 접근 로그

> 프로젝트: 트리의 부모 찾기
> 아래 내용은 `notion-archive/01-approach-log.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 핵심

루트(1)에서 BFS. 처음 방문하는 순간, 탐색 출발점이 부모.

```python
visited[1] = True
q = deque([1])
while q:
    u = q.popleft()
    for v in adj[u]:
        if not visited[v]:
            visited[v] = True
            parent[v] = u
            q.append(v)
```

## 출력

2번부터 $N$번까지 순서대로 `parent[i]` 출력.

## 시간/공간

- $O(N)$

## 이 접근에서 꼭 기억할 선택

- `트리의 부모 찾기`에서 중심이 된 판단은 `트리 구조의 성질을 이용해 탐색과 누적 계산을 재구성하는 연습`를 가장 단순한 상태 전이로 번역하는 것이었다.
- 대안이 더 화려해 보여도, 자동 검증과 설명 가능성을 함께 만족하는 쪽이 학습 레포에서는 더 가치가 있다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.
- 구현 이유를 따라가다가 막히면 `05-development-timeline.md`로 돌아가 실제로 어떤 순서로 판단을 굳혔는지 다시 보는 편이 좋다.

## 다음에 다시 풀 때의 질문

- 같은 문제를 더 작은 자료구조나 더 적은 상태로 설명할 수 있는가?
- 지금 선택한 전략이 경계 사례에서도 동일하게 유지되는가?
- 코드보다 먼저 적어 둘 한 문장은 무엇인가?

## 같이 읽을 문서

- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`tree-parent-concept.md`](../docs/concepts/tree-parent-concept.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
