import sys
input = sys.stdin.readline

class Node:
    __slots__ = ("key", "child", "sibling")
    def __init__(self, key):
        self.key = key
        self.child = None
        self.sibling = None

def merge(a, b):
    if a is None:
        return b
    if b is None:
        return a
    if b.key < a.key:
        a, b = b, a
    b.sibling = a.child
    a.child = b
    return a

def merge_pairs(node):
    if node is None or node.sibling is None:
        return node
    first = node
    second = node.sibling
    rest = second.sibling
    first.sibling = None
    second.sibling = None
    return merge(merge(first, second), merge_pairs(rest))

class PairingHeap:
    def __init__(self):
        self.root = None
    def push(self, key):
        self.root = merge(self.root, Node(key))
    def pop(self):
        if self.root is None:
            return None
        ret = self.root.key
        self.root = merge_pairs(self.root.child)
        return ret
    def meld(self, other):
        self.root = merge(self.root, other.root)
        other.root = None

def solve():
    first = input().strip()
    if not first:
        return
    q = int(first)
    heaps = {}
    out = []
    for _ in range(q):
        parts = input().split()
        cmd = parts[0]
        if cmd == "MAKE":
            heaps[parts[1]] = PairingHeap()
        elif cmd == "PUSH":
            heaps[parts[1]].push(int(parts[2]))
        elif cmd == "MELD":
            heaps[parts[1]].meld(heaps[parts[2]])
        elif cmd == "POP":
            value = heaps[parts[1]].pop()
            out.append(str(value) if value is not None else "EMPTY")
    print("\n".join(out))

if __name__ == "__main__":
    solve()
