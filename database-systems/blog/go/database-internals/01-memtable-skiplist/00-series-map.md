# 01 MemTable SkipList 시리즈 맵

`01 MemTable SkipList`은 Database Internals 트랙에서 1번째로 만나는 프로젝트다. LSM-Tree의 active memtable을 독립적인 SkipList로 구현해 정렬된 쓰기 경로와 tombstone semantics를 먼저 고정합니다. 여기서는 완성된 해설보다, 테스트와 코드가 어디서 같은 문제를 가리키는지 차례대로 따라간다.

## 먼저 보고 갈 질문

- `Put(key, value)`는 새 키를 삽입하거나 기존 키를 갱신하면서 key 오름차순을 유지해야 합니다.
- `Get(key)`는 존재하는 값, tombstone, 미존재를 구분해야 합니다.

## 읽는 순서

1. [10-chronology-scope-and-surface.md](10-chronology-scope-and-surface.md) — 테스트 이름과 파일 배치부터 훑으면서 문제의 테두리를 다시 좁히는 글
2. [20-chronology-core-invariants.md](20-chronology-core-invariants.md) — 핵심 함수와 상태 전이에서 invariant가 실제로 어디서 잠기는지 따라가는 글
3. [30-chronology-verification-and-boundaries.md](30-chronology-verification-and-boundaries.md) — 테스트와 demo를 다시 돌려 약속 범위와 남는 한계를 정리하는 글

## 재검증 명령

```bash
GOWORK=off go test ./...
GOWORK=off go run ./cmd/skiplist-demo
```

## 이번 시리즈가 근거로 삼은 파일

- `database-systems/go/database-internals/projects/01-memtable-skiplist/internal/skiplist/skiplist.go`
- `database-systems/go/database-internals/projects/01-memtable-skiplist/tests/skiplist_test.go`
- `database-systems/go/database-internals/projects/01-memtable-skiplist/README.md`
- `database-systems/go/database-internals/projects/01-memtable-skiplist/problem/README.md`
- `database-systems/go/database-internals/projects/01-memtable-skiplist/docs/README.md`
- `database-systems/go/database-internals/projects/01-memtable-skiplist/cmd/skiplist-demo/main.go`

## 보조 메모

작업 메모가 꼭 필요할 때만 [_evidence-ledger.md](_evidence-ledger.md)와 [_structure-outline.md](_structure-outline.md)를 보면 된다. 공개 시리즈는 `00 -> 10 -> 20 -> 30`만 따라가면 충분하다.

## Git Anchor

- `2026-03-11 bbb6673 Track 1에 대한 전반적인 개선 완료`
