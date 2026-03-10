# 지식 인덱스

## 핵심 용어
- `MVCC`: 여러 version을 유지해 concurrent transaction이 서로 다른 snapshot을 읽게 하는 기법입니다.
- `version chain`: 한 key에 대해 시간순으로 쌓인 version 목록입니다.
- `snapshot isolation`: transaction 시작 시점의 committed state를 일관되게 읽는 규칙입니다.
- `first-committer-wins`: 같은 key를 두 transaction이 쓸 때 먼저 commit한 쪽만 성공시키는 충돌 규칙입니다.
- `GC`: 더 이상 어떤 active snapshot에서도 보이지 않는 오래된 version을 제거하는 작업입니다.

## 다시 볼 파일
- `../internal/mvcc/mvcc.go`: `VersionStore`, `TransactionManager`, commit/abort/GC 로직이 모두 모여 있습니다.
- `../tests/mvcc_test.go`: snapshot isolation, conflict, abort, GC가 어디서 깨지는지 바로 보여 줍니다.
- `../cmd/mvcc/main.go`: 동시 transaction에서 오래된 snapshot이 어떤 값을 보는지 간단히 보여 주는 데모입니다.
- `../docs/concepts/snapshot-visibility.md`: 어떤 version이 읽혀야 하는지 기준을 먼저 맞출 때 도움이 됩니다.

## 개념 문서
- `../docs/concepts/snapshot-visibility.md`: 트랜잭션 시작 시점 기준으로 어떤 version이 보이는지 설명합니다.
- `../docs/concepts/write-conflict.md`: first-committer-wins 충돌 규칙을 정리합니다.

## 검증 앵커
- 확인일: 2026-03-10
- 테스트 파일: `../tests/mvcc_test.go`
- 다시 돌릴 테스트 이름: `TestBasicReadWrite`, `TestSnapshotIsolation`, `TestLatestCommittedValue`, `TestWriteWriteConflict`, `TestDifferentKeysNoConflict`, `TestAbortAndDelete`, `TestGC`
- 데모 경로: `../cmd/mvcc/main.go`
- 데모가 보여 주는 장면: concurrent transaction에서 `t2`가 어떤 값을 보는지 출력합니다.

- 더 긴 이전 기록은 `../notion-archive/`에 남겨 두고, 여기에는 다시 읽을 때 바로 쓸 정보만 남깁니다.
