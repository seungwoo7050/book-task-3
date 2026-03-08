# 구간 병합(Interval Merge) 개념 정리 — 선 긋기

## 핵심 아이디어
좌표 축 위의 N개 선분의 합집합 길이를 구하는 문제.
**정렬 후 스위핑(Sweep)** 패턴의 전형적 문제.

## 알고리즘
1. 선분을 시작점 기준 오름차순 정렬
2. 현재 구간 `[cur_start, cur_end]` 유지
3. 다음 선분이 겹치면 → `cur_end = max(cur_end, e)` 확장
4. 겹치지 않으면 → 현재 구간 길이 누적, 새 구간 시작

## CLRS 연결
CLRS Ch 16.1 Activity Selection Problem과 유사한 정렬+스위핑 패턴.
탐욕적(Greedy)으로 현재 구간을 확장해 나간다.

## 시간 복잡도
$O(N \log N)$ — 정렬이 병목.
