# 학습 노트 안내

한 key의 최신 값 하나만 보는 대신 version chain과 snapshot visibility를 도입해 transaction isolation을 설명하는 단계입니다.

## 이 노트를 읽기 전에 잡을 질문
- 같은 key에 대해 여러 transaction이 겹칠 때, 누가 어떤 version을 볼 수 있고 어떤 commit은 거절되어야 하는가?
- 이 트랙을 포트폴리오 설명으로 바꿀 때 어떤 장면을 남길 것인가?

## 권장 읽기 순서
1. `../problem/README.md`로 요구와 범위를 먼저 확인합니다.
2. `../internal/mvcc/mvcc.go`, `../tests/mvcc_test.go`, `../cmd/mvcc/main.go`를 열어 실제 구현 표면을 먼저 잡습니다.
3. `../tests/`에서 이 프로젝트가 무엇을 보장하는지 확인합니다. 핵심 테스트는 `TestBasicReadWrite`, `TestSnapshotIsolation`, `TestLatestCommittedValue`, `TestWriteWriteConflict`입니다.
4. 데모 경로 `../cmd/mvcc/main.go`를 실행해 전체 흐름을 빠르게 눈으로 확인합니다.
5. 마지막으로 `./00-problem-framing.md`부터 `./04-knowledge-index.md`까지 읽으며 판단과 연결 지점을 정리합니다.

## 이번 노트가 담는 것
- `00-problem-framing.md`: 같은 key에 대해 여러 transaction이 겹칠 때, 누가 어떤 version을 볼 수 있고 어떤 commit은 거절되어야 하는가?에 대한 범위와 성공 기준을 정리합니다.
- `01-approach-log.md`: key별 version chain을 저장한다, transaction 시작 시 snapshot을 고정한다 같은 실제 구현 선택을 기록합니다.
- `02-debug-log.md`: snapshot이 future commit을 읽어 버리는 경우, 동일 key write conflict를 놓치는 경우처럼 다시 깨질 수 있는 지점을 모아 둡니다.
- `03-retrospective.md`: 이 단계에서 얻은 것, 남긴 단순화, 다음 확장 방향을 정리합니다.
- `04-knowledge-index.md`: 용어, 핵심 파일, 개념 문서, 검증 앵커를 빠르게 다시 찾는 인덱스입니다.

## 검증 앵커
- 테스트: `TestBasicReadWrite`, `TestSnapshotIsolation`, `TestLatestCommittedValue`, `TestWriteWriteConflict`
- 데모 경로: `../cmd/mvcc/main.go`에서 `cmd/mvcc/main.go`는 concurrent transaction
- 데모가 보여 주는 장면: `t2`가 어떤 값을 보는지 출력합니다.
- 개념 문서: `../docs/concepts/snapshot-visibility.md`, `../docs/concepts/write-conflict.md`

- 이전 장문 기록은 `../notion-archive/`에 보존돼 있습니다.
