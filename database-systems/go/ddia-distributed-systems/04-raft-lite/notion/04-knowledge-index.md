# 지식 인덱스

## 핵심 용어
- `term`: 리더 선출과 권한을 구분하는 논리적 시간 단위입니다.
- `leader election`: 현재 term에서 어느 node가 leader인지 정하는 과정입니다.
- `commit index`: 충분히 복제되어 state machine에 적용해도 되는 log의 최대 index입니다.
- `step down`: 더 높은 term을 보고 leader나 candidate가 follower로 내려오는 동작입니다.
- `majority`: cluster 과반수 노드의 동의를 뜻하며 commit 판단의 기준이 됩니다.

## 다시 볼 파일
- `../internal/raft/raft.go`: `Node`, `Cluster`, term/state transition, append/commit 로직이 모두 모여 있습니다.
- `../tests/raft_test.go`: election, failover, commit, higher-term stepdown을 검증합니다.
- `../cmd/raft-lite/main.go`: 선출된 leader ID, commit index, log length를 출력합니다.
- `../docs/concepts/commit-rule.md`: 어느 시점에 commit index를 올릴 수 있는지 먼저 읽어 두면 좋습니다.

## 개념 문서
- `../docs/concepts/commit-rule.md`: commit index를 언제 올릴 수 있는지 설명합니다.
- `../docs/concepts/election-cycle.md`: term, vote, leader 전환 흐름을 요약합니다.

## 검증 앵커
- 확인일: 2026-03-10
- 테스트 파일: `../tests/raft_test.go`
- 다시 돌릴 테스트 이름: `TestLeaderElection`, `TestLeaderFailover`, `TestLogReplicationAndCommit`, `TestHigherTermForcesStepDown`
- 데모 경로: `../cmd/raft-lite/main.go`
- 데모가 보여 주는 장면: 선출된 leader ID, commit index, log length를 출력해 election과 commit이 한 번에 보이게 합니다.

- 더 긴 이전 기록은 `../notion-archive/`에 남겨 두고, 여기에는 다시 읽을 때 바로 쓸 정보만 남깁니다.
