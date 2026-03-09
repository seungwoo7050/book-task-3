# 접근 과정 — Worker Pool과 Pipeline 구현

## Part 1: Worker Pool

### Pool 구조체

```go
type Pool struct {
    ctx     context.Context
    cancel  context.CancelFunc
    jobs    chan Job
    results chan Result
    handler func(Job) Result
    wg      sync.WaitGroup
}
```

- `jobs`: 버퍼드 채널 (`workers * 2`). 제출자(Submit)가 블로킹 없이 몇 개를 미리 넣을 수 있게.
- `results`: 처리 결과를 받는 버퍼드 채널.
- `wg`: 모든 worker가 끝났는지 추적. Stop()에서 `wg.Wait()`.
- `ctx/cancel`: context cancellation으로 즉시 종료 지원.

### worker 루프

```go
func (p *Pool) worker() {
    defer p.wg.Done()
    for {
        select {
        case <-p.ctx.Done():
            return
        case job, ok := <-p.jobs:
            if !ok { return }
            result := p.handler(job)
            select {
            case p.results <- result:
            case <-p.ctx.Done():
                return
            }
        }
    }
}
```

두 중첩된 `select`가 핵심이다. 바깥 select는 "새 job을 받을지, 종료할지"를 결정한다. 안쪽 select는 "result를 보낼 수 있는지, 종료됐는지"를 확인한다. 이렇게 해야 context가 취소될 때 result 채널이 가득 차서 영원히 블로킹되는 상황을 방지한다.

### results 채널 닫기

```go
go func() {
    p.wg.Wait()
    close(p.results)
}()
```

모든 worker가 끝나면 results를 닫는다. 소비자 쪽에서 `range pool.Results()`로 깔끔하게 순회할 수 있다.

### Submit과 back-pressure

```go
func (p *Pool) Submit(job Job) {
    select {
    case p.jobs <- job:
    case <-p.ctx.Done():
    }
}
```

jobs 버퍼가 가득 차면 Submit이 블로킹된다. 이것이 back-pressure다. 생산자가 소비자보다 빠르면 자연스럽게 감속된다.

### Stop vs Cancel

- `Stop()`: `close(p.jobs)` → worker가 남은 job을 마저 처리 → `wg.Wait()` → results 닫힘
- `Cancel()`: `p.cancel()` → worker가 즉시 종료 → 처리 중인 job 포기

Graceful shutdown은 Stop, 긴급 종료는 Cancel.

## Part 2: Pipeline

### Generate

```go
func Generate(ctx context.Context, start, end int) <-chan int {
    out := make(chan int)
    go func() {
        defer close(out)
        for i := start; i <= end; i++ {
            select {
            case <-ctx.Done(): return
            case out <- i:
            }
        }
    }()
    return out
}
```

반환 타입이 `<-chan int`(읽기 전용)인 게 중요하다. 호출자가 닫을 수 없게 한다. 채널을 만든 쪽이 닫는다.

### Filter

```go
func Filter(ctx context.Context, in <-chan int, predicate func(int) bool) <-chan int
```

입력 채널에서 읽고, 조건을 만족하는 값만 출력 채널로 보낸다. `range in`으로 순회하되, 각 반복에서 context를 체크한다.

### Sink

```go
func Sink(ctx context.Context, in <-chan int) []int
```

채널의 모든 값을 슬라이스로 수집한다. context가 취소되면 수집된 부분만 반환한다.

### FanOut

```go
func FanOut(ctx context.Context, in <-chan int, n int, worker func(int) int) <-chan int
```

하나의 입력 채널을 n개의 goroutine이 동시에 읽고, 처리 결과를 하나의 출력 채널로 모은다. 모든 goroutine이 끝나면 출력 채널을 닫는다.

## 조합 예시

```go
gen := Generate(ctx, 1, 50)
primes := Filter(ctx, gen, isPrime)
result := Sink(ctx, primes)
```

각 단계가 독립된 goroutine이고 채널로 연결된다. Unix 파이프(`ls | grep | wc`)와 동일한 구조.
