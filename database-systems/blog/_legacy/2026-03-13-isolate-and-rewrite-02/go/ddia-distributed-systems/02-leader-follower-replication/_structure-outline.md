# 02 Leader-Follower Replication — Structure Outline

최종 시리즈는 chronology를 매끈하게 재배열하지 않고, 범위 파악 -> 핵심 invariant -> 재검증과 경계의 순서를 유지한다.

## Planned Files

- `00-series-map.md`: 프로젝트 질문, 읽는 순서, source-of-truth 파일, 재검증 명령을 잡는 지도
- `10-chronology-scope-and-surface.md`: 파일 구조와 테스트 이름을 근거로 처음 가설이 바뀌는 구간
- `20-chronology-core-invariants.md`: `Append`와 `ReplicateOnce`가 실제로 invariant를 고정하는 구간
- `30-chronology-verification-and-boundaries.md`: `go test`/`pytest`와 demo 출력으로 경계를 확정하는 구간

## Article Goals

1. `10-chronology-scope-and-surface.md`
   범위를 `tests/`와 README에서 어떻게 다시 좁혔는지 보여 준다.
   코드 앵커: `TestReplicationLogAssignsSequentialOffsets`, `Append`
   CLI: `find internal tests cmd -type f | sort`, `rg -n "^func Test" tests`

2. `20-chronology-core-invariants.md`
   핵심 invariant가 `Append`와 `ReplicateOnce` 사이에서 어떻게 고정되는지 보여 준다.
   코드 앵커: `Append`, `ReplicateOnce`
   CLI: `rg -n "^(type|func) " internal cmd`, `rg -n "Append|ReplicateOnce" internal cmd`

3. `30-chronology-verification-and-boundaries.md`
   테스트와 demo를 모두 남겨, pass 신호와 공개 표면을 구분해 설명한다.
   코드 앵커: `TestReplicateOnceIncrementalAndDeletes`, `main.go`
   CLI: GOWORK=off go test ./...; GOWORK=off go run ./cmd/replication
