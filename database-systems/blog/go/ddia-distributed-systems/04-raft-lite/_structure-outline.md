# Structure Outline

## Chosen arc

1. production Raft가 아니라 consensus minimum viable semantics라는 범위를 먼저 잡는다.
2. demo와 추가 재실행으로 first leader, commit index, failover leader를 먼저 보여 준다.
3. election cycle, vote up-to-date rule, append consistency, majority commit, step-down을 invariant로 정리한다.
4. 마지막에는 persistence/snapshotting 부재를 분리해 과장을 막는다.

## Why this structure

- 이 랩은 구현량보다 term/log invariant가 중요해서 semantics 중심 구조가 맞다.
- deterministic election TTL은 docs와 source를 연결하는 좋은 포인트라 초반에 드러내는 편이 좋다.
- current-term commit rule은 쉽게 놓칠 수 있어 invariant 장의 중심으로 두는 편이 좋다.

## Rejected alternatives

- Raft 일반론을 길게 푸는 구조는 버렸다.
- 테스트 설명만 나열하는 구조도 버렸다.
- persistence나 snapshotting을 상상으로 확장하는 서사는 현재 범위를 벗어나 제외했다.
