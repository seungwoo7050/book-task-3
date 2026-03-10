# 접근 로그

> 프로젝트: 카드 정렬하기
> 아래 내용은 `notion-archive/01-approach-log.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 핵심 관찰

매번 **가장 작은 두 묶음**을 합치면 총 비교 횟수가 최소. 이유: 작은 묶음일수록 여러 번 합쳐지는 데, 작은 것끼리 먼저 합치면 큰 쪽의 재합산 횟수가 줄어든다.

## 알고리즘

```python
heapq.heapify(heap)
total = 0
while len(heap) > 1:
    a = heapq.heappop(heap)
    b = heapq.heappop(heap)
    s = a + b
    total += s
    heapq.heappush(heap, s)
```

1. 모든 묶음을 최소 힙에 넣기: `heapify` — $O(N)$
2. 가장 작은 2개 꺼내기 → 합치기 → 비용 누적 → 합친 결과 다시 힙에 삽입
3. 묶음이 1개 남을 때까지 반복

## 왜 정렬로는 안 되는가?

정렬 후 순서대로 합치면, 합친 결과가 다음 합치기에 영향. 예: [10, 20, 40]. 정렬 그리디로 (10+20)=30, (30+40)=70 → 총 100. 이것은 최적이지만, 합친 결과가 원래 배열의 다른 원소보다 클 수도 있어서 매번 최솟값을 찾아야 한다.

## 시간/공간

- $O(N \log N)$

## 이 접근에서 꼭 기억할 선택

- `카드 정렬하기`에서 중심이 된 판단은 `우선순위 큐가 필요한 상황을 식별하고 비교 기준을 일관되게 유지하는 연습`를 가장 단순한 상태 전이로 번역하는 것이었다.
- 대안이 더 화려해 보여도, 자동 검증과 설명 가능성을 함께 만족하는 쪽이 학습 레포에서는 더 가치가 있다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.
- 구현 이유를 따라가다가 막히면 `05-development-timeline.md`로 돌아가 실제로 어떤 순서로 판단을 굳혔는지 다시 보는 편이 좋다.

## 다음에 다시 풀 때의 질문

- 같은 문제를 더 작은 자료구조나 더 적은 상태로 설명할 수 있는가?
- 지금 선택한 전략이 경계 사례에서도 동일하게 유지되는가?
- 코드보다 먼저 적어 둘 한 문장은 무엇인가?

## 같이 읽을 문서

- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`huffman-concept.md`](../docs/concepts/huffman-concept.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
