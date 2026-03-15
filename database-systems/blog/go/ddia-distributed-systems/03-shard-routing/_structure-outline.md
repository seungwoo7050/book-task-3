# Structure Outline

## Chosen arc

1. control plane가 아니라 placement function과 rebalance accounting이라는 범위를 먼저 잡는다.
2. demo와 추가 재실행으로 distribution과 moved-key 숫자를 먼저 보여 준다.
3. virtual node insertion, wrap-around lookup, moved-key diffing을 invariant로 정리한다.
4. 마지막에는 gossip/data movement 부재를 분리한다.

## Why this structure

- 이 랩은 key별 예시보다 aggregate distribution과 reassignment cost가 더 중요해서 수치 중심 구조가 맞다.
- batch routing output도 실제로는 fan-out shape를 보여 주므로 초반 evidence로 가치가 있다.
- duplicate add/remove idempotency는 source-only nuance라 invariant 장에서 분명히 적는 편이 좋다.

## Rejected alternatives

- sharding 일반론을 길게 푸는 구조는 버렸다.
- demo 결과만 중심에 두는 구조도 버렸다.
- replication factor나 relocation worker를 상상으로 확장하는 서사는 현재 범위를 벗어나 제외했다.
