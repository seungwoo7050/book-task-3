# 디버그 기록 — 어디서 막혔고 어떻게 풀었나

## race detector가 잡아낸 것

`Recorder`를 처음 만들었을 때 mutex 없이 슬라이스에 직접 append했다. `go test`로는 통과했지만, `-race` 플래그를 붙이자 즉시 경고가 나왔다.

```bash
go test -race ./...
```

```
WARNING: DATA RACE
Read at 0x... by goroutine 8:
  ...
Previous write at 0x... by goroutine 7:
  ...
```

race detector는 실제로 문제가 발생하는 게 아니라, 동시 접근이 보호되지 않은 지점을 찾아서 보고한다. 이 도구가 없으면 "가끔 되고 가끔 안 되는" 증상만 보고 원인을 추측해야 한다. Go의 `-race` 플래그가 기본 도구 체인에 포함돼 있다는 건 큰 장점이었다.

## Snapshot에서 슬라이스를 복사하지 않았을 때

처음에 `Snapshot`을 이렇게 썼다:

```go
func (r *Recorder) Snapshot() []Event {
    r.mu.Lock()
    defer r.mu.Unlock()
    return r.events  // 내부 슬라이스 참조를 그대로 반환
}
```

이렇게 하면 잠금을 풀고 나서 외부 코드가 반환된 슬라이스를 읽는 동안 `Add`가 호출될 수 있다. race detector가 이것도 잡아냈다. `copy`로 독립 슬라이스를 만들어 반환하니 해결됐다.

이 경험은 "lock을 건 안에서 데이터를 반환할 때, 참조가 아니라 값을 복사해야 한다"는 원칙을 체화하게 만들었다.

## 테스트 케이스의 tc 캡처

Go 1.22 이전에는 table-driven test에서 루프 변수 문제가 있었다:

```go
for _, tc := range tests {
    tc := tc  // 루프 변수를 로컬로 캡처
    t.Run(tc.name, func(t *testing.T) {
        t.Parallel()
        // tc를 안전하게 사용
    })
}
```

`tc := tc`를 빼먹으면 모든 subtest가 마지막 케이스의 값으로 실행된다. Go 1.22부터는 루프 변수의 semantics가 바뀌어서 이 문제가 해결됐지만, 이전 버전과의 호환성과 명시성을 위해 캡처를 남겨 뒀다.

## benchmark에서 b.ResetTimer 누락

처음에 `b.ResetTimer()`을 넣지 않았더니, 1000줄의 로그를 생성하는 셋업 시간이 측정에 포함됐다. 벤치마크 수치가 실제 처리 시간보다 유의미하게 높게 나왔다. 셋업과 측정 구간을 명확히 분리하는 건 벤치마크의 기본이지만, 처음에는 놓치기 쉬운 부분이다.
