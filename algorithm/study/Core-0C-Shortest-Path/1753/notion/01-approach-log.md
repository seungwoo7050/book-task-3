# 접근 로그

> 프로젝트: 최단경로
> 아래 내용은 `notion-archive/01-approach-log.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 다익스트라 + 힙

```python
dist = [INF] * (v + 1)
dist[k] = 0
hq = [(0, k)]
while hq:
    d, u = heapq.heappop(hq)
    if d > dist[u]:
        continue  # lazy deletion
    for nv, w in adj[u]:
        nd = d + w
        if nd < dist[nv]:
            dist[nv] = nd
            heapq.heappush(hq, (nd, nv))
```

## Lazy Deletion

`if d > dist[u]: continue` — 이미 더 나은 경로를 찾은 노드는 건너뛴다. `decrease-key` 대신 사용하는 파이썬식 패턴.

## 왜 다익스트라가 맞는가?

모든 가중치가 양수 → 한 번 확정된 최단 거리는 나중에 줄어들 수 없음 → 그리디 선택(가장 짧은 거리의 노드부터 확정)이 정당.

## 시간/공간

- $O((V+E)\log V)$

## 이 접근에서 꼭 기억할 선택

- `최단경로`에서 중심이 된 판단은 `가중치 조건과 그래프 특성에 맞는 최단 경로 알고리즘을 선택하는 연습`를 가장 단순한 상태 전이로 번역하는 것이었다.
- 대안이 더 화려해 보여도, 자동 검증과 설명 가능성을 함께 만족하는 쪽이 학습 레포에서는 더 가치가 있다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.
- 구현 이유를 따라가다가 막히면 `05-development-timeline.md`로 돌아가 실제로 어떤 순서로 판단을 굳혔는지 다시 보는 편이 좋다.

## 다음에 다시 풀 때의 질문

- 같은 문제를 더 작은 자료구조나 더 적은 상태로 설명할 수 있는가?
- 지금 선택한 전략이 경계 사례에서도 동일하게 유지되는가?
- 코드보다 먼저 적어 둘 한 문장은 무엇인가?

## 같이 읽을 문서

- [`dijkstra-all-concept.md`](../docs/concepts/dijkstra-all-concept.md)
- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
