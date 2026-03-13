# 13 Distributed Log Core — Tests And Bench Evidence

`02-distributed-systems/13-distributed-log-core`는 append-only store, mmap index, segment rotation, log abstraction을 직접 구현해 commit log 핵심을 익히는 대표 과제다. 이 글에서는 7단계: 전체 테스트 및 검증 -> 8단계: go.work 등록 구간을 따라가면서, 어떤 파일과 어떤 명령이 실제 구현 전환점이었는지 복원한다.

## 구현 순서 요약

- 7단계: 전체 테스트 및 검증
- 8단계: go.work 등록

## Day 1
### Session 1

- 당시 목표: 검증 명령과 공개 surface를 함께 닫고 `verified` 기준을 다시 확인한다.
- 변경 단위: `solution/go/log/log_test.go`, `solution/go/log/segment_test.go`
- 처음 가설: 파일 포맷과 segment lifecycle을 먼저 구현해 분산 복제 이전의 로컬 불변식을 학습하게 했다.
- 실제 진행: 

CLI:

```bash
# 전체 테스트 실행
cd 13-distributed-log-core/go
go test ./... -v

# 커버리지 측정
go test ./log/ -coverprofile=coverage.out
go tool cover -html=coverage.out

# Race condition 검사
go test ./log/ -race -v

# study/go.work에 모듈 추가
cd ../../
# go.work에 use ./02-distributed-systems/13-distributed-log-core/go 추가
```

검증 신호:

- 2026-03-07 기준 `make -C problem test`가 통과했다.
- 2026-03-07 기준 `make -C problem bench`가 통과했다.
- 남은 선택 검증: replication layer는 study 본선 범위에서 제외했다.

핵심 코드: `solution/go/log/log_test.go`

```go
func TestLogAppendRead(t *testing.T) {
	dir, err := os.MkdirTemp("", "log_test")
	if err != nil {
		t.Fatal(err)
	}
	defer os.RemoveAll(dir)

	c := Config{
		MaxStoreBytes: 1024,
		MaxIndexBytes: indexEntryWidth * 100,
	}

	l, err := NewLog(dir, c)
	if err != nil {
		t.Fatal(err)
	}
	defer l.Close()
```

왜 이 코드가 중요했는가:

이 테스트나 재현 스크립트는 프로젝트의 공개 표면을 말이 아니라 입력과 결과로 고정한다. 최종 글에서 이 증거를 빼면 구현은 보여도 완료 기준은 흐려진다.

새로 배운 것:

- segment는 store와 index를 묶은 관리 단위다.

보조 코드: `solution/go/log/segment_test.go`

```go
func TestSegmentAppendRead(t *testing.T) {
	dir, err := os.MkdirTemp("", "segment_test")
	if err != nil {
		t.Fatal(err)
	}
	defer os.RemoveAll(dir)

	c := Config{
		MaxStoreBytes: 1024,
		MaxIndexBytes: indexEntryWidth * 10,
	}

	seg, err := newSegment(dir, 16, c)
	if err != nil {
		t.Fatal(err)
	}

	records := [][]byte{
```

왜 이 코드도 같이 봐야 하는가:

이 테스트나 재현 스크립트는 프로젝트의 공개 표면을 말이 아니라 입력과 결과로 고정한다. 최종 글에서 이 증거를 빼면 구현은 보여도 완료 기준은 흐려진다.

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

- replication layer는 study 본선 범위에서 제외했다.

## 마무리

이 글을 따로 떼어 쓴 이유는 결과 요약보다 구현 순서가 먼저 보이게 하기 위해서다. `solution/go/log/log_test.go` 같은 결정적인 코드와 `cd 02-distributed-systems/13-distributed-log-core` 같은 검증 명령이 같은 글 안에 있어야, 이 프로젝트가 어떤 경계부터 닫았는지 추적할 수 있다.
