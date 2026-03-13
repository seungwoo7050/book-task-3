# Go Blog Index

Go 시리즈는 같은 주제를 더 잘게 쪼갠 프로젝트 단위로 따라가며 설계 질문을 선명하게 보는 데 초점을 둡니다. 현재 공개된 프로젝트는 16개다.

## 여기서 바로 들어가기 좋은 트랙

- [Database Internals](database-internals/README.md) — 메모리 자료구조에서 시작해 flush, recovery, compaction, buffer, MVCC까지 저장 엔진 내부 규칙을 한 단계씩 넓혀 갑니다.
- [DDIA Distributed Systems](ddia-distributed-systems/README.md) — RPC framing에서 출발해 replication, shard routing, leader election, clustered KV까지 분산 경로를 순서대로 잇습니다.

## 읽는 순서

1. 먼저 트랙 README에서 어떤 질문을 다루는지 확인한다.
2. 관심 있는 프로젝트의 `00-series-map.md`로 들어가 시리즈 전체 흐름과 재검증 명령을 잡는다.
3. 본문은 `10 -> 20 -> 30` 순서로 읽는다.
4. 더 촘촘한 작업 메모가 필요할 때만 `_evidence-ledger.md`, `_structure-outline.md`를 펼친다.
