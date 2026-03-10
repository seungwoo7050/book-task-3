# 접근 로그

> 프로젝트: 수 묶기
> 아래 내용은 `notion-archive/01-approach-log.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 핵심 분류

수를 4종류로 분류:
1. **양수(>1)**: 큰 것끼리 묶어서 곱 → 합에 기여
2. **1**: 묶으면 손해 ($1 \times x < 1 + x$), 항상 그냥 더함
3. **0**: 홀수 개 음수가 남으면 0과 묶어서 상쇄
4. **음수(<0)**: 절댓값 큰 것끼리 묶어서 곱 → 양수로 변환

## 알고리즘

```python
# 양수(>1): 내림차순 정렬 → 2개씩 곱
pos.sort(reverse=True)
for i in range(0, len(pos)-1, 2):
    total += pos[i] * pos[i+1]
if len(pos) % 2 == 1:
    total += pos[-1]

# 음수: 오름차순 정렬 → 2개씩 곱 (음×음=양)
neg.sort()
for i in range(0, len(neg)-1, 2):
    total += neg[i] * neg[i+1]
if len(neg) % 2 == 1:
    if zeros == 0:
        total += neg[-1]  # 상쇄할 0이 없으면 그냥 더함
```

## 왜 1을 따로 분류하는가?

$1 \times x = x$ 이지만 $1 + x = 1 + x > x$. 곱하면 손해.

## 시간/공간
- $O(N \log N)$ 정렬

## 이 접근에서 꼭 기억할 선택

- `수 묶기`에서 중심이 된 판단은 `탐욕 선택의 기준을 말로 설명하고 반례 가능성을 점검하는 연습`를 가장 단순한 상태 전이로 번역하는 것이었다.
- 대안이 더 화려해 보여도, 자동 검증과 설명 가능성을 함께 만족하는 쪽이 학습 레포에서는 더 가치가 있다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.
- 구현 이유를 따라가다가 막히면 `05-development-timeline.md`로 돌아가 실제로 어떤 순서로 판단을 굳혔는지 다시 보는 편이 좋다.

## 다음에 다시 풀 때의 질문

- 같은 문제를 더 작은 자료구조나 더 적은 상태로 설명할 수 있는가?
- 지금 선택한 전략이 경계 사례에서도 동일하게 유지되는가?
- 코드보다 먼저 적어 둘 한 문장은 무엇인가?

## 같이 읽을 문서

- [`bundling-greedy-concept.md`](../docs/concepts/bundling-greedy-concept.md)
- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
