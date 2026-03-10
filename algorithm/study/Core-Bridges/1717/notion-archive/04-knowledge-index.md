# BOJ 1717 — 개념 인덱스

## 핵심 알고리즘

| 개념 | CLRS 참조 | 설명 |
|------|-----------|------|
| Disjoint Set Union | Ch 21 | 합집합 + 집합 판별 |
| 경로 압축 | Ch 21.3 | find 시 트리 평탄화 |
| 유니온 바이 랭크 | Ch 21.3 | 작은 트리를 큰 트리 아래에 |

## 시간 복잡도

- $O(M \cdot \alpha(N))$ ≈ $O(M)$

## 연결 문제

- **BOJ 1197** (Core-0D): MST — Union-Find 활용
- **BOJ 4195**: 친구 네트워크 — Union-Find + 크기 관리
