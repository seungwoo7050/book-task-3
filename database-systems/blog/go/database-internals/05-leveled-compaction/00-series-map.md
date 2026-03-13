# 05 Leveled Compaction 시리즈 맵

Database Internals 트랙의 5번째 슬롯인 `05 Leveled Compaction`에서는 L0의 겹치는 SSTable을 병합하고 manifest를 원자적으로 갱신해 leveled compaction의 핵심만 구현합니다. 이 시리즈는 결과 요약보다 실제 구현 순서가 어디서 선명해지는지 보여 주는 데 초점을 둔다.

## 먼저 보고 갈 질문

- 입력 source 배열에서 newer-first 우선순위를 유지한 k-way merge를 수행해야 합니다.
- deepest level일 때만 tombstone을 제거해야 합니다.

## 읽는 순서

1. [10-chronology-scope-and-surface.md](10-chronology-scope-and-surface.md) — 테스트 이름과 파일 배치부터 훑으면서 문제의 테두리를 다시 좁히는 글
2. [20-chronology-core-invariants.md](20-chronology-core-invariants.md) — 핵심 함수와 상태 전이에서 invariant가 실제로 어디서 잠기는지 따라가는 글
3. [30-chronology-verification-and-boundaries.md](30-chronology-verification-and-boundaries.md) — 테스트와 demo를 다시 돌려 약속 범위와 남는 한계를 정리하는 글

## 재검증 명령

```bash
GOWORK=off go test ./...
GOWORK=off go run ./cmd/leveled-compaction
```

## 이번 시리즈가 근거로 삼은 파일

- `database-systems/go/database-internals/projects/05-leveled-compaction/internal/sstable/sstable.go`
- `database-systems/go/database-internals/projects/05-leveled-compaction/tests/compaction_test.go`
- `database-systems/go/database-internals/projects/05-leveled-compaction/README.md`
- `database-systems/go/database-internals/projects/05-leveled-compaction/problem/README.md`
- `database-systems/go/database-internals/projects/05-leveled-compaction/docs/README.md`
- `database-systems/go/database-internals/projects/05-leveled-compaction/internal/compaction/compaction.go`
- `database-systems/go/database-internals/projects/05-leveled-compaction/cmd/leveled-compaction/main.go`

## 보조 메모

작업 메모가 꼭 필요할 때만 [_evidence-ledger.md](_evidence-ledger.md)와 [_structure-outline.md](_structure-outline.md)를 보면 된다. 공개 시리즈는 `00 -> 10 -> 20 -> 30`만 따라가면 충분하다.

## Git Anchor

- `2026-03-11 bbb6673 Track 1에 대한 전반적인 개선 완료`
