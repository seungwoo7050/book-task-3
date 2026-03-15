# leveled-compaction 문제지

## 왜 중요한가

입력 source 배열에서 newer-first 우선순위를 유지한 k-way merge를 수행해야 합니다. deepest level일 때만 tombstone을 제거해야 합니다. 새 SSTable 생성 후 manifest를 atomic write로 갱신해야 합니다. compaction이 끝나면 이전 입력 파일을 정리해야 합니다.

## 목표

시작 위치의 구현을 완성해 입력 source 배열에서 newer-first 우선순위를 유지한 k-way merge를 수행해야 합니다, deepest level일 때만 tombstone을 제거해야 합니다, 새 SSTable 생성 후 manifest를 atomic write로 갱신해야 합니다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../go/database-internals/projects/05-leveled-compaction/cmd/leveled-compaction/main.go`
- `../go/database-internals/projects/05-leveled-compaction/internal/compaction/compaction.go`
- `../go/database-internals/projects/05-leveled-compaction/internal/sstable/sstable.go`
- `../go/database-internals/projects/05-leveled-compaction/tests/compaction_test.go`

## starter code / 입력 계약

- `../go/database-internals/projects/05-leveled-compaction/cmd/leveled-compaction/main.go`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- 입력 source 배열에서 newer-first 우선순위를 유지한 k-way merge를 수행해야 합니다.
- deepest level일 때만 tombstone을 제거해야 합니다.
- 새 SSTable 생성 후 manifest를 atomic write로 갱신해야 합니다.
- compaction이 끝나면 이전 입력 파일을 정리해야 합니다.

## 제외 범위

- 상위 카탈로그 요약만 보고 세부 산출물 계약을 생략하지 않는다.

## 성공 체크리스트

- 핵심 흐름은 `main`와 `seed`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `TestKWayMergeKeepsNewerValue`와 `TestKWayMergeDropsTombstonesAtDeepestLevel`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `cd /Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/05-leveled-compaction && GOWORK=off go test ./...`가 통과한다.

## 검증 방법

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/05-leveled-compaction && GOWORK=off go test ./...
```

- Go 계열 검증은 `go` toolchain과 필요한 module checksum(`go.sum`)이 준비돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`leveled-compaction_answer.md`](leveled-compaction_answer.md)에서 확인한다.
