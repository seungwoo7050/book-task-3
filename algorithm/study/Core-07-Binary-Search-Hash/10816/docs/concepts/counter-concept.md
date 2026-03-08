# Counter / 해시맵 개념 정리 — 숫자 카드 2

## 핵심 아이디어
각 숫자가 몇 번 등장하는지 세는 빈도 카운팅 문제.
`Counter`(해시맵)로 $O(N)$에 전처리 후 각 쿼리를 $O(1)$에 응답.

## CLRS 연결
CLRS Ch 11 Hash Tables — Direct-Address Table, Hash Table.
CLRS Ch 8.2 Counting Sort — 빈도 배열의 원리.

## 대안: 이진 탐색
정렬 후 `bisect_left`와 `bisect_right`로 카운트:
`count = bisect_right(arr, x) - bisect_left(arr, x)`
시간: $O(N \log N + M \log N)$
