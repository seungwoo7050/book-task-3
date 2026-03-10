# 회고

## 이번 단계에서 명확해진 것
- replication만으로는 authority 교체를 설명할 수 없고, term과 vote 규칙이 따로 필요합니다.
- commit은 append보다 더 강한 조건이며, majority rule을 코드로 명시해야 합니다.
- 학습용 in-memory 모델로도 Raft의 핵심 긴장은 충분히 드러납니다.

## 아직 단순화한 부분
- persistent log와 snapshot이 없어 실전 수준 recovery는 설명하지 못합니다.
- membership change와 network partition handling도 빠져 있습니다.

## 다음에 확장한다면
- log persistence와 snapshotting을 더해 storage layer와 연결할 수 있습니다.
- membership change를 넣어 운영에 가까운 cluster lifecycle을 실험할 수 있습니다.

## `05 Clustered KV Capstone`로 넘길 질문
- routing과 replication, durability를 하나의 KV 시스템 안에서 묶으면 어떤 인터페이스가 필요할까?
- clustered KV에서 leader election을 실제 write path에 붙이려면 무엇이 더 필요할까?
