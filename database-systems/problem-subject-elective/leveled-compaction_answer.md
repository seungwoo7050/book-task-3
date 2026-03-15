# leveled-compaction 답안지

이 문서는 문제지를 다시 넘기지 않고도 해답을 재구성할 수 있도록, 실제 구현 파일과 테스트만 기준으로 정리한 답안지다.

## 한 줄 해답

시작 위치의 구현을 완성해 입력 source 배열에서 newer-first 우선순위를 유지한 k-way merge를 수행해야 합니다, deepest level일 때만 tombstone을 제거해야 합니다, 새 SSTable 생성 후 manifest를 atomic write로 갱신해야 합니다를 한 흐름으로 설명하고 검증한다. 핵심은 `main`와 `seed`, `deref` 흐름을 구현하고 테스트를 통과시키는 것이다.

## 문제를 푸는 핵심 전략

- 입력 source 배열에서 newer-first 우선순위를 유지한 k-way merge를 수행해야 합니다.
- deepest level일 때만 tombstone을 제거해야 합니다.
- 새 SSTable 생성 후 manifest를 atomic write로 갱신해야 합니다.
- 첫 진입점은 `../go/database-internals/projects/05-leveled-compaction/cmd/leveled-compaction/main.go`이고, 여기서 `main`와 `seed` 흐름을 먼저 붙잡은 뒤 나머지 파일로 확장한다.

## 코드 워크스루

- `../go/database-internals/projects/05-leveled-compaction/cmd/leveled-compaction/main.go`: `main`, `seed`, `deref`가 핵심 흐름과 상태 전이를 묶는다.
- `../go/database-internals/projects/05-leveled-compaction/internal/compaction/compaction.go`: `New`, `AddToLevel`, `NeedsL0Compaction`, `CompactL0ToL1`가 핵심 흐름과 상태 전이를 묶는다.
- `../go/database-internals/projects/05-leveled-compaction/internal/sstable/sstable.go`: `New`, `Write`, `LoadIndex`, `Get`가 핵심 흐름과 상태 전이를 묶는다.
- `../go/database-internals/projects/05-leveled-compaction/tests/compaction_test.go`: `TestKWayMergeKeepsNewerValue`, `TestKWayMergeDropsTombstonesAtDeepestLevel`, `TestCompactL0ToL1`가 통과 조건과 회귀 포인트를 잠근다.
- `main` 구현은 `TestKWayMergeKeepsNewerValue` 등이 잠근 입력 계약과 상태 전이를 그대로 만족해야 한다.
- 회귀 게이트는 `cd /Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/05-leveled-compaction && GOWORK=off go test ./...`이며, 핵심 상태 전이를 바꿀 때마다 중간 검증으로 다시 실행한다.

## 정답을 재구성하는 절차

1. `../go/database-internals/projects/05-leveled-compaction/cmd/leveled-compaction/main.go`를 먼저 열어 입력과 상태 전이의 기준점을 잡는다.
2. `TestKWayMergeKeepsNewerValue` 등이 요구하는 순서대로 핵심 상태 전이와 예외 흐름을 채운다.
3. `cd /Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/05-leveled-compaction && GOWORK=off go test ./...`를 실행해 결과를 잠그고, 필요하면 남은 검증 명령까지 이어서 돌린다.

## 검증과 실패 포인트

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/05-leveled-compaction && GOWORK=off go test ./...
```

- 상위 카탈로그나 보조 문서만 보고 구현을 추측하지 않고, 지금 열어 둔 source/test를 정답 근거로 고정한다.
- `TestKWayMergeKeepsNewerValue`와 `TestKWayMergeDropsTombstonesAtDeepestLevel`가 잠근 상태 전이와 입력 계약을 빼먹지 않는다.
- 완성 직전에만 한 번 돌리지 말고, 상태 전이를 건드릴 때마다 `cd /Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/05-leveled-compaction && GOWORK=off go test ./...`로 회귀를 조기에 잡는다.

## 소스 근거

- `../go/database-internals/projects/05-leveled-compaction/cmd/leveled-compaction/main.go`
- `../go/database-internals/projects/05-leveled-compaction/internal/compaction/compaction.go`
- `../go/database-internals/projects/05-leveled-compaction/internal/sstable/sstable.go`
- `../go/database-internals/projects/05-leveled-compaction/tests/compaction_test.go`
