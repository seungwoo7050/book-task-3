import sys
input = sys.stdin.readline

class Node:
    __slots__ = ("key", "color", "left", "right", "parent")
    def __init__(self, key=None, color="BLACK"):
        self.key = key
        self.color = color
        self.left = None
        self.right = None
        self.parent = None

class RBTree:
    def __init__(self):
        self.nil = Node()
        self.nil.left = self.nil.right = self.nil.parent = self.nil
        self.root = self.nil

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.nil:
            y.left.parent = x
        y.parent = x.parent
        if x.parent == self.nil:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, y):
        x = y.left
        y.left = x.right
        if x.right != self.nil:
            x.right.parent = y
        x.parent = y.parent
        if y.parent == self.nil:
            self.root = x
        elif y == y.parent.right:
            y.parent.right = x
        else:
            y.parent.left = x
        x.right = y
        y.parent = x

    def insert(self, key):
        z = Node(key, "RED")
        z.left = z.right = self.nil
        y = self.nil
        x = self.root
        while x != self.nil:
            y = x
            if key == x.key:
                return
            if key < x.key:
                x = x.left
            else:
                x = x.right
        z.parent = y
        if y == self.nil:
            self.root = z
        elif key < y.key:
            y.left = z
        else:
            y.right = z
        self.insert_fixup(z)

    def insert_fixup(self, z):
        while z.parent.color == "RED":
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right
                if y.color == "RED":
                    z.parent.color = y.color = "BLACK"
                    z.parent.parent.color = "RED"
                    z = z.parent.parent
                else:
                    if z == z.parent.right:
                        z = z.parent
                        self.left_rotate(z)
                    z.parent.color = "BLACK"
                    z.parent.parent.color = "RED"
                    self.right_rotate(z.parent.parent)
            else:
                y = z.parent.parent.left
                if y.color == "RED":
                    z.parent.color = y.color = "BLACK"
                    z.parent.parent.color = "RED"
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        z = z.parent
                        self.right_rotate(z)
                    z.parent.color = "BLACK"
                    z.parent.parent.color = "RED"
                    self.left_rotate(z.parent.parent)
        self.root.color = "BLACK"
        self.root.parent = self.nil

    def find(self, key):
        x = self.root
        while x != self.nil:
            if key == x.key:
                return True
            x = x.left if key < x.key else x.right
        return False

    def inorder(self):
        out = []
        def dfs(node):
            if node == self.nil:
                return
            dfs(node.left)
            out.append(str(node.key))
            dfs(node.right)
        dfs(self.root)
        return " ".join(out) if out else "EMPTY"

    def validate(self):
        if self.root == self.nil:
            return True
        if self.root.color != "BLACK":
            return False

        def dfs(node, lo, hi):
            if node == self.nil:
                return True, 1
            if (lo is not None and node.key <= lo) or (hi is not None and node.key >= hi):
                return False, 0
            if node.color == "RED" and (node.left.color == "RED" or node.right.color == "RED"):
                return False, 0
            ok_l, bh_l = dfs(node.left, lo, node.key)
            ok_r, bh_r = dfs(node.right, node.key, hi)
            if not ok_l or not ok_r or bh_l != bh_r:
                return False, 0
            return True, bh_l + (1 if node.color == "BLACK" else 0)

        ok, _ = dfs(self.root, None, None)
        return ok

def solve():
    first = input().strip()
    if not first:
        return
    q = int(first)
    tree = RBTree()
    out = []
    for _ in range(q):
        parts = input().split()
        cmd = parts[0]
        if cmd == "INSERT":
            tree.insert(int(parts[1]))
        elif cmd == "FIND":
            out.append("FOUND" if tree.find(int(parts[1])) else "NOT_FOUND")
        elif cmd == "INORDER":
            out.append(tree.inorder())
        elif cmd == "VALIDATE":
            out.append("YES" if tree.validate() else "NO")
    print("\n".join(out))

if __name__ == "__main__":
    solve()
