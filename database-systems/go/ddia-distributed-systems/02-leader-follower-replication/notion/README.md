# 학습 노트 안내

consensus를 넣기 전 단계에서 append-only mutation log와 watermark 기반 incremental sync만으로 leader-follower replication을 보여 주는 프로젝트입니다.

## 이 노트를 읽기 전에 잡을 질문
- follower가 중간에 끊겼다가 다시 붙어도 leader log에서 필요한 부분만 안전하게 따라오게 하려면 어떤 상태를 기억해야 하는가?
- 다음 단계 `03 Shard Routing`에 무엇을 넘기는가?

## 권장 읽기 순서
1. `../problem/README.md`로 요구와 범위를 먼저 확인합니다.
2. `../internal/replication/replication.go`, `../tests/replication_test.go`, `../cmd/replication/main.go`를 열어 실제 구현 표면을 먼저 잡습니다.
3. `../tests/`에서 이 프로젝트가 무엇을 보장하는지 확인합니다. 핵심 테스트는 `TestReplicationLogAssignsSequentialOffsets`, `TestFollowerApplyIsIdempotent`, `TestReplicateOnceIncrementalAndDeletes`입니다.
4. 데모 경로 `../cmd/replication/main.go`를 실행해 전체 흐름을 빠르게 눈으로 확인합니다.
5. 마지막으로 `./00-problem-framing.md`부터 `./04-knowledge-index.md`까지 읽으며 판단과 연결 지점을 정리합니다.

## 이번 노트가 담는 것
- `00-problem-framing.md`: follower가 중간에 끊겼다가 다시 붙어도 leader log에서 필요한 부분만 안전하게 따라오게 하려면 어떤 상태를 기억해야 하는가?에 대한 범위와 성공 기준을 정리합니다.
- `01-approach-log.md`: append-only log에 연속 offset을 부여한다, follower는 watermark 이전 entry를 건너뛴다 같은 실제 구현 선택을 기록합니다.
- `02-debug-log.md`: offset가 비거나 역전되는 경우, duplicate delivery가 follower 상태를 또 바꾸는 경우처럼 다시 깨질 수 있는 지점을 모아 둡니다.
- `03-retrospective.md`: 이 단계에서 얻은 것, 남긴 단순화, 다음 확장 방향을 정리합니다.
- `04-knowledge-index.md`: 용어, 핵심 파일, 개념 문서, 검증 앵커를 빠르게 다시 찾는 인덱스입니다.

## 검증 앵커
- 테스트: `TestReplicationLogAssignsSequentialOffsets`, `TestFollowerApplyIsIdempotent`, `TestReplicateOnceIncrementalAndDeletes`
- 데모 경로: `../cmd/replication/main.go`
- 데모가 보여 주는 장면: delete 이후 follower 상태와 watermark를 출력합니다.
- 개념 문서: `../docs/concepts/idempotent-follower.md`, `../docs/concepts/log-shipping.md`

- 이전 장문 기록은 `../notion-archive/`에 보존돼 있습니다.
