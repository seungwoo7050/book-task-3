# 디버그 기록 — 동시성 코드에서 흔한 실수들

## Goroutine 누수

Worker pool에서 `close(p.results)`를 하지 않으면, 소비자(`range pool.Results()`)가 영원히 블로킹된다. 반대로 결과를 수집하지 않으면 worker가 result 채널에 쓰려다 영원히 블로킹된다.

**진단**: `go test -race`는 race condition은 잡지만 goroutine 누수는 잡지 못한다. 테스트 마지막에 `runtime.NumGoroutine()`을 확인하거나, `goleak` 패키지를 사용한다.

## 채널 닫기 규칙

- **보내는 쪽이 닫는다**: `Generate`가 `out`을 닫고, `Filter`가 자신의 `out`을 닫는다.
- **받는 쪽은 닫지 않는다**: `Sink`는 입력 채널을 닫지 않는다.
- **이미 닫힌 채널에 보내면 panic**: `Send on closed channel`. runtime recovery 불가.

## select에서 default 사용 주의

```go
// 위험:
select {
case val := <-ch:
    process(val)
default:
    // ch에 값이 없으면 즉시 여기로
}
```

이렇게 하면 CPU를 100% 사용하는 busy loop가 된다. `default`는 non-blocking 확인이 정말 필요할 때만 써야 한다. Filter에서 context 확인용으로 `default`를 사용한 건, 값이 이미 range로 들어온 뒤이므로 안전하다.

## WaitGroup Add/Done 불균형

```go
p.wg.Add(workers)  // NewPool에서
for i := 0; i < workers; i++ {
    go p.worker()   // 각 worker에서 defer p.wg.Done()
}
```

`Add`를 goroutine 안에서 하면 `Wait()`가 먼저 실행될 수 있다. 반드시 goroutine 시작 전에 `Add`를 호출한다.

## 버퍼드 vs 언버퍼드 채널

Pipeline의 Generate, Filter, Sink는 **언버퍼드** 채널을 쓴다. 각 단계의 속도가 비슷하면 언버퍼드가 동기화에 유리하다.

Worker Pool의 jobs, results는 **버퍼드** (`workers * 2`). Submit이 블로킹되는 빈도를 줄인다.

잘못된 직관: "버퍼를 크게 하면 빨라진다." → 아니다. 버퍼는 일시적 속도 차이를 흡수할 뿐이다. 근본적으로 생산자가 소비자보다 빠르면 버퍼 크기와 무관하게 블로킹된다.

## context.WithCancel 후 cancel 호출 누락

```go
ctx, cancel := context.WithCancel(ctx)
// cancel()을 한 번도 안 하면 ctx는 garbage collect되지만,
// parent가 살아있으면 child도 GC되지 않을 수 있다.
```

`Pool`에서는 `Cancel()` 메서드로 명시적으로 호출할 수 있게 했다. 사용하지 않더라도 defer로 cancel을 호출하는 습관이 좋다.
