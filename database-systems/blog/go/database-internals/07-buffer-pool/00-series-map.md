# 07 Buffer Pool

## 이 랩의 실제 초점

이 프로젝트는 page cache를 만든다는 말보다 더 정확하게, "disk page를 메모리에 올려 둔 뒤 언제 내보낼 수 있고 언제 내보내면 안 되는가"를 다룬다. page는 `pageID = filePath:pageNumber`로 식별되고, fetch hit는 pin count를 올리며, dirty page는 flush 또는 eviction 전에 write-back 돼야 하고, pin count가 남아 있으면 eviction하면 안 된다. LRU는 후보를 고르는 기본 정책이지만, page metadata가 그 위에 덧씌워진다.

즉 이 랩의 핵심은 LRU 자체보다 pin/dirty와 eviction의 충돌을 어떻게 다루는가에 있다.

이번 시리즈는 기존 blog를 입력 근거로 쓰지 않고 [`problem/README.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/07-buffer-pool/problem/README.md), [`buffer_pool.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/07-buffer-pool/internal/bufferpool/buffer_pool.go), [`buffer_pool_test.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/07-buffer-pool/tests/buffer_pool_test.go), [`lru_cache_test.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/07-buffer-pool/tests/lru_cache_test.go), [`main.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/07-buffer-pool/cmd/buffer-pool/main.go), 그리고 2026-03-14 재실행 결과만으로 다시 썼다.

## 이번에 붙드는 질문

- cache hit/miss는 pin count를 어떻게 바꾸는가
- LRU eviction은 page metadata와 어디서 충돌하는가
- dirty page는 언제 disk에 다시 써지는가
- pinned page eviction 실패는 현재 구현에서 어떤 형태로 드러나는가

## 문서 지도

- [10-chronology-scope-and-surface.md](/Users/woopinbell/work/book-task-3/database-systems/blog/go/database-internals/07-buffer-pool/10-chronology-scope-and-surface.md): 문제 범위, fetch/unpin/flush 표면, demo 결과를 시간순으로 정리한다.
- [20-chronology-core-invariants.md](/Users/woopinbell/work/book-task-3/database-systems/blog/go/database-internals/07-buffer-pool/20-chronology-core-invariants.md): page identity, hit pinning, dirty write-back, pinned eviction failure를 소스 기준으로 해부한다.
- [30-chronology-verification-and-boundaries.md](/Users/woopinbell/work/book-task-3/database-systems/blog/go/database-internals/07-buffer-pool/30-chronology-verification-and-boundaries.md): go test와 demo, 추가 재실행을 묶어 현재 검증 범위와 한계를 정리한다.
- [_evidence-ledger.md](/Users/woopinbell/work/book-task-3/database-systems/blog/go/database-internals/07-buffer-pool/_evidence-ledger.md): 근거 파일과 재실행 명령, 관찰값을 남긴다.
- [_structure-outline.md](/Users/woopinbell/work/book-task-3/database-systems/blog/go/database-internals/07-buffer-pool/_structure-outline.md): 문서 구조 선택 이유와 버린 접근을 적는다.

## 지금 기준의 결론

이 랩은 Go 저장 엔진 트랙에서 "buffer pool이 단순 캐시가 아니라 page lifecycle manager"라는 사실을 가장 직접적으로 보여 준다. concurrent latch, lock manager, async IO는 없다. 대신 pin count, dirty flag, LRU ordering, write-back 경계는 명확히 드러난다.
