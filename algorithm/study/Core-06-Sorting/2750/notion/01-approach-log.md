# 접근 로그

> 프로젝트: 수 정렬하기
> 아래 내용은 `notion-archive/01-approach-log.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 구현

```python
nums = [int(input()) for _ in range(N)]
nums.sort()
print('\n'.join(map(str, nums)))
```

Python의 Timsort는 $O(N \log N)$ 보장. $N \leq 1000$에서 어떤 정렬 알고리즘이든 충분.

## 대안으로 고려한 것

- **삽입 정렬 직접 구현**: CLRS Ch 2.1의 학습 목적으로 가능. $O(N^2)$이지만 $N \leq 1000$에서 문제 없음.
- **병합 정렬**: Ch 2.3의 분할 정복 예시. 재귀 + 병합으로 $O(N \log N)$.
- **힙 정렬**: Ch 6의 in-place $O(N \log N)$.

학습 목적으로 직접 구현을 해볼 수 있지만, 제출용으로는 내장 `sort()`가 가장 간결하고 확실하다.

## 이 접근에서 꼭 기억할 선택

- `수 정렬하기`에서 중심이 된 판단은 `정렬 기준을 설계하고, 정렬 이후의 후처리 로직을 분리해 설명하는 연습`를 가장 단순한 상태 전이로 번역하는 것이었다.
- 대안이 더 화려해 보여도, 자동 검증과 설명 가능성을 함께 만족하는 쪽이 학습 레포에서는 더 가치가 있다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.
- 구현 이유를 따라가다가 막히면 `05-development-timeline.md`로 돌아가 실제로 어떤 순서로 판단을 굳혔는지 다시 보는 편이 좋다.

## 다음에 다시 풀 때의 질문

- 같은 문제를 더 작은 자료구조나 더 적은 상태로 설명할 수 있는가?
- 지금 선택한 전략이 경계 사례에서도 동일하게 유지되는가?
- 코드보다 먼저 적어 둘 한 문장은 무엇인가?

## 같이 읽을 문서

- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`sorting-concept.md`](../docs/concepts/sorting-concept.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
