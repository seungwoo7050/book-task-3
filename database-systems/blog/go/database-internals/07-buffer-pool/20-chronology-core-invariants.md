# 20 07 Buffer Pool에서 진짜 중요한 상태 전이만 붙잡기

이 시리즈의 가운데 글이다. 기능 목록을 다시 적기보다, 규칙이 실제 코드에서 언제 강제되는지 보여 주는 데 초점을 둔다.

## Phase 2 — 핵심 상태 전이를 붙잡는 구간

이번 글에서는 핵심 함수 두 곳을 따라가며 같은 invariant가 어디서 고정되고, 다른 각도에서 어떻게 반복되는지 본다.

### Session 1 — FetchPage에서 invariant가 잠기는 지점 보기

이번 세션의 목표는 `FetchPage`가 어떤 입력을 받아 어떤 상태를 고정하는지 분해하는 것이었다. 초기 가설은 `FetchPage` 하나를 이해하면 나머지 흐름도 거의 자동으로 따라올 거라고 생각했다.

막상 다시 펼쳐 보니 `rg -n "FetchPage|UnpinPage" internal cmd`로 핵심 함수 위치를 다시 잡고, `FetchPage`가 문제 정의의 첫 번째 bullet과 정확히 맞물리는지 확인했다. 특히 `FetchPage` 안에서 상태가 한 번에 굳는지, 아니면 보조 구조로 넘겨지는지가 프로젝트의 설명 밀도를 갈랐다.

변경 단위:
- `database-systems/go/database-internals/projects/07-buffer-pool/internal/bufferpool/buffer_pool.go`의 `FetchPage`

CLI:

```bash
$ rg -n "FetchPage|UnpinPage" internal cmd
cmd/buffer-pool/main.go:28:	page, err := pool.FetchPage(dataFile + ":1")
internal/bufferpool/buffer_pool.go:41:func (pool *BufferPool) FetchPage(pageID string) (*Page, error) {
internal/bufferpool/buffer_pool.go:79:func (pool *BufferPool) UnpinPage(pageID string, isDirty bool) {
```

검증 신호:
- `FetchPage` 안에서 상태가 한 번에 굳는지, 아니면 보조 구조로 넘겨지는지가 프로젝트의 설명 밀도를 갈랐다.
- `고정 크기 page를 메모리에 캐시하는 기본 구조를 익힙니다.`

핵심 코드:

```go
func (pool *BufferPool) FetchPage(pageID string) (*Page, error) {
	if cached := pool.cache.Get(pageID); cached != nil {
		page := cached.(*Page)
		page.PinCount++
		return page, nil
	}

	filePath, pageNumber, err := parsePageID(pageID)
	if err != nil {
		return nil, err
	}
	handle, err := pool.getHandle(filePath)
	if err != nil {
		return nil, err
```

왜 여기서 판단이 바뀌었는가:

`FetchPage`는 이 프로젝트에서 규칙이 가장 먼저 굳는 지점을 보여 준다. 테스트가 요구한 첫 번째 조건이 실제 코드 규칙으로 바뀌는 순간을 여기서 확인할 수 있었다.

이번 구간에서 새로 이해한 것:
- `Pin And Dirty`에서 정리한 요점처럼, pin count가 0보다 큰 page는 eviction 대상이 될 수 없다.

다음으로 넘긴 질문:
- `UnpinPage`까지 읽어야 비로소 이 프로젝트가 '쓰는 방법'만이 아니라 '읽고 복원하는 방법'까지 같이 고정하는지 판단할 수 있다.

### Session 2 — UnpinPage로 같은 규칙 다시 확인하기

이 구간에서 먼저 붙잡으려 한 것은 `UnpinPage`가 `FetchPage`와 어떤 짝을 이루는지 확인하는 것이었다. 처음 읽을 때는 `UnpinPage`는 단순 보조 함수일 거라고 생각했다.

그런데 두 번째 앵커를 읽고 나니, 실제로는 `FetchPage`가 만든 상태를 외부에서 관찰 가능하게 만드는 규칙이 여기 있었다. 특히 `UnpinPage`는 테스트의 뒤쪽 시나리오를 설명하는 열쇠였다.

