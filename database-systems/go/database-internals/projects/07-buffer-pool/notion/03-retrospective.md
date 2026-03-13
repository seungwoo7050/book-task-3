# 회고

## 이번 단계에서 명확해진 것
- buffer pool은 단순 캐시가 아니라 page life-cycle을 관리하는 계층이라는 점이 분명해졌습니다.
- eviction 정책만 맞아도 되는 것이 아니라, pin/dirty contract가 함께 맞아야 안전합니다.
- 디스크 page라는 물리 단위의 관심사는 앞선 LSM 계열 논리 단위와 성격이 다릅니다.

## 아직 단순화한 부분
- writeback scheduler와 flush ordering이 없어 dirty page 지속성은 완성되지 않았습니다.
- 동시성 제어가 없어 multi-threaded access 시나리오는 설명하지 못합니다.

## 다음에 확장한다면
- clock policy를 추가해 LRU와 비교하는 실험을 만들 수 있습니다.
- dirty page background flusher를 넣으면 recovery와 더 자연스럽게 연결됩니다.

## `08 BTree Index And Query Scan`으로 넘길 질문
- 같은 logical key라도 transaction 시점에 따라 다른 version이 보여야 할 때 page cache 위에는 무엇이 더 필요할까?
- buffer pool과 MVCC가 함께 있을 때 garbage collection은 어떤 단위를 기준으로 해야 할까?
