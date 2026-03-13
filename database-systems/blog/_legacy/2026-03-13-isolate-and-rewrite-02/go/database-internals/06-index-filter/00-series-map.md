# 06 Index Filter — Series Map

Bloom filter와 sparse index를 붙여 point lookup이 전체 SSTable 스캔으로 떨어지지 않도록 만듭니다. 이 시리즈는 기존 초안의 말투를 따라가지 않고, 실제 코드와 검증 신호를 다시 읽으면서 판단이 어디서 바뀌는지에만 집중한다.

## 이 프로젝트가 답하는 질문

- Bloom filter를 직렬화·복원할 수 있어야 합니다.
- 정렬된 key-offset 스트림에서 sparse index를 생성해야 합니다.

## 작업 산출물

- [_evidence-ledger.md](_evidence-ledger.md)
- [_structure-outline.md](_structure-outline.md)

## 읽는 순서

1. [10-chronology-scope-and-surface.md](10-chronology-scope-and-surface.md) — 파일 구조와 테스트 이름으로 범위를 다시 잡는 구간
2. [20-chronology-core-invariants.md](20-chronology-core-invariants.md) — 핵심 invariant를 코드 조각으로 고정하는 구간
3. [30-chronology-verification-and-boundaries.md](30-chronology-verification-and-boundaries.md) — 실제 pass 신호와 남은 경계를 정리하는 구간

## 참조한 실제 파일

- `database-systems/go/database-internals/projects/06-index-filter/internal/sstable/sstable.go`
- `database-systems/go/database-internals/projects/06-index-filter/tests/index_filter_test.go`
- `database-systems/go/database-internals/projects/06-index-filter/README.md`
- `database-systems/go/database-internals/projects/06-index-filter/problem/README.md`
- `database-systems/go/database-internals/projects/06-index-filter/docs/README.md`
- `database-systems/go/database-internals/projects/06-index-filter/internal/bloomfilter/bloom_filter.go`
- `database-systems/go/database-internals/projects/06-index-filter/cmd/index-filter/main.go`

## 재검증 명령

```bash
GOWORK=off go test ./...
GOWORK=off go run ./cmd/index-filter
```

## Git Anchor

- `2026-03-11 bbb6673 Track 1에 대한 전반적인 개선 완료`
