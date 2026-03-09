# BOJ 1991 — 접근 과정

## 트리 표현

딕셔너리로 각 노드의 왼쪽/오른쪽 자식 저장:

```python
left = {}
right = {}
for _ in range(n):
    node, l, r = parts[0], parts[1], parts[2]
    left[node] = l
    right[node] = r
```

## 세 가지 순회

```python
def preorder(node):   # 루트 → 왼 → 오
    if node == '.': return
    result.append(node)
    preorder(left[node])
    preorder(right[node])

def inorder(node):    # 왼 → 루트 → 오
    if node == '.': return
    inorder(left[node])
    result.append(node)
    inorder(right[node])

def postorder(node):  # 왼 → 오 → 루트
    if node == '.': return
    postorder(left[node])
    postorder(right[node])
    result.append(node)
```

차이는 `result.append(node)`의 위치뿐.

## 시간/공간

- $O(N)$ 각 순회
