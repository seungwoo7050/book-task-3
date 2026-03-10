# 접근 로그

> 프로젝트: 상근이의 여행
> 아래 내용은 `notion-archive/01-approach-log.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 핵심 관찰

연결 그래프에서 모든 노드를 방문하는 최소 간선 수 = 스패닝 트리 = $N - 1$.

가중치도 없고, 연결이 보장되므로:

```python
print(n - 1)
```

간선을 읽기만 하고 무시.

## 왜 N-1인가?

트리의 정의: $N$개 노드, $N-1$개 간선, 연결, 사이클 없음. 모든 노드를 방문하면서 사이클 없이 이동하면 트리. 트리의 간선 수 = $N-1$.

## 시간/공간

- $O(M)$ 입력 읽기

## 이 접근에서 꼭 기억할 선택

- `상근이의 여행`에서 중심이 된 판단은 `그래프 전체 구조를 만들거나 순서를 고정하는 규칙을 설명하는 연습`를 가장 단순한 상태 전이로 번역하는 것이었다.
- 대안이 더 화려해 보여도, 자동 검증과 설명 가능성을 함께 만족하는 쪽이 학습 레포에서는 더 가치가 있다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.
- 구현 이유를 따라가다가 막히면 `05-development-timeline.md`로 돌아가 실제로 어떤 순서로 판단을 굳혔는지 다시 보는 편이 좋다.

## 다음에 다시 풀 때의 질문

- 같은 문제를 더 작은 자료구조나 더 적은 상태로 설명할 수 있는가?
- 지금 선택한 전략이 경계 사례에서도 동일하게 유지되는가?
- 코드보다 먼저 적어 둘 한 문장은 무엇인가?

## 같이 읽을 문서

- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`spanning-tree-concept.md`](../docs/concepts/spanning-tree-concept.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
