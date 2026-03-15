# 09 MVCC

## 이 랩의 실제 초점

이 프로젝트는 MVCC를 거대한 transaction manager로 다루지 않는다. 대신 snapshot isolation에서 꼭 필요한 최소 규칙만 남긴다. transaction은 시작 시 committed watermark를 snapshot으로 잡고, read는 그 snapshot 이하의 committed version만 볼 수 있으며, 자기 자신이 쓴 uncommitted version은 예외적으로 read-your-own-write로 본다. commit 시에는 first-committer-wins 충돌 검사를 하고, abort는 자기 tx가 쓴 version만 지운다. GC는 더 이상 어떤 active snapshot도 보지 못하는 오래된 version을 줄인다.

즉 이 랩의 핵심은 SQL 격리 수준 전체를 설명하는 것이 아니라, version chain과 transaction metadata만으로 snapshot visibility와 write-write conflict를 어떻게 만드는가를 source-first로 드러내는 데 있다.

이번 시리즈는 기존 blog를 입력 근거로 쓰지 않고 [`problem/README.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/09-mvcc/problem/README.md), [`mvcc.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/09-mvcc/internal/mvcc/mvcc.go), [`mvcc_test.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/09-mvcc/tests/mvcc_test.go), [`main.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/09-mvcc/cmd/mvcc/main.go), 그리고 2026-03-14 재실행 결과만으로 다시 썼다.

## 이번에 붙드는 질문

- snapshot timestamp는 어떤 version을 visible로 만드는가
- read-your-own-write는 일반 visibility 규칙과 어디서 갈라지는가
- first-committer-wins 충돌은 commit 시점에 어떻게 판정되는가
- abort cleanup과 stale version GC는 언제 어떤 version을 지우는가

## 문서 지도

- [10-chronology-scope-and-surface.md](/Users/woopinbell/work/book-task-3/database-systems/blog/go/database-internals/09-mvcc/10-chronology-scope-and-surface.md): 문제 범위, transaction/version store 표면, demo 결과를 시간순으로 정리한다.
- [20-chronology-core-invariants.md](/Users/woopinbell/work/book-task-3/database-systems/blog/go/database-internals/09-mvcc/20-chronology-core-invariants.md): snapshot visibility, read-your-own-write, conflict detection, GC trimming을 소스 기준으로 해부한다.
- [30-chronology-verification-and-boundaries.md](/Users/woopinbell/work/book-task-3/database-systems/blog/go/database-internals/09-mvcc/30-chronology-verification-and-boundaries.md): go test와 demo, 추가 재실행을 묶어 현재 검증 범위와 한계를 정리한다.
- [_evidence-ledger.md](/Users/woopinbell/work/book-task-3/database-systems/blog/go/database-internals/09-mvcc/_evidence-ledger.md): 근거 파일과 재실행 명령, 관찰값을 남긴다.
- [_structure-outline.md](/Users/woopinbell/work/book-task-3/database-systems/blog/go/database-internals/09-mvcc/_structure-outline.md): 문서 구조 선택 이유와 버린 접근을 적는다.

## 지금 기준의 결론

이 랩은 Go 저장 엔진 트랙의 마지막 단계에서 "같은 key의 여러 version 중 지금 어떤 것을 볼 수 있는가"를 가장 작게 구현한다. predicate locking, phantom control, distributed transaction은 없다. 대신 snapshot watermark, write-write conflict, abort cleanup, GC 조건은 선명하게 드러난다.