변경 단위:
- `database-systems/go/database-internals/projects/07-buffer-pool/internal/bufferpool/buffer_pool.go`의 `UnpinPage`

CLI:

```bash
$ rg -n "^(type|func) " internal cmd
cmd/buffer-pool/main.go:11:func main() {
cmd/buffer-pool/main.go:33:func must(err error) {
internal/lrucache/lru_cache.go:3:type node struct {
internal/lrucache/lru_cache.go:10:type LRUCache struct {
internal/lrucache/lru_cache.go:18:func New(capacity int) *LRUCache {
internal/lrucache/lru_cache.go:31:func (cache *LRUCache) Get(key string) any {
internal/lrucache/lru_cache.go:40:func (cache *LRUCache) Put(key string, value any) *Entry {
internal/lrucache/lru_cache.go:65:func (cache *LRUCache) Delete(key string) bool {
internal/lrucache/lru_cache.go:76:func (cache *LRUCache) Has(key string) bool {
internal/lrucache/lru_cache.go:81:func (cache *LRUCache) Keys() []string {
internal/lrucache/lru_cache.go:91:func (cache *LRUCache) Size() int {
internal/lrucache/lru_cache.go:95:type Entry struct {
internal/lrucache/lru_cache.go:100:func (cache *LRUCache) remove(item *node) {
internal/lrucache/lru_cache.go:107:func (cache *LRUCache) addToFront(item *node) {
internal/lrucache/lru_cache.go:114:func (cache *LRUCache) moveToFront(item *node) {
internal/bufferpool/buffer_pool.go:15:type Page struct {
internal/bufferpool/buffer_pool.go:22:type BufferPool struct {
internal/bufferpool/buffer_pool.go:29:func New(maxPages, pageSize int) *BufferPool {
internal/bufferpool/buffer_pool.go:41:func (pool *BufferPool) FetchPage(pageID string) (*Page, error) {
internal/bufferpool/buffer_pool.go:79:func (pool *BufferPool) UnpinPage(pageID string, isDirty bool) {
internal/bufferpool/buffer_pool.go:93:func (pool *BufferPool) FlushPage(pageID string) error {
internal/bufferpool/buffer_pool.go:109:func (pool *BufferPool) FlushAll() error {
internal/bufferpool/buffer_pool.go:118:func (pool *BufferPool) Close() error {
internal/bufferpool/buffer_pool.go:131:func (pool *BufferPool) getHandle(filePath string) (*fileio.FileHandle, error) {
internal/bufferpool/buffer_pool.go:144:func (pool *BufferPool) writePage(page *Page) error {
internal/bufferpool/buffer_pool.go:159:func parsePageID(pageID string) (string, int, error) {
```

검증 신호:
- `UnpinPage`는 테스트의 뒤쪽 시나리오를 설명하는 열쇠였다.
- 특히 `TestLRUOrderingAndDelete` 같은 이름이 왜 필요한지, 이 함수에서야 연결이 됐다.

핵심 코드:

```go
func (pool *BufferPool) UnpinPage(pageID string, isDirty bool) {
	cached := pool.cache.Get(pageID)
	if cached == nil {
		return
	}
	page := cached.(*Page)
	if page.PinCount > 0 {
		page.PinCount--
	}
	if isDirty {
		page.Dirty = true
	}
}
```

왜 여기서 판단이 바뀌었는가:

`UnpinPage`가 없으면 `FetchPage`의 의미도 끝까지 설명되지 않는다. 이 코드를 보고 나서야, 이 프로젝트가 단일 API 구현이 아니라 ordering / visibility / recovery 규칙을 통째로 묶는 이유를 납득할 수 있었다.

이번 구간에서 새로 이해한 것:
- `Pin And Dirty`에서 정리한 요점처럼, pin count가 0보다 큰 page는 eviction 대상이 될 수 없다.

다음으로 넘긴 질문:
- 실제 재검증 명령을 다시 돌려, 지금까지 읽은 invariant가 테스트와 demo 출력에서 같은 모양으로 보이는지 확인한다.
