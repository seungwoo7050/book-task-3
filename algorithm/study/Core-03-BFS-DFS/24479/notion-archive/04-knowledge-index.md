# BOJ 24479 — 개념 인덱스

## 핵심 알고리즘

| 개념 | CLRS 참조 | 설명 |
|------|-----------|------|
| DFS | Ch 22.3 | 재귀 탐색, 발견 시각(d) 기록 |
| DFS 방문 순서 | Ch 22.3 | 정점별 방문 번호 — `u.d` 타임스탬프 |

## 자료구조 사용

- **인접 리스트**: 정렬 후 결정론적 DFS 순서 보장
- **result 배열**: 1-indexed, 방문 순서 저장
- **mutable 카운터**: `order = [0]` 패턴

## 시간 복잡도

- DFS 탐색: $O(V + E)$
- 인접 리스트 정렬: $O(V \cdot d \log d)$
- 출력: $O(V)$

## 연결 문제

- **BOJ 1260** (Core-03): DFS/BFS 기본 — 이 문제의 기반
- **BOJ 24480**: DFS 방문 순서 (내림차순) — 정렬 방향만 바꿈
- **BOJ 2252** (Core-0D): 위상 정렬 — DFS finishing time 활용
- **BOJ 11724**: 연결 요소 — DFS 응용

## Python 특이사항

- `sys.setrecursionlimit(200000)`: $N \leq 100,000$ 대응
- `nonlocal` vs 리스트 래핑: 클로저에서 mutable 변수 관리
- `'\n'.join(...)`: 대량 출력 최적화
