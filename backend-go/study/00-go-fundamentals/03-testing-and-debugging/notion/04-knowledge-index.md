# 지식 인덱스 — 빠른 참조용

## go test 플래그

| 플래그 | 용도 | 예시 |
|--------|------|------|
| `-v` | 개별 테스트 이름과 결과 표시 | `go test -v ./...` |
| `-run` | 이름으로 테스트 필터 | `go test -run TestParseLine ./analyzer/` |
| `-bench` | 벤치마크 실행 | `go test -bench=. ./...` |
| `-race` | race detector 활성화 | `go test -race ./...` |
| `-count` | 테스트 반복 횟수 | `go test -count=5 -race ./...` |

## table-driven test 템플릿

```go
func TestFoo(t *testing.T) {
    t.Parallel()
    tests := []struct {
        name    string
        input   string
        want    int
        wantErr bool
    }{
        {name: "case1", input: "...", want: 42},
        {name: "error case", input: "bad", wantErr: true},
    }
    for _, tc := range tests {
        tc := tc
        t.Run(tc.name, func(t *testing.T) {
            t.Parallel()
            got, err := Foo(tc.input)
            if tc.wantErr && err == nil { t.Fatal("want error") }
            if !tc.wantErr && got != tc.want { t.Fatalf("got %d, want %d", got, tc.want) }
        })
    }
}
```

## sync.Mutex 패턴

```go
type SafeStore struct {
    mu    sync.Mutex
    items []Item
}

func (s *SafeStore) Add(item Item) {
    s.mu.Lock()
    defer s.mu.Unlock()
    s.items = append(s.items, item)
}

func (s *SafeStore) Snapshot() []Item {
    s.mu.Lock()
    defer s.mu.Unlock()
    out := make([]Item, len(s.items))
    copy(out, s.items)
    return out
}
```

**핵심**: Snapshot은 반드시 `copy`로 독립 슬라이스를 반환해야 한다. 내부 슬라이스 참조를 반환하면 lock 밖에서 race가 발생한다.

## CLI 명령 정리

```bash
# 모듈 초기화
go mod init github.com/woopinbell/go-backend/study/00-go-fundamentals/03-testing-and-debugging

# 실행
cd go
go run ./cmd/debugdemo

# 테스트 (기본)
go test ./...

# 벤치마크 포함
go test ./... -bench=.

# race detector 포함
go test -race ./...

# 특정 테스트만
go test -run TestParseLine -v ./analyzer/
```
