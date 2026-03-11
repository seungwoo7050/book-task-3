# 학습 노트 안내

quorum consistency 다음에는 “누가 authority를 갖는가”를 따로 풀어야 합니다. 이 단계는 full Raft보다 작은 failure detector + leader election 모델로 그 질문만 분리합니다.

## 이 노트를 읽기 전에 잡을 질문
- heartbeat silence는 언제부터 장애 신호라고 부를 수 있는가?
- leader election이 없다면 stale authority는 어떤 식으로 남게 되는가?

## 권장 읽기 순서
1. `../problem/README.md`로 요구와 범위를 먼저 확인합니다.
2. `../internal/election/election.go`, `../tests/election_test.go`, `../cmd/leader-election/main.go`를 열어 구현 표면을 먼저 잡습니다.
3. `../tests/`에서 healthy heartbeat, failover, isolated node, recovered step-down을 확인합니다.
4. 마지막으로 `./00-problem-framing.md`부터 `./04-knowledge-index.md`까지 읽으며 판단과 연결 지점을 정리합니다.

## 이번 노트가 담는 것
- `00-problem-framing.md`: 왜 quorum consistency 다음에 election을 별도 단계로 두는지 정리합니다.
- `01-approach-log.md`: suspicion 단계 분리, 고정 timeout, majority-only promotion 같은 구현 선택
- `02-debug-log.md`: follower가 계속 suspect로 남거나 old leader가 안 물러나는 경우 같은 실패 징후
- `03-retrospective.md`: election만 떼어 내서 얻는 학습 이점과 남긴 단순화
- `04-knowledge-index.md`: 용어, 파일, 검증 앵커

## 검증 앵커
- 테스트: `TestHealthyLeaderKeepsSendingHeartbeats`, `TestLeaderFailureTriggersSingleReelection`, `TestIsolatedNodeCannotPromoteItself`, `TestHigherTermHeartbeatForcesOldLeaderToStepDown`
- 데모 경로: `../cmd/leader-election/main.go`
- 개념 문서: `../docs/concepts/heartbeat-failure-detector.md`, `../docs/concepts/majority-election.md`

- 이전 장문 기록은 `../notion-archive/`에 보존돼 있습니다.
