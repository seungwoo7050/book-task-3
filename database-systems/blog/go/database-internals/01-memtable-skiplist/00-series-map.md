# 01 MemTable SkipList

## 이 랩의 실제 목적

이 프로젝트는 SkipList 자료구조 자체를 뽐내는 과제가 아니다. 소스와 테스트를 다시 읽으면 더 정확한 목표는 LSM write path의 첫 단계인 MemTable semantics를 고정하는 데 있다. key는 항상 정렬된 순서로 유지돼야 하고, delete는 physical remove가 아니라 tombstone이어야 하며, ordered iteration과 대략적인 byte-size accounting이 다음 flush 판단의 재료가 된다.

즉 여기서 중요한 질문은 "SkipList를 구현했는가"보다 "flush 이전의 in-memory state가 어떤 계약을 만족해야 SSTable, recovery, compaction으로 이어질 수 있는가"에 가깝다.

이번 시리즈는 기존 blog를 입력 근거로 쓰지 않고 [`problem/README.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/01-memtable-skiplist/problem/README.md), [`skiplist.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/01-memtable-skiplist/internal/skiplist/skiplist.go), [`skiplist_test.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/01-memtable-skiplist/tests/skiplist_test.go), [`main.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/01-memtable-skiplist/cmd/skiplist-demo/main.go), 그리고 2026-03-14 재실행 결과만으로 다시 썼다.

## 이번에 붙드는 질문

- ordered write structure는 어떤 invariant를 유지해야 하는가
- tombstone은 왜 remove보다 중요한가
- update와 delete 뒤 logical size와 byte size는 어떻게 달라지는가
- 이 구현이 아직 일부러 다루지 않는 운영 문제는 무엇인가

## 문서 지도

- [10-chronology-scope-and-surface.md](/Users/woopinbell/work/book-task-3/database-systems/blog/go/database-internals/01-memtable-skiplist/10-chronology-scope-and-surface.md): 문제 범위와 SkipList surface를 시간순으로 정리한다.
- [20-chronology-core-invariants.md](/Users/woopinbell/work/book-task-3/database-systems/blog/go/database-internals/01-memtable-skiplist/20-chronology-core-invariants.md): sorted level-0 list, tombstone semantics, byte-size accounting, deterministic level generation을 소스 기준으로 해부한다.
- [30-chronology-verification-and-boundaries.md](/Users/woopinbell/work/book-task-3/database-systems/blog/go/database-internals/01-memtable-skiplist/30-chronology-verification-and-boundaries.md): go test와 demo 재실행을 묶어 현재 검증 범위와 한계를 정리한다.
- [_evidence-ledger.md](/Users/woopinbell/work/book-task-3/database-systems/blog/go/database-internals/01-memtable-skiplist/_evidence-ledger.md): 사용한 근거와 재실행 명령, 관찰값을 남긴다.
- [_structure-outline.md](/Users/woopinbell/work/book-task-3/database-systems/blog/go/database-internals/01-memtable-skiplist/_structure-outline.md): 문서 구조 선택 이유와 버린 접근을 적는다.

## 지금 기준의 결론

이 랩은 Go로 옮겨 온 ordered MemTable의 최소 계약을 보여 준다. 동시성이나 benchmark는 없다. 대신 tombstone을 포함한 ordered entries, logical size 유지, flush threshold용 byte estimate라는 실제 저장 엔진 연결 지점이 선명하다.
