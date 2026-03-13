# 13 Distributed Log Core — Store Index And Segment Core

`02-distributed-systems/13-distributed-log-core`는 append-only store, mmap index, segment rotation, log abstraction을 직접 구현해 commit log 핵심을 익히는 대표 과제다. 이 글에서는 1단계: 프로젝트 초기화 -> 2단계: Store 구현 (append-only 파일) -> 3단계: Index 구현 (mmap 기반) -> 4단계: Segment 구현 (Store + Index 조합) 구간을 따라가면서, 어떤 파일과 어떤 명령이 실제 구현 전환점이었는지 복원한다.

## 구현 순서 요약

- 1단계: 프로젝트 초기화
- 2단계: Store 구현 (append-only 파일)
- 3단계: Index 구현 (mmap 기반)
- 4단계: Segment 구현 (Store + Index 조합)

## Day 1
### Session 1

- 당시 목표: length-prefixed store와 fixed-width index를 직접 구현해야 한다.
- 변경 단위: `log/store.go`, `log/index.go`, `log/segment.go`
- 처음 가설: Kafka형 시스템을 한 번에 복제하지 않고 append-only log 핵심 구조만 분리했다.
- 실제 진행: Go 1.22 사용, 외부 의존성 없이 표준 라이브러리만으로 구현. `log/store.go` 작성. 주요 결정: `bufio.NewWriter`로 쓰기 버퍼링 (시스템 콜 최소화) 길이 접두사: `binary.BigEndian.PutUint64` (8바이트 고정) `sync.Mutex`로 동시 접근 보호 `Read`에서 항상 `buf.Flush()` 먼저 `log/index.go` 작성.

CLI:

```bash
mkdir -p 13-distributed-log-core/solution/go/log
cd 13-distributed-log-core/go
go mod init distributed-log-core

# 파일 생성 후 첫 컴파일 확인
go build ./...
```

검증 신호:

- 이 구간에서 실행 진입점과 검증 명령이 처음 함께 닫혔다.

핵심 코드: `solution/go/log/store.go`

```go
var enc = binary.BigEndian

// lenWidth는 레코드 길이를 저장하는 바이트 수다.
const lenWidth = 8

// store는 길이 접두사가 붙은 레코드를 순차적으로 저장하는 파일 래퍼다.
// 각 레코드는 `[8바이트 길이][데이터 바이트]` 형식으로 기록된다.
type store struct {
	mu   sync.Mutex
	file *os.File
	buf  *bufio.Writer
	size uint64
}

// newStore는 기존 파일 크기를 기준으로 이어 쓰기 가능한 store를 만든다.
func newStore(f *os.File) (*store, error) {
	fi, err := os.Stat(f.Name())
	if err != nil {
```

왜 이 코드가 중요했는가:

이 코드는 상태를 저장하고 읽는 계약을 고정한 부분이다. 이후의 handler, service, runtime 설명은 이 저장 규칙이 닫혀 있어야만 설득력을 갖는다.

새로 배운 것:

- store는 레코드 바이트를 순차 append하는 역할이다.

보조 코드: `solution/go/log/segment.go`

```go
type Config struct {
	MaxStoreBytes uint64
	MaxIndexBytes uint64
}

// segment는 하나의 store 파일과 index 파일을 묶어 관리한다.
// baseOffset부터 시작하는 연속된 레코드를 저장하며, 최대 크기에 도달하면 새 세그먼트로 넘긴다.
type segment struct {
	store      *store
	index      *index
	baseOffset uint64
	nextOffset uint64
	config     Config
}

// newSegment는 baseOffset 기준의 store/index 파일을 열고 세그먼트를 복구한다.
func newSegment(dir string, baseOffset uint64, c Config) (*segment, error) {
	storePath := filepath.Join(dir, fmt.Sprintf("%d.store", baseOffset))
```

왜 이 코드도 같이 봐야 하는가:

이 조각은 프로젝트의 핵심 판단이 실제 어느 함수와 자료구조에 걸려 있는지 보여 준다. 추상 요약보다 먼저 이 코드를 봐야 구현 순서가 살아난다.

CLI:

```bash
cd 02-distributed-systems/13-distributed-log-core
make -C problem test
make -C problem bench
```

검증 신호:

- 2026-03-07 기준 `make -C problem test`가 통과했다.
- 2026-03-07 기준 `make -C problem bench`가 통과했다.

다음:

- 다음 글에서는 `20-log-abstraction-and-rotation.md`에서 이어지는 경계를 다룬다.

## 마무리

이 글을 따로 떼어 쓴 이유는 결과 요약보다 구현 순서가 먼저 보이게 하기 위해서다. `solution/go/log/store.go` 같은 결정적인 코드와 `cd 02-distributed-systems/13-distributed-log-core` 같은 검증 명령이 같은 글 안에 있어야, 이 프로젝트가 어떤 경계부터 닫았는지 추적할 수 있다.
