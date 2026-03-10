# BOJ 1744 — 접근 과정

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
