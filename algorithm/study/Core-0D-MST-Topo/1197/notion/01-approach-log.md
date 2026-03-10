# 접근 로그

> 프로젝트: 최소 스패닝 트리
> 아래 내용은 `notion-archive/01-approach-log.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 크루스칼 알고리즘

1. 모든 간선을 가중치 기준 정렬
2. 가장 가벼운 간선부터 순회
3. 두 끝점이 같은 집합이 아니면 선택 (Union)
4. $V-1$개 간선을 선택하면 종료

```python
edges.sort()  # (weight, a, b)
for w, a, b in edges:
    if union(parent, rank, a, b):
        total += w
        cnt += 1
        if cnt == v - 1:
            break
```

## Union-Find 최적화

- **경로 압축**: `parent[x] = parent[parent[x]]` (path splitting)
- **유니온 바이 랭크**: 작은 트리를 큰 트리 아래에 붙임

```python
def find(parent, x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]  # path splitting
        x = parent[x]
    return x
```

## 시간/공간

- $O(E \log E)$ 정렬 + $O(E \cdot \alpha(V))$ Union-Find ≈ $O(E \log E)$

## 이 접근에서 꼭 기억할 선택

- `최소 스패닝 트리`에서 중심이 된 판단은 `그래프 전체 구조를 만들거나 순서를 고정하는 규칙을 설명하는 연습`를 가장 단순한 상태 전이로 번역하는 것이었다.
- 대안이 더 화려해 보여도, 자동 검증과 설명 가능성을 함께 만족하는 쪽이 학습 레포에서는 더 가치가 있다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.
- 구현 이유를 따라가다가 막히면 `05-development-timeline.md`로 돌아가 실제로 어떤 순서로 판단을 굳혔는지 다시 보는 편이 좋다.

## 다음에 다시 풀 때의 질문

- 같은 문제를 더 작은 자료구조나 더 적은 상태로 설명할 수 있는가?
- 지금 선택한 전략이 경계 사례에서도 동일하게 유지되는가?
- 코드보다 먼저 적어 둘 한 문장은 무엇인가?

## 같이 읽을 문서

- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`kruskal-concept.md`](../docs/concepts/kruskal-concept.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
