# 10 07 Buffer Pool의 범위를 다시 잡기

이 글은 프로젝트 전체에서 가장 앞부분에 해당한다. README의 한 줄 설명을 곧바로 믿지 않고, 파일 구조와 테스트 이름만으로 먼저 범위를 다시 세운다.

## Phase 1
### Session 1

- 당시 목표:
  `07 Buffer Pool`가 어떤 invariant를 먼저 고정하는 슬롯인지 파악한다.
- 변경 단위:
  `database-systems/go/database-internals/projects/07-buffer-pool/README.md`, `database-systems/go/database-internals/projects/07-buffer-pool/tests/buffer_pool_test.go`
- 처음 가설:
  구현이 너무 작아서 단순 API 연습에 가까울 거라고 봤다.
- 실제 진행:
  `find internal tests cmd -type f | sort`로 구조를 펼친 뒤 `rg -n "^func Test" tests`로 테스트 이름을 나열했다. `TestLRUOrderingAndDelete`까지 테스트 이름을 훑고 나니, 이 프로젝트의 중심이 단순 기능 추가가 아니라 `FetchPage` 주변의 invariant를 고정하는 일이라는 게 보였다.

CLI:

```bash
$ find internal tests cmd -type f | sort
cmd/buffer-pool/main.go
internal/bufferpool/buffer_pool.go
internal/lrucache/lru_cache.go
tests/buffer_pool_test.go
tests/lru_cache_test.go
```

```bash
$ rg -n "^func Test" tests
tests/lru_cache_test.go:10:func TestLRUBasicOperations(t *testing.T) {
tests/lru_cache_test.go:29:func TestLRUEvictionAndPromotion(t *testing.T) {
tests/lru_cache_test.go:47:func TestLRUOrderingAndDelete(t *testing.T) {
tests/buffer_pool_test.go:11:func TestFetchPageFromDisk(t *testing.T) {
tests/buffer_pool_test.go:24:func TestReturnCachedPage(t *testing.T) {
tests/buffer_pool_test.go:42:func TestTrackDirtyPages(t *testing.T) {
tests/buffer_pool_test.go:57:func TestEvictionAfterUnpin(t *testing.T) {
```

검증 신호:

- `TestFetchPageFromDisk`는 가장 기본 표면을 보여 줬고, `TestLRUOrderingAndDelete`는 이 프로젝트가 이미 경계 조건까지 포함한다는 신호였다.
- 테스트 이름만으로도 문제의 중심이 `FetchPage` 주변의 ordering / visibility 규칙이라는 점이 드러났다.

핵심 코드:

```go
func TestLRUOrderingAndDelete(t *testing.T) {
	cache := lrucache.New(3)
	cache.Put("a", 1)
	cache.Put("b", 2)
	cache.Put("c", 3)

	if !reflect.DeepEqual(cache.Keys(), []string{"c", "b", "a"}) {
		t.Fatalf("unexpected order: %+v", cache.Keys())
	}
	cache.Get("a")
	if !reflect.DeepEqual(cache.Keys(), []string{"a", "c", "b"}) {
		t.Fatalf("unexpected order after promotion: %+v", cache.Keys())
	}
	if !cache.Delete("a") {
```

왜 이 코드가 중요했는가:

`TestLRUOrderingAndDelete`는 README의 추상 설명보다 더 직접적으로, 어떤 실패를 막아야 하는지 보여 준다. 나는 여기서 구현 순서를 거꾸로 세우기보다 테스트가 요구하는 경계를 먼저 고정해야 한다고 판단했다.

새로 배운 것:

- `LRU Eviction`에서 정리한 요점처럼, doubly-linked list와 hash map을 조합하면 O(1) get/put/evict가 가능하다.

다음:

- `FetchPage`와 `UnpinPage`를 코드에서 직접 확인해, 테스트 이름이 가리키는 invariant가 실제로 어디에 박혀 있는지 본다.

### Session 2

- 당시 목표:
  소스 파일의 중심 타입/클래스가 어떤 책임을 한곳에 묶고 있는지 확인한다.
- 변경 단위:
  `database-systems/go/database-internals/projects/07-buffer-pool/internal/bufferpool/buffer_pool.go`
- 처음 가설:
  구현이 작으면 책임도 단순하게 한 줄로 설명될 거라고 생각했다.
- 실제 진행:
  가장 큰 구현 파일인 `database-systems/go/database-internals/projects/07-buffer-pool/internal/bufferpool/buffer_pool.go`를 먼저 읽고, 테스트가 요구한 상태 전이가 정말 이 파일 안에서 닫히는지 확인했다.

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

- `FetchPage` 같은 이름이 초기에 바로 보이면 write path의 중심이 선명해진다.
- 반대로 `UnpinPage`가 함께 보이면 read path나 visibility 규칙을 따로 떼어 설명할 수 없다는 뜻이다.

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

왜 이 코드가 중요했는가:

`FetchPage`는 이 프로젝트가 가장 먼저 고정해야 하는 상태 전이를 보여 준다. 이 조각을 읽고 나서야 테스트 이름과 실제 구현 책임이 같은 축에 놓여 있다는 확신이 생겼다.

새로 배운 것:

- `Pin And Dirty`에서 정리한 요점처럼, pin count가 0보다 큰 page는 eviction 대상이 될 수 없다.

다음:

- 같은 상태를 반대 방향에서 고정하는 `UnpinPage`를 읽어, write/read 혹은 append/replay가 서로 어떻게 잠기는지 확인한다.
