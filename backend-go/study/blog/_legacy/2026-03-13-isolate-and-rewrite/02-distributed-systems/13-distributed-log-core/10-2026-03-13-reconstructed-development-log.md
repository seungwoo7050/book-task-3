# 13 Distributed Log Core 재구성 개발 로그

13 Distributed Log Core는 append-only store, mmap index, segment rotation, log abstraction을 직접 구현해 commit log 핵심을 익히는 대표 과제다.

이 글은 2026-03-13에 `isolate-and-rewrite` 방식으로 다시 쓴 버전이다. 기존 `study/blog/` 디렉터리가 없어서 격리할 초안은 없었다. 세밀한 shell history가 남아 있지 않아 시간 표지는 `Phase 1/2/3`처럼 재구성했고, 근거는 README, 살아 있는 소스코드, docs, 테스트, 현재 CLI 재실행 결과만 사용했다.

## 구현 순서 요약

- Phase 1: store와 index로 바이트, offset primitive를 먼저 고정한다 - `solution/go/log/store.go`의 `store.Append`
- Phase 2: segment와 Log로 append-only composition을 완성한다 - `solution/go/log/log.go`의 `Log.Append`
- Phase 3: restore, truncate tests와 benchmark로 durability 계약을 잠근다 - `solution/go/log/log_test.go`의 `TestLogRestore`

## Phase 1. store와 index로 바이트, offset primitive를 먼저 고정한다

- 당시 목표: store와 index로 바이트, offset primitive를 먼저 고정한다
- 변경 단위: `solution/go/log/store.go`의 `store.Append`
- 처음 가설: `store.Append` 같은 바이트 단위 primitive가 먼저 안정돼야 segment와 log 조합을 설명할 수 있다고 봤다.
- 실제 진행: `solution/go/log/store.go`의 `store.Append`를 통해 offset과 byte append primitive를 먼저 고정했다.
- CLI: `cd solution/go && go test -run TestLogRestore -v ./log`
- 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `=== RUN   TestLogRestore`였다.

핵심 코드:

```go
// Append는 현재 파일 끝에 레코드를 추가하고, 기록한 바이트 수와 시작 위치를 반환한다.
func (s *store) Append(data []byte) (n uint64, pos uint64, err error) {
	s.mu.Lock()
	defer s.mu.Unlock()

	pos = s.size

	// 길이 접두사를 먼저 기록한다.
	if err = binary.Write(s.buf, enc, uint64(len(data))); err != nil {
		return 0, 0, err
```

왜 이 코드가 중요했는가: `store.Append`는 `solution/go/log/store.go`에서 판단이 실제로 갈린 지점을 보여 준다. 이 줄이 먼저 고정되어야 다음 phase의 공개 surface나 검증 고리가 과도하게 복잡해지지 않는다.

- 새로 배운 것: store는 레코드 바이트를 순차 append하는 역할이다.
- 다음: segment와 Log로 append-only composition을 완성한다
## Phase 2. segment와 Log로 append-only composition을 완성한다

- 당시 목표: segment와 Log로 append-only composition을 완성한다
- 변경 단위: `solution/go/log/log.go`의 `Log.Append`
- 처음 가설: `Log.Append`에 append path를 모으면 segment split과 reopen 규칙을 한 흐름으로 읽을 수 있다고 판단했다.
- 실제 진행: `solution/go/log/log.go`의 `Log.Append`에서 segment rotation과 append-only log composition을 묶었다.
- CLI: `cd solution/go && go test ./log/... -bench=.`
- 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `goos: darwin`였다.

핵심 코드:

```go
// Append는 활성 세그먼트에 레코드를 추가하고 절대 오프셋을 반환한다.
func (l *Log) Append(data []byte) (uint64, error) {
	l.mu.Lock()
	defer l.mu.Unlock()

	if l.activeSegment.IsFull() {
		nextBase := l.activeSegment.nextOffset
		if err := l.newSegment(nextBase); err != nil {
			return 0, err
		}
```

