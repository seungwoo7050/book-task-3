# 지식 색인 — 동시성 패턴 핵심 개념

## Goroutine

Go의 경량 스레드. OS 스레드보다 수천 배 가볍다(초기 스택 ~4KB). `go func()` 키워드로 시작한다. Go 런타임의 스케줄러가 OS 스레드에 다중화(multiplexing)한다.

## Channel

goroutine 간 통신 수단. 데이터를 안전하게 전달하면서 동기화까지 제공한다.

```go
ch := make(chan int)      // 언버퍼드: 보내기/받기가 동시에 일어남
ch := make(chan int, 10)  // 버퍼드: 버퍼가 찰 때까지 보내기 가능
```

## Worker Pool

N개의 goroutine이 공유 채널에서 작업을 꺼내 처리하는 패턴. 동시 처리량을 조절할 수 있다. 핵심 구성: jobs 채널, results 채널, WaitGroup, context.

## Pipeline

여러 단계를 채널로 연결하는 패턴. 각 단계가 독립된 goroutine에서 실행된다. Unix 파이프와 동일한 구조.

```
Generate(1..N) → Filter(odd?) → Sink(collect)
```

## FanOut

하나의 입력 채널을 여러 goroutine이 동시에 읽는 패턴. 병렬 처리를 극대화한다. 결과 순서는 보장되지 않는다.

## context.WithCancel

취소 가능한 context를 생성한다. `cancel()` 호출 시 `ctx.Done()` 채널이 닫히고, 이를 `select`로 감지한 goroutine이 즉시 종료한다.

```go
ctx, cancel := context.WithCancel(parent)
defer cancel()
```

## sync.WaitGroup

여러 goroutine의 완료를 기다리는 카운터.

```go
wg.Add(n)           // goroutine 시작 전에 호출
go func() {
    defer wg.Done() // goroutine 종료 시
    // ...
}()
wg.Wait()           // 모든 goroutine 완료 대기
```

`Add`는 반드시 goroutine 시작 전에 호출한다.

## select

여러 채널 연산 중 준비된 것을 실행하는 Go의 다중화 구문.

```go
select {
case val := <-ch1:    // ch1에서 값이 오면
case ch2 <- data:     // ch2에 보낼 수 있으면
case <-ctx.Done():    // context 취소 시
default:              // 위 중 아무것도 준비 안 되면 (non-blocking)
}
```

## Back-pressure

생산자가 소비자보다 빠를 때, 채널 버퍼가 차면 생산자가 블로킹되어 속도가 조절되는 메커니즘. 별도 구현 없이 Go 채널이 자연스럽게 제공한다.

## Graceful Shutdown

진행 중인 작업을 마무리한 후 종료하는 것. Worker Pool에서: `close(jobs)` → 남은 job 처리 → worker 종료 → `close(results)`.

## 채널 닫기 규칙

1. 보내는 쪽만 닫는다
2. 이미 닫힌 채널에 보내면 panic
3. 닫힌 채널에서 받으면 zero value 반환
4. `val, ok := <-ch`에서 `ok`가 false면 채널이 닫힘
