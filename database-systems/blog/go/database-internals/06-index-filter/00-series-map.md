# 06 Index Filter 시리즈 맵

이 시리즈는 Database Internals 트랙의 6번째 프로젝트 `06 Index Filter`를 따라간다. Bloom filter와 sparse index를 붙여 point lookup이 전체 SSTable 스캔으로 떨어지지 않도록 만듭니다. 기능 목록보다 먼저, 어떤 순서로 경계를 고정했는지 읽는 쪽에 무게를 두었다.

## 먼저 보고 갈 질문

- Bloom filter를 직렬화·복원할 수 있어야 합니다.
- 정렬된 key-offset 스트림에서 sparse index를 생성해야 합니다.

## 읽는 순서

1. [10-chronology-scope-and-surface.md](10-chronology-scope-and-surface.md) — 테스트 이름과 파일 배치부터 훑으면서 문제의 테두리를 다시 좁히는 글
2. [20-chronology-core-invariants.md](20-chronology-core-invariants.md) — 핵심 함수와 상태 전이에서 invariant가 실제로 어디서 잠기는지 따라가는 글
3. [30-chronology-verification-and-boundaries.md](30-chronology-verification-and-boundaries.md) — 테스트와 demo를 다시 돌려 약속 범위와 남는 한계를 정리하는 글

## 재검증 명령

```bash
GOWORK=off go test ./...
GOWORK=off go run ./cmd/index-filter
```

## 이번 시리즈가 근거로 삼은 파일

- `database-systems/go/database-internals/projects/06-index-filter/internal/sstable/sstable.go`
- `database-systems/go/database-internals/projects/06-index-filter/tests/index_filter_test.go`
- `database-systems/go/database-internals/projects/06-index-filter/README.md`
- `database-systems/go/database-internals/projects/06-index-filter/problem/README.md`
- `database-systems/go/database-internals/projects/06-index-filter/docs/README.md`
- `database-systems/go/database-internals/projects/06-index-filter/internal/bloomfilter/bloom_filter.go`
- `database-systems/go/database-internals/projects/06-index-filter/cmd/index-filter/main.go`

## 보조 메모

작업 메모가 꼭 필요할 때만 [_evidence-ledger.md](_evidence-ledger.md)와 [_structure-outline.md](_structure-outline.md)를 보면 된다. 공개 시리즈는 `00 -> 10 -> 20 -> 30`만 따라가면 충분하다.

## Git Anchor

- `2026-03-11 bbb6673 Track 1에 대한 전반적인 개선 완료`
