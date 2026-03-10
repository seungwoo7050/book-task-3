# 접근 로그

> 프로젝트: 트리의 지름
> 아래 내용은 `notion-archive/01-approach-log.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 핵심 알고리즘: 두 번의 BFS

1. 임의의 점(보통 1번)에서 BFS → 가장 먼 점 $u$를 찾음
2. $u$에서 BFS → 가장 먼 점 $v$와 그 거리 = 지름

```python
u, _ = bfs(1)
_, diameter = bfs(u)
```

## 왜 이것이 맞는가?

**정리**: 트리에서 임의의 정점에서 가장 먼 점은 지름의 한 끝점이다.

**증명 스케치**: 지름의 끝점이 $a, b$라 하자. 임의의 점 $s$에서 BFS한 최원점이 $u$인데, $u$가 $a$도 $b$도 아니라면 → $s$에서 $u$까지의 경로와 지름 경로를 비교하여 모순 도출.

## 입력 파싱

각 줄: `노드번호 이웃1 가중치1 이웃2 가중치2 ... -1`

```python
while data[i] != -1:
    neighbor, weight = data[i], data[i+1]
    adj[node].append((neighbor, weight))
    i += 2
```

## 시간/공간

- BFS 2회: $O(V)$

## 이 접근에서 꼭 기억할 선택

- `트리의 지름`에서 중심이 된 판단은 `트리 구조의 성질을 이용해 탐색과 누적 계산을 재구성하는 연습`를 가장 단순한 상태 전이로 번역하는 것이었다.
- 대안이 더 화려해 보여도, 자동 검증과 설명 가능성을 함께 만족하는 쪽이 학습 레포에서는 더 가치가 있다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.
- 구현 이유를 따라가다가 막히면 `05-development-timeline.md`로 돌아가 실제로 어떤 순서로 판단을 굳혔는지 다시 보는 편이 좋다.

## 다음에 다시 풀 때의 질문

- 같은 문제를 더 작은 자료구조나 더 적은 상태로 설명할 수 있는가?
- 지금 선택한 전략이 경계 사례에서도 동일하게 유지되는가?
- 코드보다 먼저 적어 둘 한 문장은 무엇인가?

## 같이 읽을 문서

- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`tree-diameter-concept.md`](../docs/concepts/tree-diameter-concept.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
