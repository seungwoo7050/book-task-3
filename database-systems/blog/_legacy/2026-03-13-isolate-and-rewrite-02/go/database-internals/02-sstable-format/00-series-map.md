# 02 SSTable Format — Series Map

immutable SSTable 파일 형식, sparse key index, footer metadata를 구현해 on-disk lookup의 기본을 고정합니다. 이 시리즈는 기존 초안의 말투를 따라가지 않고, 실제 코드와 검증 신호를 다시 읽으면서 판단이 어디서 바뀌는지에만 집중한다.

## 이 프로젝트가 답하는 질문

- data section은 key 오름차순 record의 연속 바이트 배열이어야 합니다.
- index section은 `(key, offset)` 쌍을 저장해 point lookup 시작 위치를 알려야 합니다.

## 작업 산출물

- [_evidence-ledger.md](_evidence-ledger.md)
- [_structure-outline.md](_structure-outline.md)

## 읽는 순서

1. [10-chronology-scope-and-surface.md](10-chronology-scope-and-surface.md) — 파일 구조와 테스트 이름으로 범위를 다시 잡는 구간
2. [20-chronology-core-invariants.md](20-chronology-core-invariants.md) — 핵심 invariant를 코드 조각으로 고정하는 구간
3. [30-chronology-verification-and-boundaries.md](30-chronology-verification-and-boundaries.md) — 실제 pass 신호와 남은 경계를 정리하는 구간

## 참조한 실제 파일

- `database-systems/go/database-internals/projects/02-sstable-format/internal/sstable/sstable.go`
- `database-systems/go/database-internals/projects/02-sstable-format/tests/sstable_test.go`
- `database-systems/go/database-internals/projects/02-sstable-format/README.md`
- `database-systems/go/database-internals/projects/02-sstable-format/problem/README.md`
- `database-systems/go/database-internals/projects/02-sstable-format/docs/README.md`
- `database-systems/go/database-internals/projects/02-sstable-format/cmd/sstable-format/main.go`

## 재검증 명령

```bash
GOWORK=off go test ./...
GOWORK=off go run ./cmd/sstable-format
```

## Git Anchor

- `2026-03-11 bbb6673 Track 1에 대한 전반적인 개선 완료`
