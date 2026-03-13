# 20 09 MVCC에서 진짜 중요한 상태 전이만 붙잡기

이 시리즈의 가운데 글이다. 여기서는 추상 설명을 줄이고, 실제 구현에서 invariant가 어디서 잠기는지 핵심 코드만 붙잡아 따라간다.

## Phase 2 — 핵심 상태 전이를 붙잡는 구간

이번 글에서는 핵심 함수 두 곳을 따라가며 같은 invariant가 어디서 고정되고, 다른 각도에서 어떻게 반복되는지 본다.

### Session 1 — Begin에서 invariant가 잠기는 지점 보기

이 구간에서 먼저 붙잡으려 한 것은 `Begin`가 어떤 입력을 받아 어떤 상태를 고정하는지 분해하는 것이었다. 처음 읽을 때는 `Begin` 하나를 이해하면 나머지 흐름도 거의 자동으로 따라올 거라고 생각했다.

그런데 `rg -n "Begin|Read" internal cmd`로 핵심 함수 위치를 다시 잡고, `Begin`가 문제 정의의 첫 번째 bullet과 정확히 맞물리는지 확인했다. 특히 `Begin` 안에서 상태가 한 번에 굳는지, 아니면 보조 구조로 넘겨지는지가 프로젝트의 설명 밀도를 갈랐다.

변경 단위:
- `database-systems/go/database-internals/projects/09-mvcc/internal/mvcc/mvcc.go`의 `Begin`

CLI:

```bash
$ rg -n "Begin|Read" internal cmd
cmd/mvcc/main.go:12:	t1 := manager.Begin()
cmd/mvcc/main.go:16:	t2 := manager.Begin()
cmd/mvcc/main.go:17:	t3 := manager.Begin()
cmd/mvcc/main.go:21:	fmt.Printf("t2 sees x=%v\n", manager.Read(t2, "x"))
internal/mvcc/mvcc.go:107:func (manager *TransactionManager) Begin() int {
internal/mvcc/mvcc.go:125:func (manager *TransactionManager) Read(txID int, key string) any {
```

검증 신호:
- `Begin` 안에서 상태가 한 번에 굳는지, 아니면 보조 구조로 넘겨지는지가 프로젝트의 설명 밀도를 갈랐다.
- `snapshot timestamp가 어떤 version을 볼 수 있는지 판단하는 규칙을 익힙니다.`

핵심 코드:

```go
func (manager *TransactionManager) Begin() int {
	txID := manager.NextTxID
	manager.NextTxID++

	maxCommitted := 0
	for id := range manager.Committed {
		if id > maxCommitted {
			maxCommitted = id
		}
	}
	manager.Transactions[txID] = &Transaction{
		Snapshot: maxCommitted,
		Status:   txActive,
		WriteSet: map[string]bool{},
```

왜 여기서 판단이 바뀌었는가:

`Begin`는 이 프로젝트에서 규칙이 가장 먼저 굳는 지점을 보여 준다. 테스트가 요구한 첫 번째 조건이 실제 코드 규칙으로 바뀌는 순간을 여기서 확인할 수 있었다.

이번 구간에서 새로 이해한 것:
- `Write Conflict`에서 정리한 요점처럼, 이 프로젝트는 first-committer-wins 규칙을 사용한다.

다음으로 넘긴 질문:
- `Read`까지 읽어야 비로소 이 프로젝트가 '쓰는 방법'만이 아니라 '읽고 복원하는 방법'까지 같이 고정하는지 판단할 수 있다.

### Session 2 — Read로 같은 규칙 다시 확인하기

여기서 가장 먼저 확인한 것은 `Read`가 `Begin`와 어떤 짝을 이루는지 확인한다. 처음에는 `Read`는 단순 보조 함수일 거라고 생각했다.

하지만 실제로는 두 번째 앵커를 읽고 나니, 실제로는 `Begin`가 만든 상태를 외부에서 관찰 가능하게 만드는 규칙이 여기 있었다. 결정적으로 방향을 잡아 준 신호는 `Read`는 테스트의 뒤쪽 시나리오를 설명하는 열쇠였다.

변경 단위:
- `database-systems/go/database-internals/projects/09-mvcc/internal/mvcc/mvcc.go`의 `Read`

CLI:

```bash
$ rg -n "^(type|func) " internal cmd
internal/mvcc/mvcc.go:5:type Version struct {
internal/mvcc/mvcc.go:11:type VersionStore struct {
internal/mvcc/mvcc.go:15:func NewVersionStore() *VersionStore {
internal/mvcc/mvcc.go:19:func (store *VersionStore) Append(key string, value any, txID int, deleted bool) {
internal/mvcc/mvcc.go:31:func (store *VersionStore) GetVisible(key string, snapshot int, committed map[int]bool) *Version {
internal/mvcc/mvcc.go:42:func (store *VersionStore) RemoveByTxID(key string, txID int) {
internal/mvcc/mvcc.go:57:func (store *VersionStore) GC(minSnapshot int) {
internal/mvcc/mvcc.go:85:type Transaction struct {
internal/mvcc/mvcc.go:91:type TransactionManager struct {
internal/mvcc/mvcc.go:98:func NewTransactionManager() *TransactionManager {
internal/mvcc/mvcc.go:107:func (manager *TransactionManager) Begin() int {
internal/mvcc/mvcc.go:125:func (manager *TransactionManager) Read(txID int, key string) any {
internal/mvcc/mvcc.go:146:func (manager *TransactionManager) Write(txID int, key string, value any) {
internal/mvcc/mvcc.go:152:func (manager *TransactionManager) Delete(txID int, key string) {
internal/mvcc/mvcc.go:158:func (manager *TransactionManager) Commit(txID int) error {
internal/mvcc/mvcc.go:174:func (manager *TransactionManager) Abort(txID int) {
internal/mvcc/mvcc.go:178:func (manager *TransactionManager) GC() {
internal/mvcc/mvcc.go:188:func (manager *TransactionManager) activeTx(txID int) *Transaction {
internal/mvcc/mvcc.go:199:func (manager *TransactionManager) abortInternal(txID int, tx *Transaction) {
cmd/mvcc/main.go:9:func main() {
cmd/mvcc/main.go:25:func must(err error) {
```

검증 신호:
- `Read`는 테스트의 뒤쪽 시나리오를 설명하는 열쇠였다.
- 특히 `TestAbortAndDelete` 같은 이름이 왜 필요한지, 이 함수에서야 연결이 됐다.

핵심 코드:

```go
func (manager *TransactionManager) Read(txID int, key string) any {
	tx := manager.activeTx(txID)

	if tx.WriteSet[key] {
		for _, version := range manager.VersionStore.Store[key] {
			if version.TxID == txID {
				if version.Deleted {
					return nil
				}
				return version.Value
			}
		}
	}
```

왜 여기서 판단이 바뀌었는가:

`Read`가 없으면 `Begin`의 의미도 끝까지 설명되지 않는다. 이 코드를 보고 나서야, 이 프로젝트가 단일 API 구현이 아니라 ordering / visibility / recovery 규칙을 통째로 묶는 이유를 납득할 수 있었다.

이번 구간에서 새로 이해한 것:
- `Write Conflict`에서 정리한 요점처럼, 이 프로젝트는 first-committer-wins 규칙을 사용한다.

다음으로 넘긴 질문:
- 실제 재검증 명령을 다시 돌려, 지금까지 읽은 invariant가 테스트와 demo 출력에서 같은 모양으로 보이는지 확인한다.
