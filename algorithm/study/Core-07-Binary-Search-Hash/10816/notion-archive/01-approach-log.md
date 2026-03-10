# BOJ 10816 — 접근 과정: Counter vs bisect

## Counter 방식 (채택)

```python
cnt = Counter(cards)
print(' '.join(str(cnt[q]) for q in queries))
```

`Counter`는 딕셔너리 서브클래스로, 존재하지 않는 키에 0을 반환. 쿼리마다 $O(1)$.

## 이진 탐색 방식 (대안)

```python
cards.sort()
for q in queries:
    count = bisect_right(cards, q) - bisect_left(cards, q)
```

정렬 후 `bisect_left`와 `bisect_right`의 차이가 해당 숫자의 개수. $O(\log N)$ per query.

## 선택 이유

$N, M \leq 500,000$에서 둘 다 충분히 빠르지만, Counter가 코드가 더 간결하다. 이진 탐색 방식은 CLRS Ch 12.3의 `lower_bound`/`upper_bound` 개념을 직접 사용하므로 학습적으로는 가치 있다.
