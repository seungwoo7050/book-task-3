# 접근 로그

> 프로젝트: 공유기 설치
> 아래 내용은 `notion-archive/01-approach-log.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 핵심 아이디어

"최소 거리 $d$로 $C$개의 공유기를 설치할 수 있는가?"를 판별 함수로 정의하고, $d$에 대해 이진 탐색한다.

## 판별 함수

```python
def feasible(d):
    count = 1
    last = houses[0]
    for i in range(1, N):
        if houses[i] - last >= d:
            count += 1
            last = houses[i]
            if count >= C:
                return True
    return False
```

탐욕적으로 가능한 한 빨리 설치: 현재 위치에서 거리 $d$ 이상인 첫 집에 설치. $O(N)$.

## 이진 탐색

```python
lo, hi, ans = 1, houses[-1] - houses[0], 0
while lo <= hi:
    mid = (lo + hi) // 2
    if feasible(mid):
        ans = mid
        lo = mid + 1  # 더 큰 거리도 가능?
    else:
        hi = mid - 1  # 거리 줄이기
```

## 전체 복잡도

- 정렬: $O(N \log N)$
- 이진 탐색: $O(\log(\text{max\_coord}) \cdot N)$
- 전체: $O(N \log N + N \log(\text{max\_coord}))$

## 왜 탐욕적 판별이 정당한가

집이 정렬되어 있으므로, "가능한 한 빨리 설치"하는 것이 설치 개수를 최대화한다. 뒤에서 더 많이 설치할 수 있는 여지를 희생할 이유가 없다.

## 이 접근에서 꼭 기억할 선택

- `공유기 설치`에서 중심이 된 판단은 `탐색 대상을 재정의하고 자료구조 또는 매개변수 탐색으로 문제를 다시 보는 연습`를 가장 단순한 상태 전이로 번역하는 것이었다.
- 대안이 더 화려해 보여도, 자동 검증과 설명 가능성을 함께 만족하는 쪽이 학습 레포에서는 더 가치가 있다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.
- 구현 이유를 따라가다가 막히면 `05-development-timeline.md`로 돌아가 실제로 어떤 순서로 판단을 굳혔는지 다시 보는 편이 좋다.

## 다음에 다시 풀 때의 질문

- 같은 문제를 더 작은 자료구조나 더 적은 상태로 설명할 수 있는가?
- 지금 선택한 전략이 경계 사례에서도 동일하게 유지되는가?
- 코드보다 먼저 적어 둘 한 문장은 무엇인가?

## 같이 읽을 문서

- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`parametric-search-concept.md`](../docs/concepts/parametric-search-concept.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
