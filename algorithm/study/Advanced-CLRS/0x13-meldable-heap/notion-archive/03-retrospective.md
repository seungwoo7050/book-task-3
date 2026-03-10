# 0x13 Meldable Heap — 회고

## 배운 것

- Pairing Heap은 Fibonacci Heap과 유사한 amortized 성능을 단순한 구조로 달성
- merge_pairs의 2-pass가 성능의 열쇠 — 단순 순차 merge는 $O(n)$ 퇴화 가능
- child-sibling 표현으로 임의 차수 트리를 이진 구조로 관리

## 실무 연결

Boost C++의 `boost::heap::pairing_heap` 등 실제 라이브러리에 채택된 구조.
