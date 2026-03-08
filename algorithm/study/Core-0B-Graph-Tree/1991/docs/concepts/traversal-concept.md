# 이진 트리 순회 개념 정리

## CLRS 연결
CLRS Ch 12.1 — Binary Tree 순회:
- **전위(Preorder)**: 루트 → 왼쪽 → 오른쪽
- **중위(Inorder)**: 왼쪽 → 루트 → 오른쪽
- **후위(Postorder)**: 왼쪽 → 오른쪽 → 루트

## 시간 복잡도
모든 순회: $O(N)$ — 각 노드를 정확히 한 번 방문.

## 구현
딕셔너리로 `left[node]`, `right[node]` 저장.
재귀적 구현이 가장 직관적.
