# Structure Outline

## Core thesis

이 lab의 핵심은 full consensus가 아니라, heartbeat silence와 majority vote만으로 authority가 어떻게 옮겨 가는지 결정적 tick 시뮬레이션으로 보여 주는 데 있다.

## Writing plan

1. problem 문서로 election-only 범위를 먼저 고정한다.
2. `NewCluster`의 fixed TTL ladder로 deterministic leader selection을 설명한다.
3. `Tick`으로 suspicion/election 분리를 설명한다.
4. `startElection`과 `HandleHeartbeat`로 majority와 step-down을 설명한다.
5. demo와 테스트로 검증 및 한계를 정리한다.

## Must-keep evidence

- `tick=4 leader=node-1 term=1`
- `tick=8 suspected=[node-2]`
- `tick=9 reelected=node-2 term=2`
- `recovered=node-1 state=follower term=2`
- `TestIsolatedNodeCannotPromoteItself`
