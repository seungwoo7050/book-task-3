// Package pipeline은 채널 기반 generator -> filter -> sink 패턴을 구현한다.
package pipeline

import "context"

// Generate는 start부터 end까지의 정수를 순서대로 생성한다.
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
func Filter(ctx context.Context, in <-chan int, predicate func(int) bool) <-chan int {
	out := make(chan int)

	go func() {
		defer close(out)
		for val := range in {
			select {
			case <-ctx.Done():
				return
			default:
			}
			if predicate(val) {
				select {
				case out <- val:
				case <-ctx.Done():
					return
				}
			}
		}
	}()

	return out
}

// Sink는 입력 채널의 값을 모두 수집해 슬라이스로 반환한다.
func Sink(ctx context.Context, in <-chan int) []int {
	var result []int

	for {
		select {
		case <-ctx.Done():
			return result
		case val, ok := <-in:
			if !ok {
				return result
			}
			result = append(result, val)
		}
	}
}

// FanOut은 입력 작업을 n개의 worker goroutine으로 분산 처리하고 결과를 하나로 모은다.
func FanOut(ctx context.Context, in <-chan int, n int, worker func(int) int) <-chan int {
	out := make(chan int)
	done := make(chan struct{})

	for i := 0; i < n; i++ {
		go func() {
			defer func() { done <- struct{}{} }()
			for val := range in {
				select {
				case <-ctx.Done():
					return
				case out <- worker(val):
				}
			}
		}()
	}

	// 모든 worker가 끝나면 결과 채널을 닫는다.
	go func() {
		for i := 0; i < n; i++ {
			<-done
		}
		close(out)
	}()

	return out
}
