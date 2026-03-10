# 0x12 Red-Black Tree — 개발 타임라인

## Phase 1: Node / RBTree 스캐폴딩

`__slots__` 기반 Node 클래스, sentinel nil 초기화.

## Phase 2: 회전 + 삽입

CLRS 수도코드 → Python 번역. left_rotate, right_rotate, insert, insert_fixup.

## Phase 3: 조회 + 순회

find (BST 탐색), inorder (재귀).

## Phase 4: 테스트

```bash
make -C problem test
```

PASS.

## 사용 도구

- Python 3
- GNU Make
