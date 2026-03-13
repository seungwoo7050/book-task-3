# 13 Distributed Log Core Evidence Ledger

이 문서는 기존 `blog/` 초안을 입력으로 읽지 않고, 살아 있는 근거만으로 chronology를 복원한 ledger다.

## 근거 묶음

- 프로젝트 요약: append-only store, mmap index, segment rotation, log abstraction을 직접 구현해 commit log 핵심을 익히는 대표 과제다.
- 구현 디렉터리: `solution/go`
- 주요 구현 파일: `solution/go/log/store.go`, `solution/go/log/log.go`, `solution/go/log/log_test.go`
- 대표 검증 명령: `cd solution/go && go test -run TestLogRestore -v ./log`, `cd solution/go && go test ./log/... -bench=.`
- 핵심 개념 축: `store는 레코드 바이트를 순차 append하는 역할이다.`, `index는 logical offset을 물리 위치로 빠르게 찾기 위한 보조 구조다.`, `segment는 store와 index를 묶은 관리 단위다.`, `log는 여러 segment를 회전시키며 append-only 추상화를 제공한다.`
- chronology 복원 주석: 이 경로의 git 이력은 대체로 큰 source drop과 문서 보강 위주라 세밀한 시각 정보를 주지 못한다. 그래서 chronology는 README, 살아 있는 소스코드, 테스트, 현재 CLI 재실행 결과를 기준으로 Phase 1/2/3 형태로 복원했다.

## Git History Anchor

- `2026-03-08 46051f3 A large commit`
- `2026-03-09 69364e2 docs(notion): backend-go`
- `2026-03-12 0e12fb8 Track 3에 대한 전반적인 개선 완료 (backend go/node/spring, front react )`

## Chronology Ledger

                ### 1. Phase 1 - store와 index로 바이트, offset primitive를 먼저 고정한다

        - 당시 목표: store와 index로 바이트, offset primitive를 먼저 고정한다
        - 변경 단위: `solution/go/log/store.go`의 `store.Append`
        - 처음 가설: `store.Append` 같은 바이트 단위 primitive가 먼저 안정돼야 segment와 log 조합을 설명할 수 있다고 봤다.
        - 실제 조치: `solution/go/log/store.go`의 `store.Append`를 통해 offset과 byte append primitive를 먼저 고정했다.
        - CLI: `cd solution/go && go test -run TestLogRestore -v ./log`
        - 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `=== RUN   TestLogRestore`였다.
        - 핵심 코드 앵커:
        - `store.Append`: `solution/go/log/store.go`

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

        - 새로 배운 것: store는 레코드 바이트를 순차 append하는 역할이다.
        - 다음: segment와 Log로 append-only composition을 완성한다
        ### 2. Phase 2 - segment와 Log로 append-only composition을 완성한다

        - 당시 목표: segment와 Log로 append-only composition을 완성한다
        - 변경 단위: `solution/go/log/log.go`의 `Log.Append`
        - 처음 가설: `Log.Append`에 append path를 모으면 segment split과 reopen 규칙을 한 흐름으로 읽을 수 있다고 판단했다.
        - 실제 조치: `solution/go/log/log.go`의 `Log.Append`에서 segment rotation과 append-only log composition을 묶었다.
        - CLI: `cd solution/go && go test ./log/... -bench=.`
        - 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `goos: darwin`였다.
        - 핵심 코드 앵커:
        - `Log.Append`: `solution/go/log/log.go`

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

        - 새로 배운 것: replication을 빼면 범위는 줄지만 “분산”이라는 이름이 다소 강하게 들릴 수 있다.
        - 다음: restore, truncate tests와 benchmark로 durability 계약을 잠근다
        ### 3. Phase 3 - restore, truncate tests와 benchmark로 durability 계약을 잠근다

        - 당시 목표: restore, truncate tests와 benchmark로 durability 계약을 잠근다
        - 변경 단위: `solution/go/log/log_test.go`의 `TestLogRestore`
        - 처음 가설: `TestLogRestore` 같은 회복 테스트가 있어야 durability를 진짜로 설명할 수 있다고 봤다.
        - 실제 조치: `solution/go/log/log_test.go`의 `TestLogRestore`와 benchmark를 통해 reopen, truncate, append path를 같이 검증했다.
        - CLI: `cd solution/go && go test ./log/... -bench=.`
        - 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `goos: darwin`였다.
        - 핵심 코드 앵커:
        - `TestLogRestore`: `solution/go/log/log_test.go`

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

        - 새로 배운 것: truncate/reset 시 store와 index를 같이 정리하지 않으면 논리적 오염이 남는다.
        - 다음: 최종 글은 이 세 phase를 같은 순서로 묶어 development log로 다시 쓴다.

## Latest CLI Excerpt

        ```bash
(cd /Users/woopinbell/work/book-task-3/study/02-distributed-systems/13-distributed-log-core && cd solution/go && go test -run TestLogRestore -v ./log)
```

```text
=== RUN   TestLogRestore
--- PASS: TestLogRestore (0.02s)
PASS
ok  	github.com/woopinbell/go-backend/study/02-distributed-systems/13-distributed-log-core/log	(cached)
```

```bash
(cd /Users/woopinbell/work/book-task-3/study/02-distributed-systems/13-distributed-log-core && cd solution/go && go test ./log/... -bench=.)
```

```text
goos: darwin
goarch: arm64
pkg: github.com/woopinbell/go-backend/study/02-distributed-systems/13-distributed-log-core/log
cpu: Apple M1
BenchmarkLogAppend-8     	 2452268	       445.6 ns/op
BenchmarkStoreAppend-8   	 3288534	       363.9 ns/op
PASS
ok  	github.com/woopinbell/go-backend/study/02-distributed-systems/13-distributed-log-core/log	3.433s
```
