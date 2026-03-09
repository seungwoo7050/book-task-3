# 지식 인덱스 — BOJ 2164

## 핵심 개념

### 큐 (Queue)
FIFO(First In, First Out) 자료 구조. `popleft()`/`append()` 패턴.

### collections.deque
Python 표준 라이브러리의 양방향 큐. 양쪽 끝에서 O(1) 삽입/삭제.
일반 list의 `pop(0)`은 O(n)이므로, 큐 용도로는 반드시 deque를 사용해야 한다.

## 연결되는 문제들
| 개념 | 관련 |
|------|------|
| 큐 시뮬레이션 | 요세푸스(1158), BFS 전반 |
| deque 활용 | BOJ 5430 (AC), 슬라이딩 윈도우 |

## CLRS 매핑
| Ch 10.1 | 큐의 배열 구현 |
