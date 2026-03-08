# 그리디 개념 정리 — 동전 0

## CLRS 연결
CLRS Ch 16.1 Activity Selection — 그리디 선택 성질(Greedy-Choice Property).
CLRS Ch 16.2 — 동전 문제에서 그리디가 최적인 조건: **각 동전이 다음 동전의 배수**.

## 핵심 아이디어
큰 동전부터 최대한 사용 → 최소 동전 수.
$A_i | A_{i+1}$ 조건이 보장되므로 그리디가 최적.

## 알고리즘
```python
for coin in reversed(coins):
    count += K // coin
    K %= coin
```

## 그리디가 실패하는 경우
동전이 `[1, 3, 4]`일 때 6을 만들면:
- 그리디: 4+1+1 = 3개
- 최적: 3+3 = 2개
→ 배수 조건이 없으면 DP 필요.
