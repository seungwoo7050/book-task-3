# Scope, Fetch Surface, And First Page

## 1. 문제는 cache hit ratio보다 page lifecycle을 먼저 고정하는 데 있다

[`problem/README.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/07-buffer-pool/problem/README.md)는 page identity parsing, hit/miss fetch, dirty write-back, pinned page eviction 금지를 요구한다. concurrent latch, lock manager, async IO는 뺀다.

즉 이 랩의 목적은 DBMS buffer manager의 최소 lifecycle을 설명하는 것이지, 동시성까지 포함한 완성형 cache subsystem을 만드는 것이 아니다.

## 2. 코드 표면은 생각보다 작다

핵심 구현은 [`buffer_pool.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/07-buffer-pool/internal/bufferpool/buffer_pool.go)에 있다.

- `FetchPage(pageID)`
- `UnpinPage(pageID, isDirty)`
- `FlushPage(pageID)`
- `FlushAll()`
- `Close()`

구조체 필드도 의도를 드러낸다.

- `cache *lrucache.LRUCache`
- `fileHandles map[string]*fileio.FileHandle`
- `pageSize`

즉 replacement는 LRU cache가 맡고, buffer pool은 page metadata와 disk IO를 책임진다.

## 3. demo는 fetch hit 이전의 가장 기본 관찰을 보여 준다

2026-03-14에 아래 명령을 다시 실행했다.

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/07-buffer-pool
GOWORK=off go run ./cmd/buffer-pool
```

출력은 아래였다.

```text
page-1
```

짧은 출력이지만 의미는 분명하다. page id `data.db:1`이 실제로 파일 path와 page number로 분리돼 해당 offset의 bytes를 읽어 왔다는 뜻이다. buffer pool의 첫 번째 책임은 이 mapping을 안정적으로 수행하는 것이다.

## 4. 추가 재실행으로 dirty flush와 pinned eviction failure를 고정했다

이번에 project root 내부 임시 Go 파일로 아래 결과를 추가로 확인했다.

```text
disk_after_flush modified
pinned_evict_error true
```

이 결과는 두 가지를 보여 준다.

- dirty page를 수정한 뒤 `FlushPage()`를 호출하면 실제 disk bytes가 바뀐다
- capacity보다 많은 page를 fetch하려 할 때, eviction 대상이 pinned면 현재 구현은 에러를 돌려준다

즉 buffer pool은 read cache에 그치지 않고 write-back 경계와 eviction 금지 조건을 함께 가진다.
