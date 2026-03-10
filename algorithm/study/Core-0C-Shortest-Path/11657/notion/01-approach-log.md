# 접근 로그

> 프로젝트: 타임머신
> 아래 내용은 `notion-archive/01-approach-log.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 벨만-포드 알고리즘

$V-1$번 모든 간선을 순회하며 relaxation. $V$번째에도 갱신이 일어나면 음의 사이클.

```python
dist = [INF] * (n + 1)
dist[1] = 0
for i in range(n):
    for a, b, c in edges:
        if dist[a] != INF and dist[a] + c < dist[b]:
            if i == n - 1:
                print(-1)
                return
            dist[b] = dist[a] + c
```

## 핵심 포인트

1. $V-1$번 반복: 최단 경로는 최대 $V-1$개 간선을 포함
2. $V$번째 갱신 = 음의 사이클: 이미 최적인데 더 줄어든다면 무한히 줄어들 수 있음
3. `dist[a] != INF` 검사: 아직 도달 불가한 정점에서 출발하는 relaxation 방지

## 다익스트라와의 차이

- 다익스트라: 음의 가중치 불가, $O((V+E)\log V)$
- 벨만-포드: 음의 가중치 OK, $O(VE)$

## 시간/공간

- $O(VE)$

## 이 접근에서 꼭 기억할 선택

- `타임머신`에서 중심이 된 판단은 `가중치 조건과 그래프 특성에 맞는 최단 경로 알고리즘을 선택하는 연습`를 가장 단순한 상태 전이로 번역하는 것이었다.
- 대안이 더 화려해 보여도, 자동 검증과 설명 가능성을 함께 만족하는 쪽이 학습 레포에서는 더 가치가 있다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.
- 구현 이유를 따라가다가 막히면 `05-development-timeline.md`로 돌아가 실제로 어떤 순서로 판단을 굳혔는지 다시 보는 편이 좋다.

## 다음에 다시 풀 때의 질문

- 같은 문제를 더 작은 자료구조나 더 적은 상태로 설명할 수 있는가?
- 지금 선택한 전략이 경계 사례에서도 동일하게 유지되는가?
- 코드보다 먼저 적어 둘 한 문장은 무엇인가?

## 같이 읽을 문서

- [`bellman-ford-concept.md`](../docs/concepts/bellman-ford-concept.md)
- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
