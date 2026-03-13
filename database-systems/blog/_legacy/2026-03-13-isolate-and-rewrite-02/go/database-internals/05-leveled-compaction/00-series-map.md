# 05 Leveled Compaction — Series Map

L0의 겹치는 SSTable을 병합하고 manifest를 원자적으로 갱신해 leveled compaction의 핵심만 구현합니다. 이 시리즈는 기존 초안의 말투를 따라가지 않고, 실제 코드와 검증 신호를 다시 읽으면서 판단이 어디서 바뀌는지에만 집중한다.

## 이 프로젝트가 답하는 질문

- 입력 source 배열에서 newer-first 우선순위를 유지한 k-way merge를 수행해야 합니다.
- deepest level일 때만 tombstone을 제거해야 합니다.

## 작업 산출물

- [_evidence-ledger.md](_evidence-ledger.md)
- [_structure-outline.md](_structure-outline.md)

## 읽는 순서

1. [10-chronology-scope-and-surface.md](10-chronology-scope-and-surface.md) — 파일 구조와 테스트 이름으로 범위를 다시 잡는 구간
2. [20-chronology-core-invariants.md](20-chronology-core-invariants.md) — 핵심 invariant를 코드 조각으로 고정하는 구간
3. [30-chronology-verification-and-boundaries.md](30-chronology-verification-and-boundaries.md) — 실제 pass 신호와 남은 경계를 정리하는 구간

## 참조한 실제 파일

- `database-systems/go/database-internals/projects/05-leveled-compaction/internal/sstable/sstable.go`
- `database-systems/go/database-internals/projects/05-leveled-compaction/tests/compaction_test.go`
- `database-systems/go/database-internals/projects/05-leveled-compaction/README.md`
- `database-systems/go/database-internals/projects/05-leveled-compaction/problem/README.md`
- `database-systems/go/database-internals/projects/05-leveled-compaction/docs/README.md`
- `database-systems/go/database-internals/projects/05-leveled-compaction/internal/compaction/compaction.go`
- `database-systems/go/database-internals/projects/05-leveled-compaction/cmd/leveled-compaction/main.go`

## 재검증 명령

```bash
GOWORK=off go test ./...
GOWORK=off go run ./cmd/leveled-compaction
```

## Git Anchor

- `2026-03-11 bbb6673 Track 1에 대한 전반적인 개선 완료`
