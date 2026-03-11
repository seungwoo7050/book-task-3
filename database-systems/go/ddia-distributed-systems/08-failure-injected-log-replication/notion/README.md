# 학습 노트 안내

leader election 다음에는 실제 write가 failure를 만나도 어떻게 수렴하는지 보여 줘야 합니다. 이 단계는 full Raft 대신 append/ack replication과 작은 장애 하네스만 남겨 그 질문을 분리합니다.

## 이 노트를 읽기 전에 잡을 질문
- quorum commit과 follower convergence는 왜 같은 말이 아닌가?
- retry와 duplicate handling이 없으면 partial failure 뒤에 어떤 문제가 남는가?

## 권장 읽기 순서
1. `../problem/README.md`로 요구와 범위를 먼저 확인합니다.
2. `../internal/replication/replication.go`, `../tests/replication_test.go`, `../cmd/failure-replication/main.go`를 열어 구현 표면을 먼저 잡습니다.
3. `../tests/`에서 drop, duplicate, pause, recovery가 각각 어떤 보장을 검증하는지 확인합니다.
4. 마지막으로 `./00-problem-framing.md`부터 `./04-knowledge-index.md`까지 읽으며 판단과 연결 지점을 정리합니다.

## 이번 노트가 담는 것
- `00-problem-framing.md`: 왜 election 다음에 failure-injected replication을 따로 두는지 정리합니다.
- `01-approach-log.md`: explicit message type, scripted harness, nextIndex retry 같은 구현 선택을 기록합니다.
- `02-debug-log.md`: duplicate apply, stalled follower, commit index 정체 같은 실패 징후를 모읍니다.
- `03-retrospective.md`: quorum commit과 convergence를 분리해 얻는 학습 이점을 정리합니다.
- `04-knowledge-index.md`: 용어, 핵심 파일, 검증 앵커를 빠르게 다시 찾는 인덱스입니다.

## 검증 앵커
- 테스트: `TestDroppedAppendRetriesUntilFollowerConverges`, `TestDuplicateAppendIsIdempotent`, `TestPausedFollowerLagsButRecoversAfterResume`
- 데모 경로: `../cmd/failure-replication/main.go`
- 개념 문서: `../docs/concepts/failure-injection-harness.md`, `../docs/concepts/quorum-commit-and-retry.md`

- 이전 장문 기록은 `../notion-archive/`에 보존돼 있습니다.
