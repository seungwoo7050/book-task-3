# 05 Leveled Compaction

## 이 랩의 실제 질문

이 프로젝트는 compaction을 "파일 몇 개를 합친다" 수준이 아니라, overwrite와 tombstone의 우선순위를 어떻게 보존하면서 level state를 원자적으로 바꾸는가라는 질문으로 다룬다. L0의 겹치는 SSTable들을 newest-first source 배열로 뒤집어 merge하고, deepest level일 때만 tombstone을 제거하며, 새 결과 파일이 생긴 뒤에야 manifest를 atomic write로 갱신하고, 마지막에 입력 파일을 지운다.

즉 이 랩의 핵심은 compaction scheduling이 아니라 merge ordering과 metadata atomicity다.

이번 시리즈는 기존 blog를 입력 근거로 쓰지 않고 [`problem/README.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/05-leveled-compaction/problem/README.md), [`compaction.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/05-leveled-compaction/internal/compaction/compaction.go), [`compaction_test.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/05-leveled-compaction/tests/compaction_test.go), [`main.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/05-leveled-compaction/cmd/leveled-compaction/main.go), 그리고 2026-03-14 재실행 결과만으로 다시 썼다.

## 이번에 붙드는 질문

- k-way merge에서 같은 key의 최신 값은 어떻게 살아남는가
- tombstone은 언제 유지되고 언제 버려지는가
- manifest와 data file은 어떤 순서로 바뀌어야 하는가
- compaction 뒤 old input file 정리는 언제 일어나는가

## 문서 지도

- [10-chronology-scope-and-surface.md](/Users/woopinbell/work/book-task-3/database-systems/blog/go/database-internals/05-leveled-compaction/10-chronology-scope-and-surface.md): 문제 범위, compaction surface, demo 결과를 시간순으로 정리한다.
- [20-chronology-core-invariants.md](/Users/woopinbell/work/book-task-3/database-systems/blog/go/database-internals/05-leveled-compaction/20-chronology-core-invariants.md): newest-first merge, tombstone drop 조건, manifest atomicity, input file cleanup를 소스 기준으로 설명한다.
- [30-chronology-verification-and-boundaries.md](/Users/woopinbell/work/book-task-3/database-systems/blog/go/database-internals/05-leveled-compaction/30-chronology-verification-and-boundaries.md): go test와 demo, 추가 재실행을 묶어 현재 검증 범위와 한계를 정리한다.
- [_evidence-ledger.md](/Users/woopinbell/work/book-task-3/database-systems/blog/go/database-internals/05-leveled-compaction/_evidence-ledger.md): 근거 파일과 재실행 명령, 관찰값을 남긴다.
- [_structure-outline.md](/Users/woopinbell/work/book-task-3/database-systems/blog/go/database-internals/05-leveled-compaction/_structure-outline.md): 문서 구조 선택 이유와 버린 접근을 적는다.

## 지금 기준의 결론

이 랩은 Go 저장 엔진 트랙에서 "compaction이 단순 merge가 아니라 overwrite/tombstone semantics와 metadata atomicity를 동시에 다루는 작업"이라는 사실을 가장 선명하게 보여 준다. background scheduler나 multi-level balancing은 아직 의도적으로 비워 둔다.
