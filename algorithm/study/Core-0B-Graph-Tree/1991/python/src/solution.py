import sys
input = sys.stdin.readline

def main():
    n = int(input())
    left = {}
    right = {}
    for _ in range(n):
        parts = input().split()
        node, l, r = parts[0], parts[1], parts[2]
        left[node] = l
        right[node] = r

    result = []

    def preorder(node):
        if node == '.':
            return
        result.append(node)
        preorder(left[node])
        preorder(right[node])

    def inorder(node):
        if node == '.':
            return
        inorder(left[node])
        result.append(node)
        inorder(right[node])

    def postorder(node):
        if node == '.':
            return
        postorder(left[node])
        postorder(right[node])
        result.append(node)

    preorder('A')
    print(''.join(result))
    result.clear()
    inorder('A')
    print(''.join(result))
    result.clear()
    postorder('A')
    print(''.join(result))

if __name__ == "__main__":
    main()
