# 04 Raft Lite 시리즈 맵

DDIA Distributed Systems 트랙의 4번째 슬롯인 `04 Raft Lite`에서는 leader election, vote rule, AppendEntries consistency, majority commit이 드러나는 작은 동기 Raft 시뮬레이터를 구현합니다. 이 시리즈는 결과 요약보다 실제 구현 순서가 어디서 선명해지는지 보여 주는 데 초점을 둔다.

## 먼저 보고 갈 질문

- leader election과 단일 leader 보장을 재현해야 합니다.
- up-to-date log vote rule을 구현해야 합니다.

## 읽는 순서

1. [10-chronology-scope-and-surface.md](10-chronology-scope-and-surface.md) — 테스트 이름과 파일 배치부터 훑으면서 문제의 테두리를 다시 좁히는 글
2. [20-chronology-core-invariants.md](20-chronology-core-invariants.md) — 핵심 함수와 상태 전이에서 invariant가 실제로 어디서 잠기는지 따라가는 글
3. [30-chronology-verification-and-boundaries.md](30-chronology-verification-and-boundaries.md) — 테스트와 demo를 다시 돌려 약속 범위와 남는 한계를 정리하는 글

## 재검증 명령

```bash
GOWORK=off go test ./...
GOWORK=off go run ./cmd/raft-lite
```

## 이번 시리즈가 근거로 삼은 파일

- `database-systems/go/ddia-distributed-systems/projects/04-raft-lite/internal/raft/raft.go`
- `database-systems/go/ddia-distributed-systems/projects/04-raft-lite/tests/raft_test.go`
- `database-systems/go/ddia-distributed-systems/projects/04-raft-lite/README.md`
- `database-systems/go/ddia-distributed-systems/projects/04-raft-lite/problem/README.md`
- `database-systems/go/ddia-distributed-systems/projects/04-raft-lite/docs/README.md`
- `database-systems/go/ddia-distributed-systems/projects/04-raft-lite/cmd/raft-lite/main.go`

## 보조 메모

작업 메모가 꼭 필요할 때만 [_evidence-ledger.md](_evidence-ledger.md)와 [_structure-outline.md](_structure-outline.md)를 보면 된다. 공개 시리즈는 `00 -> 10 -> 20 -> 30`만 따라가면 충분하다.

## Git Anchor

- `2026-03-11 bbb6673 Track 1에 대한 전반적인 개선 완료`
