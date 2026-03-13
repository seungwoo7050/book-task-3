# 10 08 MVCC의 범위를 다시 잡기

이 글은 프로젝트 전체에서 가장 앞부분에 해당한다. README의 한 줄 설명을 곧바로 믿지 않고, 파일 구조와 테스트 이름만으로 먼저 범위를 다시 세운다.

## Phase 1
### Session 1

- 당시 목표:
  `08 MVCC`가 어떤 invariant를 먼저 고정하는 슬롯인지 파악한다.
- 변경 단위:
  `database-systems/go/database-internals/projects/08-mvcc/README.md`, `database-systems/go/database-internals/projects/08-mvcc/tests/mvcc_test.go`
- 처음 가설:
  구현이 너무 작아서 단순 API 연습에 가까울 거라고 봤다.
- 실제 진행:
  `find internal tests cmd -type f | sort`로 구조를 펼친 뒤 `rg -n "^func Test" tests`로 테스트 이름을 나열했다. `TestAbortAndDelete`까지 테스트 이름을 훑고 나니, 이 프로젝트의 중심이 단순 기능 추가가 아니라 `Begin` 주변의 invariant를 고정하는 일이라는 게 보였다.

CLI:

```bash
$ find internal tests cmd -type f | sort
cmd/mvcc/main.go
internal/mvcc/mvcc.go
tests/mvcc_test.go
```

```bash
$ rg -n "^func Test" tests
tests/mvcc_test.go:9:func TestBasicReadWrite(t *testing.T) {
tests/mvcc_test.go:29:func TestSnapshotIsolation(t *testing.T) {
tests/mvcc_test.go:46:func TestLatestCommittedValue(t *testing.T) {
tests/mvcc_test.go:63:func TestWriteWriteConflict(t *testing.T) {
tests/mvcc_test.go:75:func TestDifferentKeysNoConflict(t *testing.T) {
tests/mvcc_test.go:85:func TestAbortAndDelete(t *testing.T) {
tests/mvcc_test.go:112:func TestGC(t *testing.T) {
```

검증 신호:

- `TestBasicReadWrite`는 가장 기본 표면을 보여 줬고, `TestAbortAndDelete`는 이 프로젝트가 이미 경계 조건까지 포함한다는 신호였다.
- 테스트 이름만으로도 문제의 중심이 `Begin` 주변의 ordering / visibility 규칙이라는 점이 드러났다.

핵심 코드:

```go
func TestAbortAndDelete(t *testing.T) {
	manager := mvcc.NewTransactionManager()
	t1 := manager.Begin()
	manager.Write(t1, "x", "temp")
	manager.Abort(t1)

	t2 := manager.Begin()
	if got := manager.Read(t2, "x"); got != nil {
		t.Fatalf("expected aborted write to disappear, got %v", got)
	}
	mustCommit(t, manager, t2)
```

왜 이 코드가 중요했는가:

`TestAbortAndDelete`는 README의 추상 설명보다 더 직접적으로, 어떤 실패를 막아야 하는지 보여 준다. 나는 여기서 구현 순서를 거꾸로 세우기보다 테스트가 요구하는 경계를 먼저 고정해야 한다고 판단했다.

새로 배운 것:

- `Snapshot Visibility`에서 정리한 요점처럼, transaction은 시작 시점의 committed watermark를 snapshot으로 잡는다.

다음:

- `Begin`와 `Read`를 코드에서 직접 확인해, 테스트 이름이 가리키는 invariant가 실제로 어디에 박혀 있는지 본다.

### Session 2

- 당시 목표:
  소스 파일의 중심 타입/클래스가 어떤 책임을 한곳에 묶고 있는지 확인한다.
- 변경 단위:
  `database-systems/go/database-internals/projects/08-mvcc/internal/mvcc/mvcc.go`
- 처음 가설:
  구현이 작으면 책임도 단순하게 한 줄로 설명될 거라고 생각했다.
- 실제 진행:
  가장 큰 구현 파일인 `database-systems/go/database-internals/projects/08-mvcc/internal/mvcc/mvcc.go`를 먼저 읽고, 테스트가 요구한 상태 전이가 정말 이 파일 안에서 닫히는지 확인했다.

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

- `Begin` 같은 이름이 초기에 바로 보이면 write path의 중심이 선명해진다.
- 반대로 `Read`가 함께 보이면 read path나 visibility 규칙을 따로 떼어 설명할 수 없다는 뜻이다.

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

왜 이 코드가 중요했는가:

`Begin`는 이 프로젝트가 가장 먼저 고정해야 하는 상태 전이를 보여 준다. 이 조각을 읽고 나서야 테스트 이름과 실제 구현 책임이 같은 축에 놓여 있다는 확신이 생겼다.

새로 배운 것:

- `Write Conflict`에서 정리한 요점처럼, 이 프로젝트는 first-committer-wins 규칙을 사용한다.

다음:

- 같은 상태를 반대 방향에서 고정하는 `Read`를 읽어, write/read 혹은 append/replay가 서로 어떻게 잠기는지 확인한다.
