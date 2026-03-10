# BOJ 10816 — 회고

## 배운 것

`Counter`는 Python에서 빈도 분석의 표준 도구다. 내부적으로 해시 맵이므로 $O(N)$ 구성 + $O(1)$ 쿼리. `bisect`를 사용한 이진 탐색 방식은 메모리를 덜 쓰고 최악 시간 보장이 더 좋다는 장점이 있다.

## lower_bound / upper_bound

CLRS의 `SEARCH` 연산을 확장한 개념. `bisect_left`= lower_bound, `bisect_right` = upper_bound. 차이가 "같은 값의 개수".
