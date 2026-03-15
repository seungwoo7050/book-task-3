# Structure Outline

## Chosen arc

1. failover가 아니라 ordered mutation stream replication이라는 범위를 먼저 잡는다.
2. demo와 추가 재실행으로 delete propagation과 duplicate replay를 먼저 보여 준다.
3. sequential offset, watermark fetch, idempotent apply, delete-as-mutation을 invariant로 정리한다.
4. 마지막에 election/quorum 부재를 분리해 과장을 막는다.

## Why this structure

- 이 랩은 구현량보다 invariant가 중요해서 파일 설명보다 semantics 중심 구조가 더 잘 맞는다.
- demo가 delete와 watermark를 동시에 보여 줘서 초반 evidence로 적합하다.
- unknown operation ignore는 source-only nuance라 invariant 장에서 분명히 적는 편이 좋다.

## Rejected alternatives

- replication 일반론을 길게 푸는 구조는 버렸다.
- consensus나 election을 미리 끌어오는 구조도 버렸다.
- network fault model을 상상으로 확장하는 서사는 현재 범위를 벗어나 제외했다.
