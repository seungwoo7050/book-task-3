# BOJ 1717 — 회고

## 배운 것

Union-Find는 단순하지만 최적화가 중요한 자료구조. 경로 압축 하나로 $O(N)$ → $O(\alpha(N))$ 개선. 이 차이가 TLE와 AC의 경계.

## 1197 크루스칼과의 연결

이 문제의 Union-Find가 크루스칼의 핵심 부품. 독립적으로 연습한 후 MST에 적용하면 이해가 깊어진다.

## Path Splitting vs Path Halving vs Full Compression

- Full compression (재귀): 모든 노드를 루트 직속으로 → Python에서 스택 문제
- Path splitting (반복): 각 노드를 할아버지로 → 안전하고 충분히 빠름
- Path halving: 짝수 번째 노드만 → splitting과 비슷
