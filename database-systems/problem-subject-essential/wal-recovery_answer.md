# wal-recovery 답안지

이 문서는 문제지를 다시 넘기지 않고도 해답을 재구성할 수 있도록, 실제 구현 파일과 테스트만 기준으로 정리한 답안지다.

## 한 줄 해답

시작 위치의 구현을 완성해 PUT/DELETE는 memtable 반영 전에 WAL에 먼저 기록돼야 합니다, 레코드는 checksum, type, key/value 길이, payload를 포함해야 합니다, replay는 첫 손상 레코드에서 멈추고 그 뒤는 버려야 합니다를 한 흐름으로 설명하고 검증한다. 핵심은 `main`와 `must`, `New` 흐름을 구현하고 테스트를 통과시키는 것이다.

## 문제를 푸는 핵심 전략

- PUT/DELETE는 memtable 반영 전에 WAL에 먼저 기록돼야 합니다.
- 레코드는 checksum, type, key/value 길이, payload를 포함해야 합니다.
- replay는 첫 손상 레코드에서 멈추고 그 뒤는 버려야 합니다.
- 첫 진입점은 `../go/database-internals/projects/04-wal-recovery/cmd/wal-recovery/main.go`이고, 여기서 `main`와 `must` 흐름을 먼저 붙잡은 뒤 나머지 파일로 확장한다.

## 코드 워크스루

- `../go/database-internals/projects/04-wal-recovery/cmd/wal-recovery/main.go`: `main`, `must`가 핵심 흐름과 상태 전이를 묶는다.
- `../go/database-internals/projects/04-wal-recovery/internal/skiplist/skiplist.go`: `New`, `newNode`, `Put`, `Delete`가 핵심 흐름과 상태 전이를 묶는다.
- `../go/database-internals/projects/04-wal-recovery/internal/sstable/sstable.go`: `New`, `Write`, `LoadIndex`, `Lookup`가 핵심 흐름과 상태 전이를 묶는다.
- `../go/database-internals/projects/04-wal-recovery/internal/store/store.go`: `New`, `Open`, `Put`, `Delete`가 핵심 흐름과 상태 전이를 묶는다.
- `../go/database-internals/projects/04-wal-recovery/internal/wal/wal.go`: `New`, `Open`, `AppendPut`, `AppendDelete`가 핵심 흐름과 상태 전이를 묶는다.
- `../go/database-internals/projects/04-wal-recovery/tests/wal_test.go`: `TestRecoverPutRecords`, `TestRecoverDeleteRecords`, `TestRecoverManyRecords`가 통과 조건과 회귀 포인트를 잠근다.
- `main` 구현은 `TestRecoverPutRecords` 등이 잠근 입력 계약과 상태 전이를 그대로 만족해야 한다.
- 회귀 게이트는 `cd /Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/04-wal-recovery && GOWORK=off go test ./...`이며, 핵심 상태 전이를 바꿀 때마다 중간 검증으로 다시 실행한다.

## 정답을 재구성하는 절차

1. `../go/database-internals/projects/04-wal-recovery/cmd/wal-recovery/main.go`를 먼저 열어 입력과 상태 전이의 기준점을 잡는다.
2. `TestRecoverPutRecords` 등이 요구하는 순서대로 핵심 상태 전이와 예외 흐름을 채운다.
3. `cd /Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/04-wal-recovery && GOWORK=off go test ./...`를 실행해 결과를 잠그고, 필요하면 남은 검증 명령까지 이어서 돌린다.

## 검증과 실패 포인트

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/04-wal-recovery && GOWORK=off go test ./...
```

- 상위 카탈로그나 보조 문서만 보고 구현을 추측하지 않고, 지금 열어 둔 source/test를 정답 근거로 고정한다.
- `TestRecoverPutRecords`와 `TestRecoverDeleteRecords`가 잠근 상태 전이와 입력 계약을 빼먹지 않는다.
- 완성 직전에만 한 번 돌리지 말고, 상태 전이를 건드릴 때마다 `cd /Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/04-wal-recovery && GOWORK=off go test ./...`로 회귀를 조기에 잡는다.

## 소스 근거

- `../go/database-internals/projects/04-wal-recovery/cmd/wal-recovery/main.go`
- `../go/database-internals/projects/04-wal-recovery/internal/skiplist/skiplist.go`
- `../go/database-internals/projects/04-wal-recovery/internal/sstable/sstable.go`
- `../go/database-internals/projects/04-wal-recovery/internal/store/store.go`
- `../go/database-internals/projects/04-wal-recovery/internal/wal/wal.go`
- `../go/database-internals/projects/04-wal-recovery/tests/wal_test.go`
