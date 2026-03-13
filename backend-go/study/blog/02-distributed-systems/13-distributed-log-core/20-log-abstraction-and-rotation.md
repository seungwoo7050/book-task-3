# 13 Distributed Log Core — Log Abstraction And Rotation

`02-distributed-systems/13-distributed-log-core`는 append-only store, mmap index, segment rotation, log abstraction을 직접 구현해 commit log 핵심을 익히는 대표 과제다. 이 글에서는 5단계: Log 구현 (다중 Segment 관리) -> 6단계: 에러 정의 구간을 따라가면서, 어떤 파일과 어떤 명령이 실제 구현 전환점이었는지 복원한다.

## 구현 순서 요약

- 5단계: Log 구현 (다중 Segment 관리)
- 6단계: 에러 정의

## Day 1
### Session 1

- 당시 목표: mmap index와 segment rotation을 테스트 및 benchmark와 함께 정리했다.
- 변경 단위: `log/log.go`, `log/errors.go`
- 처음 가설: 파일 포맷과 segment lifecycle을 먼저 구현해 분산 복제 이전의 로컬 불변식을 학습하게 했다.
- 실제 진행: `log/log.go` 작성. 주요 결정: `setup()`: 디렉토리 스캔 → `.store` 파일 파싱 → baseOffset 정렬 → Segment 복원 `Append()`: activeSegment.IsFull()이면 newSegment() 호출 `Read()`: `sort.Search`로 이진 탐색 → 올바른 Segment 찾기 `Truncate(lowest)`: lowest 미만의 Segment 모두 삭제 `Reset()`: `os.RemoveAll` → 새 Segment로 재시작 `log/errors.go` — 5개 sentinel error 정의.

CLI:

```bash
# Log 전체 테스트
go test ./log/ -run TestLog -v
```

검증 신호:

- 이 구간에서 실행 진입점과 검증 명령이 처음 함께 닫혔다.

핵심 코드: `solution/go/log/log.go`

```go
type Log struct {
	mu            sync.RWMutex
	dir           string
	config        Config
	segments      []*segment
	activeSegment *segment
}

// NewLog는 로그 디렉터리를 열고 기존 세그먼트를 복구한다.
func NewLog(dir string, c Config) (*Log, error) {
	if c.MaxStoreBytes == 0 {
		c.MaxStoreBytes = 1024 * 1024 // 1 MB
	}
	if c.MaxIndexBytes == 0 {
		c.MaxIndexBytes = 1024 * 1024 // 1 MB
	}

	l := &Log{
```

왜 이 코드가 중요했는가:

이 조각은 프로젝트의 핵심 판단이 실제 어느 함수와 자료구조에 걸려 있는지 보여 준다. 추상 요약보다 먼저 이 코드를 봐야 구현 순서가 살아난다.

새로 배운 것:

- index는 logical offset을 물리 위치로 빠르게 찾기 위한 보조 구조다.

보조 코드: `solution/go/log/index.go`

```go
type index struct {
	file *os.File
	mmap []byte
	size uint64 // 실제로 사용 중인 엔트리 바이트 수
	max  uint64 // 미리 확보한 최대 파일 크기
}

// newIndex는 파일을 메모리 매핑하고 최대 크기를 설정한다.
func newIndex(f *os.File, maxBytes uint64) (*index, error) {
	fi, err := os.Stat(f.Name())
	if err != nil {
		return nil, err
	}
	size := uint64(fi.Size())

	// mmap 전에 파일을 최대 크기까지 확장한다.
	if err := f.Truncate(int64(maxBytes)); err != nil {
		return nil, err
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

- 다음 글에서는 `30-tests-and-bench-evidence.md`에서 이어지는 경계를 다룬다.

## 마무리

이 글을 따로 떼어 쓴 이유는 결과 요약보다 구현 순서가 먼저 보이게 하기 위해서다. `solution/go/log/log.go` 같은 결정적인 코드와 `cd 02-distributed-systems/13-distributed-log-core` 같은 검증 명령이 같은 글 안에 있어야, 이 프로젝트가 어떤 경계부터 닫았는지 추적할 수 있다.
