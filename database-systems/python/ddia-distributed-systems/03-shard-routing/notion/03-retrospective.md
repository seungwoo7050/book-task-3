# 회고

## 이번 단계에서 명확해진 것
- routing 문제는 replication과 별개로 떼어 놓을수록 설명이 쉬워집니다.
- virtual node는 “성능 최적화”가 아니라 균형 잡힌 분산을 위한 구조적 장치입니다.
- rebalance를 이동량 관점에서 보는 것이 consistent hashing의 장점을 가장 잘 보여 줍니다.

## 아직 단순화한 부분
- weight 기반 노드, multi-replica placement, health-aware routing은 없습니다.
- 실제 cluster membership 변경 프로토콜도 구현하지 않았습니다.

## 다음에 확장한다면
- weighted node와 replica-aware routing을 추가할 수 있습니다.
- hot key 분산이나 cache locality까지 고려하는 확장 실험을 할 수 있습니다.

## `04 Clustered KV Capstone`로 넘길 질문
- routing이 정해진 뒤 leader와 follower는 그 shard 안에서 어떻게 역할을 나눌까?
- leader가 죽었을 때 shard ownership은 누가 다시 결정할까?
