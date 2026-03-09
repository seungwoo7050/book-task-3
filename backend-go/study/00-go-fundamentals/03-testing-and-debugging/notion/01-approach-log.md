# 접근 과정 — 테스트 구조를 세우기까지

## ParseLine부터 만들기

가장 먼저 `ParseLine` 함수를 만들었다. `"category,duration_ms"` 형식의 한 줄을 받아서 `Event` struct를 반환한다. `strings.Split`으로 쉼표 기준으로 자르고, `strconv.Atoi`로 숫자를 변환한다.

여기서 에러 케이스가 세 가지 생겼다:
1. 쉼표가 없으면 → `"invalid line"` 에러
2. duration이 숫자가 아니면 → `"invalid duration"` 에러 (fmt.Errorf로 원본 에러 래핑)
3. category가 빈 문자열이면 → `"empty category"` 에러

이 세 가지를 자연스럽게 테스트로 옮기면 table-driven test가 된다.

## table-driven test의 구조

Go에서 table-driven test는 관용구다. 테스트 케이스를 struct 슬라이스로 정의하고, `for` 루프에서 `t.Run`으로 subtest를 만든다.

```go
tests := []struct {
    name    string
    line    string
    wantErr bool
}{
    {name: "valid", line: "search,120"},
    {name: "missing comma", line: "search", wantErr: true},
    {name: "empty category", line: ",10", wantErr: true},
}
```

처음에 이 구조가 과하게 느껴졌다. 테스트 3개면 그냥 함수를 3개 쓰면 되지 않나? 하지만 케이스가 10개, 20개로 늘어나면 이야기가 달라진다. 새 케이스를 추가할 때 테이블에 한 줄만 넣으면 끝이다. 이 확장성이 table-driven test의 핵심이다.

## subtest로 실패 지점 드러내기

`t.Run(tc.name, ...)` 으로 각 케이스에 이름을 붙이면, 실패했을 때 어떤 케이스가 깨졌는지가 출력에 바로 나온다.

```
--- FAIL: TestParseLine/empty_category (0.00s)
```

이름이 없으면 "3번째 케이스가 실패했다"는 메시지만 보고 어떤 입력이었는지 줄 번호를 세어야 한다. 이름 하나 붙이는 것만으로 디버깅 시간이 크게 줄어든다.

## Summarize — 여러 줄을 모아서 통계 내기

`Summarize` 함수는 `ParseLine`을 반복 호출하면서 category별로 카운트, 합계, 평균을 누적한다. 여기서 "map의 zero value"를 활용했다. `summaries["search"]`가 처음 접근되면 `Summary{}`가 반환되는데, Count가 0이므로 바로 1을 더하면 된다.

## Recorder — race-safe하게 만들기

`Recorder`는 여러 goroutine에서 이벤트를 동시에 추가할 수 있어야 한다. 가장 단순한 방법은 `sync.Mutex`로 보호하는 것이다.

```go
func (r *Recorder) Add(event Event) {
    r.mu.Lock()
    defer r.mu.Unlock()
    r.events = append(r.events, event)
}
```

`Snapshot` 메서드는 내부 슬라이스의 복사본을 반환한다. 이게 중요한 이유는, 슬라이스를 그대로 반환하면 외부에서 참조하는 동안 `Add`가 호출돼서 데이터가 변경될 수 있기 때문이다. `copy`로 독립적인 슬라이스를 만들어야 안전하다.

## Benchmark 추가

```go
func BenchmarkSummarize(b *testing.B) {
    lines := make([]string, 0, 1000)
    for i := 0; i < 1000; i++ {
        lines = append(lines, fmt.Sprintf("search,%d", i%300))
    }
    b.ResetTimer()
    for i := 0; i < b.N; i++ {
        Summarize(lines)
    }
}
```

`b.ResetTimer()`를 데이터 셋업 뒤에 호출해야 준비 시간이 측정에 포함되지 않는다. 이건 처음에 빼먹기 쉬운 부분이다. 1000줄의 로그를 사용한 건 너무 작으면 벤치마크 수치가 의미 없고, 너무 크면 실행이 느려져서 피드백 루프가 깨지기 때문이다.
