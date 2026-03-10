# 0x13 Meldable Heap — 문제 프레이밍

## 첫인상

CLRS Ch 19 기반, Pairing Heap 구현. 병합(meld) 가능한 힙으로 Fibonacci Heap의 실용적 대안.

## 프로젝트 구조

`Node` (key, child, sibling) + `PairingHeap` 클래스. 여러 이름의 힙을 dict로 관리. PUSH/POP/MELD 연산.

## 왜 이 프로젝트인가

다익스트라 decrease-key 등에 이론적 우위를 갖는 mergeable heap. Fibonacci Heap은 구현이 극도로 복잡하지만, Pairing Heap은 상대적으로 단순하면서 실측 성능 우수.