왜 이 코드가 중요했는가: `Log.Append`는 `solution/go/log/log.go`에서 판단이 실제로 갈린 지점을 보여 준다. 이 줄이 먼저 고정되어야 다음 phase의 공개 surface나 검증 고리가 과도하게 복잡해지지 않는다.

- 새로 배운 것: replication을 빼면 범위는 줄지만 “분산”이라는 이름이 다소 강하게 들릴 수 있다.
- 다음: restore, truncate tests와 benchmark로 durability 계약을 잠근다
## Phase 3. restore, truncate tests와 benchmark로 durability 계약을 잠근다

- 당시 목표: restore, truncate tests와 benchmark로 durability 계약을 잠근다
- 변경 단위: `solution/go/log/log_test.go`의 `TestLogRestore`
- 처음 가설: `TestLogRestore` 같은 회복 테스트가 있어야 durability를 진짜로 설명할 수 있다고 봤다.
- 실제 진행: `solution/go/log/log_test.go`의 `TestLogRestore`와 benchmark를 통해 reopen, truncate, append path를 같이 검증했다.
- CLI: `cd solution/go && go test ./log/... -bench=.`
- 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `goos: darwin`였다.

핵심 코드:

```go
func TestLogRestore(t *testing.T) {
	dir, err := os.MkdirTemp("", "log_restore_test")
	if err != nil {
		t.Fatal(err)
	}
	defer os.RemoveAll(dir)

	c := Config{
		MaxStoreBytes: 1024,
```

왜 이 코드가 중요했는가: `TestLogRestore`는 `solution/go/log/log_test.go`에서 판단이 실제로 갈린 지점을 보여 준다. 이 줄이 먼저 고정되어야 다음 phase의 공개 surface나 검증 고리가 과도하게 복잡해지지 않는다.

- 새로 배운 것: truncate/reset 시 store와 index를 같이 정리하지 않으면 논리적 오염이 남는다.
- 다음: 마지막엔 현재 저장소에서 다시 돌린 CLI와 남은 질문으로 닫는다.

## CLI 1. 현재 저장소에서 다시 돌린 검증

```bash
(cd /Users/woopinbell/work/book-task-3/backend-go/study/02-distributed-systems/13-distributed-log-core && cd solution/go && go test -run TestLogRestore -v ./log)
```

```text
=== RUN   TestLogRestore
--- PASS: TestLogRestore (0.02s)
PASS
ok  	github.com/woopinbell/go-backend/study/02-distributed-systems/13-distributed-log-core/log	(cached)
```
## CLI 2. 현재 저장소에서 다시 돌린 검증

```bash
(cd /Users/woopinbell/work/book-task-3/backend-go/study/02-distributed-systems/13-distributed-log-core && cd solution/go && go test ./log/... -bench=.)
```

```text
goos: darwin
goarch: arm64
pkg: github.com/woopinbell/go-backend/study/02-distributed-systems/13-distributed-log-core/log
cpu: Apple M1
BenchmarkLogAppend-8     	 2674910	       440.5 ns/op
BenchmarkStoreAppend-8   	 3445490	       330.8 ns/op
PASS
ok  	github.com/woopinbell/go-backend/study/02-distributed-systems/13-distributed-log-core/log	3.690s
```

## 이번 재작성에서 남은 것

- 이번 글을 지탱한 개념 축: store는 레코드 바이트를 순차 append하는 역할이다., index는 logical offset을 물리 위치로 빠르게 찾기 위한 보조 구조다., segment는 store와 index를 묶은 관리 단위다., log는 여러 segment를 회전시키며 append-only 추상화를 제공한다.
- 최신 검증 메모: 현재 저장소에서 다시 실행한 명령은 모두 exit 0으로 끝났다.
- 다음 질문: store, index, segment를 쌓아 append-only log가 reopen, segment split, truncate까지 버티게 만든다.
