# 학습 노트 안내

leader-follower replication만으로는 리더 교체를 설명할 수 없기 때문에, in-memory cluster 위에서 Raft의 최소 election과 commit rule을 구현한 단계입니다.

## 이 노트를 읽기 전에 잡을 질문
- 여러 node 중 누가 leader인지 합의하고, 어떤 log index까지를 committed라고 불러도 되는지 어떻게 결정할 것인가?
- 다음 단계 `05 Clustered KV Capstone`에 무엇을 넘기는가?

## 권장 읽기 순서
1. `../problem/README.md`로 요구와 범위를 먼저 확인합니다.
2. `../internal/raft/raft.go`, `../tests/raft_test.go`, `../cmd/raft-lite/main.go`를 열어 실제 구현 표면을 먼저 잡습니다.
3. `../tests/`에서 이 프로젝트가 무엇을 보장하는지 확인합니다. 핵심 테스트는 `TestLeaderElection`, `TestLeaderFailover`, `TestLogReplicationAndCommit`, `TestHigherTermForcesStepDown`입니다.
4. 데모 경로 `../cmd/raft-lite/main.go`를 실행해 전체 흐름을 빠르게 눈으로 확인합니다.
5. 마지막으로 `./00-problem-framing.md`부터 `./04-knowledge-index.md`까지 읽으며 판단과 연결 지점을 정리합니다.

## 이번 노트가 담는 것
- `00-problem-framing.md`: 여러 node 중 누가 leader인지 합의하고, 어떤 log index까지를 committed라고 불러도 되는지 어떻게 결정할 것인가?에 대한 범위와 성공 기준을 정리합니다.
- `01-approach-log.md`: state transition을 `Node` 안에 명시적으로 둔다, leader authority와 commit rule을 한 흐름으로 묶는다 같은 실제 구현 선택을 기록합니다.
- `02-debug-log.md`: leader election이 반복되거나 leader가 둘 생기는 경우, 복제는 되었지만 commit index가 안 올라가는 경우처럼 다시 깨질 수 있는 지점을 모아 둡니다.
- `03-retrospective.md`: 이 단계에서 얻은 것, 남긴 단순화, 다음 확장 방향을 정리합니다.
- `04-knowledge-index.md`: 용어, 핵심 파일, 개념 문서, 검증 앵커를 빠르게 다시 찾는 인덱스입니다.

## 검증 앵커
- 테스트: `TestLeaderElection`, `TestLeaderFailover`, `TestLogReplicationAndCommit`, `TestHigherTermForcesStepDown`
- 데모 경로: `../cmd/raft-lite/main.go`
- 데모가 보여 주는 장면: 선출된 leader ID, commit index, log length를 출력해 election과 commit이 한 번에 보이게 합니다.
- 개념 문서: `../docs/concepts/commit-rule.md`, `../docs/concepts/election-cycle.md`

- 이전 장문 기록은 `../notion-archive/`에 보존돼 있습니다.
