# 접근 로그

> 프로젝트: 수 찾기
> 아래 내용은 `notion-archive/01-approach-log.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 해시 셋 방식 (채택)

```python
A = set(map(int, input().split()))
for q in queries:
    out.append('1' if q in A else '0')
```

`set`의 `in` 연산은 평균 $O(1)$. 전체 $O(N + M)$.

## 이진 탐색 방식 (대안)

```python
A.sort()
for q in queries:
    # bisect_left로 이진 탐색
    idx = bisect_left(A, q)
    found = idx < len(A) and A[idx] == q
```

정렬 $O(N \log N)$ + 쿼리 $O(M \log N)$.

## 선택 이유

Python에서는 `set`이 더 간결하고 빠르다. C++에서는 `unordered_set`(해시)이나 `lower_bound`(이진 탐색) 모두 좋은 선택.

## 출력 최적화

$M$개 결과를 `'\n'.join`으로 한 번에 출력.

## 이 접근에서 꼭 기억할 선택

- `수 찾기`에서 중심이 된 판단은 `탐색 대상을 재정의하고 자료구조 또는 매개변수 탐색으로 문제를 다시 보는 연습`를 가장 단순한 상태 전이로 번역하는 것이었다.
- 대안이 더 화려해 보여도, 자동 검증과 설명 가능성을 함께 만족하는 쪽이 학습 레포에서는 더 가치가 있다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.
- 구현 이유를 따라가다가 막히면 `05-development-timeline.md`로 돌아가 실제로 어떤 순서로 판단을 굳혔는지 다시 보는 편이 좋다.

## 다음에 다시 풀 때의 질문

- 같은 문제를 더 작은 자료구조나 더 적은 상태로 설명할 수 있는가?
- 지금 선택한 전략이 경계 사례에서도 동일하게 유지되는가?
- 코드보다 먼저 적어 둘 한 문장은 무엇인가?

## 같이 읽을 문서

- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`hash-search-concept.md`](../docs/concepts/hash-search-concept.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
