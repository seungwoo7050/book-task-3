# Red-Black Invariants

## CLRS Connection

CLRS Ch 13 uses red-black trees as the balanced BST that keeps height O(log n) via local rotations and recoloring.

## Study Notes

- root는 항상 black이다.
- red node는 red child를 가질 수 없다.
- 모든 root-to-leaf nil path는 같은 black height를 가진다.
- B-tree 대응 관계는 구현보다 disk model 이해가 더 중요하므로 reference reading에 남긴다.
