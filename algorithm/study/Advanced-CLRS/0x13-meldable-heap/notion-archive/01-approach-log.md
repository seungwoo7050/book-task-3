# 0x13 Meldable Heap — 접근 과정

## merge(a, b)

두 루트 중 작은 쪽을 루트로 삼고, 큰 쪽을 루트의 child 리스트 맨 앞에 연결.

## merge_pairs(node)

Pairing Heap의 핵심. Child 리스트를 두 개씩 짝지어 merge하고(left-to-right), 그 결과를 역순으로 다시 merge(right-to-left). 2-pass 방식.

```python
def merge_pairs(node):
    if node is None or node.sibling is None:
        return node
    a, b, rest = node, node.sibling, node.sibling.sibling
    a.sibling = b.sibling = None
    return merge(merge(a, b), merge_pairs(rest))
```

## PairingHeap 클래스

- `push(key)`: 새 Node 생성 후 root와 merge
- `pop()`: root 제거 후 children을 merge_pairs로 합침
- `meld(other)`: 두 힙의 root를 merge

## 다중 힙 관리

`heaps = {}` 딕셔너리로 이름별 힙 관리.
