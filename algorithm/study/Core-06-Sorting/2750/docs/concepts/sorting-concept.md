# 정렬 개념 정리 — 수 정렬하기

## CLRS 연결
CLRS Part II (Sorting and Order Statistics) — Ch 2 Insertion-Sort, Ch 7 Quicksort, Ch 8 Counting Sort.

## 문제 유형
$N \le 1000$인 정수 배열 오름차순 정렬. 어떤 정렬 알고리즘이든 통과.

## Python `list.sort()`
Python의 `sort()`는 Timsort ($O(N \log N)$, stable, adaptive).
$N \le 1000$이므로 $O(N^2)$ 알고리즘도 충분.

## 정렬 알고리즘 비교
| 알고리즘 | 평균 | 최악 | 안정성 | 추가공간 |
|----------|------|------|--------|----------|
| 삽입정렬 | $O(N^2)$ | $O(N^2)$ | O | $O(1)$ |
| 병합정렬 | $O(N\log N)$ | $O(N\log N)$ | O | $O(N)$ |
| 퀵정렬 | $O(N\log N)$ | $O(N^2)$ | X | $O(\log N)$ |
| Timsort | $O(N\log N)$ | $O(N\log N)$ | O | $O(N)$ |
