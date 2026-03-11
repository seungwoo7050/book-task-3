# 개발 타임라인 — 07 Buffer Pool

이 문서는 프로젝트를 처음부터 재현할 수 있도록, 개발 과정을 시간순으로 기록한다.

---

## Phase 0: 프로젝트 초기화

```bash
mkdir -p go/database-internals/projects/07-buffer-pool/{cmd/buffer-pool,internal/{lrucache,bufferpool},tests,problem/{code,data,script},docs/{concepts,references}}
cd go/database-internals/projects/07-buffer-pool
go mod init study.local/go/database-internals/projects/07-buffer-pool
```

의존성: `shared` 패키지 (`fileio`만 사용)

```
require study.local/go/shared v0.0.0
replace study.local/go/shared => ../../../shared
```

```bash
go work use go/database-internals/projects/07-buffer-pool
```

---

## Phase 1: LRU Cache 구현

### 파일: `internal/lrucache/lru_cache.go`

1. **`node` 구조체**: key, value(any), prev/next 포인터
2. **`LRUCache` 구조체**: capacity, size, items map, head/tail sentinel 노드
3. **`New(capacity)`**: sentinel head↔tail 연결
4. **`Get(key)`**: map 조회 → moveToFront → value 반환
5. **`Put(key, value)`**: 
   - 기존 키면 → 값 갱신 + moveToFront
   - 새 키면 → 용량 초과 시 tail 직전 노드 evict → evicted Entry 반환
6. **`Delete(key)`**: map에서 삭제, 리스트에서 제거
7. **내부 함수**: `remove`, `addToFront`, `moveToFront`

---

## Phase 2: Buffer Pool Manager 구현

### 파일: `internal/bufferpool/buffer_pool.go`

1. **`Page` 구조체**: PageID, Data []byte, Dirty bool, PinCount int
2. **`BufferPool` 구조체**: maxPages, pageSize, LRUCache, fileHandles map
3. **`New(maxPages, pageSize)`**: pageSize 기본값 4096
4. **`FetchPage(pageID)`**: 
   - 캐시 히트 → PinCount++ → 반환
   - 캐시 미스 → parsePageID → getHandle → ReadAt → Page 생성 → cache.Put
   - eviction 시: pinned면 에러, dirty면 writePage
5. **`UnpinPage(pageID, isDirty)`**: PinCount--, dirty 마킹
6. **`FlushPage(pageID)`**: dirty면 writePage → dirty=false
7. **`FlushAll()`**: 모든 캐시 키 순회하며 FlushPage
8. **`Close()`**: FlushAll → 모든 핸들 Close
9. **`writePage(page)`**: parsePageID → WriteAt → Sync
10. **`parsePageID(pageID)`**: "path:number" → (path, number) 파싱

---

## Phase 3: 테스트 데이터 준비 함수

### `seedPages(t)` 헬퍼

테스트 전에 64바이트 페이지 10개를 가진 파일을 임시 디렉터리에 생성한다.
각 페이지 앞 6바이트에 "page-0", "page-1", ... 기입.

```bash
cd go/database-internals/projects/07-buffer-pool
GOWORK=off go test ./...
```

### 테스트 케이스

| 테스트명 | 검증 대상 |
|----------|----------|
| `TestFetchPageFromDisk` | 디스크 읽기 → 올바른 데이터, PinCount=1 |
| `TestReturnCachedPage` | 같은 PageID → 같은 포인터 |
| `TestTrackDirtyPages` | 수정 후 UnpinPage(dirty=true) → Dirty=true |
| `TestEvictionAfterUnpin` | 용량 초과 시 LRU 교체 |

---

## 사용한 도구 요약

| 도구 | 용도 |
|------|------|
| Go 1.26.0 | 언어 런타임 |
| `go test ./...` | 테스트 실행 |
| `shared/fileio` | ReadAt, WriteAt, Sync |
| `os.WriteFile` | 테스트 데이터 파일 생성 |

외부 패키지 의존성: **없음**
