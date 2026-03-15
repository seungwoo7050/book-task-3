# Structure Outline

## Core thesis

이 project의 핵심은 failure 종류 자체보다, quorum commit과 follower convergence가 분리되고 leader local visibility가 commit보다 앞선다는 점을 작은 replication harness에서 드러내는 데 있다.

## Writing plan

1. problem 문서로 leader-known replication 범위를 먼저 고정한다.
2. `Leader`, `Follower`, `NetworkHarness` 세 덩어리로 구현 지도를 잡는다.
3. `AppendPut`과 `advanceCommit`으로 eager leader apply와 quorum commit을 설명한다.
4. `HandleAppend`로 duplicate/retry idempotency를 설명한다.
5. test/demo/임시 visibility check로 검증과 한계를 마무리한다.

## Must-keep evidence

- `drop tick commit=0 node-2=-1 node-3=0`
- `recover tick commit=2 node-2=2 node-3=2`
- `duplicate tick commit=1 node-3-log=2 node-3-applied=2`
- `commit=-1 leader_read=true:1`
