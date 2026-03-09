# 0x12 Red-Black Tree — 문제 프레이밍

## 첫인상

CLRS Ch 13 레드-블랙 트리. 균형 이진 탐색 트리의 대표격. 삽입 시 fixup rotations으로 $O(\log n)$ 보장.

## 프로젝트 구조

`Node` 클래스 (`__slots__`: key, color, left, right, parent) + `RBTree` 클래스. Sentinel nil 노드 사용. INSERT/FIND/INORDER 연산.

## 왜 이 프로젝트인가

STL `std::map`, Java `TreeMap` 등 언어 표준 라이브러리의 근간. 직접 구현해야 회전-재색칠 메커니즘이 체화된다.
