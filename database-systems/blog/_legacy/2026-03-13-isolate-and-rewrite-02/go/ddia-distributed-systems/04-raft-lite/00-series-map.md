# 04 Raft Lite — Series Map

leader election, vote rule, AppendEntries consistency, majority commit이 드러나는 작은 동기 Raft 시뮬레이터를 구현합니다. 이 시리즈는 기존 초안의 말투를 따라가지 않고, 실제 코드와 검증 신호를 다시 읽으면서 판단이 어디서 바뀌는지에만 집중한다.

## 이 프로젝트가 답하는 질문

- leader election과 단일 leader 보장을 재현해야 합니다.
- up-to-date log vote rule을 구현해야 합니다.

## 작업 산출물

- [_evidence-ledger.md](_evidence-ledger.md)
- [_structure-outline.md](_structure-outline.md)

## 읽는 순서

1. [10-chronology-scope-and-surface.md](10-chronology-scope-and-surface.md) — 파일 구조와 테스트 이름으로 범위를 다시 잡는 구간
2. [20-chronology-core-invariants.md](20-chronology-core-invariants.md) — 핵심 invariant를 코드 조각으로 고정하는 구간
3. [30-chronology-verification-and-boundaries.md](30-chronology-verification-and-boundaries.md) — 실제 pass 신호와 남은 경계를 정리하는 구간

## 참조한 실제 파일

- `database-systems/go/ddia-distributed-systems/projects/04-raft-lite/internal/raft/raft.go`
- `database-systems/go/ddia-distributed-systems/projects/04-raft-lite/tests/raft_test.go`
- `database-systems/go/ddia-distributed-systems/projects/04-raft-lite/README.md`
- `database-systems/go/ddia-distributed-systems/projects/04-raft-lite/problem/README.md`
- `database-systems/go/ddia-distributed-systems/projects/04-raft-lite/docs/README.md`
- `database-systems/go/ddia-distributed-systems/projects/04-raft-lite/cmd/raft-lite/main.go`

## 재검증 명령

```bash
GOWORK=off go test ./...
GOWORK=off go run ./cmd/raft-lite
```

## Git Anchor

- `2026-03-11 bbb6673 Track 1에 대한 전반적인 개선 완료`
