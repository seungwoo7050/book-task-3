# 10 Concurrency Patterns — Pipeline Cancellation And Bench

`01-backend-core/10-concurrency-patterns`는 worker pool과 pipeline을 통해 goroutine lifecycle, channel, cancellation을 직접 다루는 본선 과제다. 이 글에서는 7단계: Pipeline 함수 구현 (pipeline/pipeline.go) -> 8단계: CMD 예제 작성 -> 9단계: 테스트 작성 -> 10단계: 벤치마크 -> 11단계: Race detector 구간을 따라가면서, 어떤 파일과 어떤 명령이 실제 구현 전환점이었는지 복원한다.

## 구현 순서 요약

- 7단계: Pipeline 함수 구현 (pipeline/pipeline.go)
- 8단계: CMD 예제 작성
- 9단계: 테스트 작성
- 10단계: 벤치마크
- 11단계: Race detector

## Day 1
### Session 1

- 당시 목표: 검증 명령과 공개 surface를 함께 닫고 `verified` 기준을 다시 확인한다.
- 변경 단위: `solution/go/pipeline/pipeline.go`, `solution/go/pipeline/pipeline_test.go`
- 처음 가설: goroutine leak 방지를 핵심 검증 기준으로 잡아 단순 병렬 처리 예제와 구분했다.
- 실제 진행: 순서: `Generate` — start~end 정수 생성, 채널 반환 `Filter` — predicate 만족하는 값만 통과 `Sink` — 채널의 모든 값을 슬라이스로 수집 `FanOut` — n개의 goroutine으로 병렬 처리 Worker Pool 데모 20개의 Job(1~20의 제곱)을 4 worker로 처리: Worker Pool 테스트: 모든 Job이 처리됨 확인 Stop 후 goroutine 누수 없음 확인 context cancellation으로 즉시 종료

CLI:

```bash
go run ./cmd/workerpool

go run ./cmd/pipeline
```

검증 신호:

- `Filter` — predicate 만족하는 값만 통과
- 2026-03-07 기준 `make -C problem test`가 통과했다.
- 2026-03-07 기준 `make -C problem bench`가 통과했다.
- 남은 선택 검증: 실서비스 queue/backpressure 정책은 별도 과제로 남겼다.

핵심 코드: `solution/go/pipeline/pipeline.go`

```go
func Generate(ctx context.Context, start, end int) <-chan int {
	out := make(chan int)

	go func() {
		defer close(out)
		for i := start; i <= end; i++ {
			select {
			case <-ctx.Done():
				return
			case out <- i:
			}
		}
	}()

	return out
}

// Filter는 predicate가 true인 값만 다음 단계로 전달한다.
```

왜 이 코드가 중요했는가:

이 블록은 병렬성과 보호 정책을 아이디어가 아니라 코드 invariant로 바꾼다. goroutine, channel, token을 어떤 경계로 묶었는지가 여기서 드러난다.

새로 배운 것:

- pipeline은 단계별 channel 연결로 데이터 흐름을 분리한다.

보조 코드: `solution/go/pipeline/pipeline_test.go`

```go
func TestGenerateBasic(t *testing.T) {
	ctx := context.Background()
	ch := Generate(ctx, 1, 5)

	var got []int
	for v := range ch {
		got = append(got, v)
	}

	want := []int{1, 2, 3, 4, 5}
	if len(got) != len(want) {
		t.Fatalf("got %d values, want %d", len(got), len(want))
	}
	for i, v := range got {
		if v != want[i] {
			t.Errorf("got[%d] = %d, want %d", i, v, want[i])
		}
	}
```

왜 이 코드도 같이 봐야 하는가:

이 블록은 병렬성과 보호 정책을 아이디어가 아니라 코드 invariant로 바꾼다. goroutine, channel, token을 어떤 경계로 묶었는지가 여기서 드러난다.

CLI:

```bash
cd 01-backend-core/10-concurrency-patterns
make -C problem test
make -C problem bench
```

검증 신호:

- 2026-03-07 기준 `make -C problem test`가 통과했다.
- 2026-03-07 기준 `make -C problem bench`가 통과했다.

다음:

- 실서비스 queue/backpressure 정책은 별도 과제로 남겼다.

## 마무리

이 글을 따로 떼어 쓴 이유는 결과 요약보다 구현 순서가 먼저 보이게 하기 위해서다. `solution/go/pipeline/pipeline.go` 같은 결정적인 코드와 `cd 01-backend-core/10-concurrency-patterns` 같은 검증 명령이 같은 글 안에 있어야, 이 프로젝트가 어떤 경계부터 닫았는지 추적할 수 있다.
