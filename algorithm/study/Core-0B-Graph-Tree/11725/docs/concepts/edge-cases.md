# 경계 사례 점검 — BOJ 11725 Tree Parent

## 1. 한쪽으로 치우친 트리 (사슬)
BFS 큐가 $O(N)$ 크기.

## 2. 루트의 자식이 1개
일직선 트리.

## 3. 완전 이진 트리
깊이 $O(\log N)$.

## 핵심 주의점
- DFS 사용 시 재귀 깊이 $10^5$ → `sys.setrecursionlimit` 필요
- BFS가 안전한 선택
