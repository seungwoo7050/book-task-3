# 03 Mini LSM Store

## 이 랩의 실제 무게중심

앞선 Go 트랙에서 MemTable과 SSTable을 따로 봤다면, 이 프로젝트는 그 둘을 다시 한 write/read lifecycle 안으로 묶는 단계다. active memtable이 threshold를 넘으면 immutable snapshot으로 바뀌고, 그 snapshot이 SSTable로 flush되며, read path는 active memtable, immutable memtable, newest SSTable 순으로 내려간다. 그리고 close/reopen 뒤에도 기존 SSTable index를 다시 적재해 lookup이 이어져야 한다.

즉 이 랩의 핵심은 "작은 LSM store를 완성했다"는 선언보다, 메모리 단계와 디스크 단계가 어떤 순서와 우선순위로 연결되는지를 source-first로 설명하는 데 있다.

이번 시리즈는 기존 blog를 입력 근거로 쓰지 않고 [`problem/README.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/03-mini-lsm-store/problem/README.md), [`store.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/03-mini-lsm-store/internal/lsmstore/store.go), [`lsm_store_test.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/03-mini-lsm-store/tests/lsm_store_test.go), [`main.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/03-mini-lsm-store/cmd/mini-lsm-store/main.go), 그리고 2026-03-14 재실행 결과만으로 다시 썼다.

## 이번에 붙드는 질문

- flush 직전과 flush 직후에 어떤 구조가 active인지
- read path가 왜 newest-first여야 하는지
- tombstone이 cross-level lookup에서도 어떻게 삭제 의미를 유지하는지
- reopen 이후 persisted SSTable registry가 어떤 순서로 다시 살아나는지

## 문서 지도

- [10-chronology-scope-and-surface.md](/Users/woopinbell/work/book-task-3/database-systems/blog/go/database-internals/03-mini-lsm-store/10-chronology-scope-and-surface.md): 문제 범위, write/flush/read 표면, demo 결과를 시간순으로 정리한다.
- [20-chronology-core-invariants.md](/Users/woopinbell/work/book-task-3/database-systems/blog/go/database-internals/03-mini-lsm-store/20-chronology-core-invariants.md): immutable swap, newest-first lookup, tombstone across levels, reopen ordering을 소스 기준으로 해부한다.
- [30-chronology-verification-and-boundaries.md](/Users/woopinbell/work/book-task-3/database-systems/blog/go/database-internals/03-mini-lsm-store/30-chronology-verification-and-boundaries.md): go test와 demo, 추가 재실행을 묶어 현재 검증 범위와 한계를 정리한다.
- [_evidence-ledger.md](/Users/woopinbell/work/book-task-3/database-systems/blog/go/database-internals/03-mini-lsm-store/_evidence-ledger.md): 근거 파일과 재실행 명령, 관찰값을 남긴다.
- [_structure-outline.md](/Users/woopinbell/work/book-task-3/database-systems/blog/go/database-internals/03-mini-lsm-store/_structure-outline.md): 문서 구조 선택 이유와 버린 접근을 적는다.

## 지금 기준의 결론

이 랩은 Go 저장 엔진 트랙에서 첫 orchestration 단계다. background compaction이나 concurrent flush는 없다. 대신 immutable memtable swap, SSTable registry prepend, newest-first read precedence, reopen-safe index load는 명확하게 드러난다.
