# 접근 로그

> 프로젝트: 최대 힙
> 아래 내용은 `notion-archive/01-approach-log.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 핵심 트릭: 부호 반전

Python `heapq`는 최소 힙만 지원. 최대 힙은 값을 음수로 넣고 꺼낼 때 다시 음수로 변환.

```python
heapq.heappush(heap, -x)  # 삽입
-heapq.heappop(heap)       # 추출
```

## 출력 최적화

매 연산마다 `print`하면 I/O 병목. `out` 리스트에 모아서 `'\n'.join(out)`으로 한 번에 출력.

## 시간/공간

- 삽입/추출 각 $O(\log N)$
- 전체 $O(N \log N)$

## 이 접근에서 꼭 기억할 선택

- `최대 힙`에서 중심이 된 판단은 `우선순위 큐가 필요한 상황을 식별하고 비교 기준을 일관되게 유지하는 연습`를 가장 단순한 상태 전이로 번역하는 것이었다.
- 대안이 더 화려해 보여도, 자동 검증과 설명 가능성을 함께 만족하는 쪽이 학습 레포에서는 더 가치가 있다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.
- 구현 이유를 따라가다가 막히면 `05-development-timeline.md`로 돌아가 실제로 어떤 순서로 판단을 굳혔는지 다시 보는 편이 좋다.

## 다음에 다시 풀 때의 질문

- 같은 문제를 더 작은 자료구조나 더 적은 상태로 설명할 수 있는가?
- 지금 선택한 전략이 경계 사례에서도 동일하게 유지되는가?
- 코드보다 먼저 적어 둘 한 문장은 무엇인가?

## 같이 읽을 문서

- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`heap-concept.md`](../docs/concepts/heap-concept.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
