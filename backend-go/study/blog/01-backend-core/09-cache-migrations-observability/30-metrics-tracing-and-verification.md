# 09 Cache Migrations Observability — Metrics Tracing And Verification

`01-backend-core/09-cache-migrations-observability`는 cache-aside, cache invalidation, migration, metrics, trace header를 한 API로 묶어 운영 기본기를 붙이는 과제다. 이 글에서는 11단계: /metrics 핸들러 -> 12단계: main.go 작성 -> 13단계: 테스트 작성 -> 14단계: 실행 및 검증 구간을 따라가면서, 어떤 파일과 어떤 명령이 실제 구현 전환점이었는지 복원한다.

## 구현 순서 요약

- 11단계: /metrics 핸들러
- 12단계: main.go 작성
- 13단계: 테스트 작성
- 14단계: 실행 및 검증

## Day 1
### Session 1

- 당시 목표: 검증 명령과 공개 surface를 함께 닫고 `verified` 기준을 다시 확인한다.
- 변경 단위: `solution/go/internal/app/app_test.go`, `solution/go/cmd/server/main.go`
- 처음 가설: API, migration, metrics를 한 과제에 묶어 “기능 + 운영 표면”을 동시에 읽게 했다.
- 실제 진행: 포트 4050 사용. `TestCacheHitMiss` — 첫 조회 miss, 두 번째 hit 확인 `TestInvalidationOnUpdate` — update 후 다시 조회하면 miss (cacheMisses = 2) `TestMetricsEndpoint` — /metrics 응답에 `cache_hits_total` 존재 확인 `TestTraceHeader` — X-Trace-ID 요청 헤더가 응답에 그대로 전파됨 `TestUpdateEndpoint` — PUT 후 200 응답 아이템 조회 (first = miss) 다시 조회 (cache hit)

CLI:

```bash
go test ./internal/app/...

go run ./cmd/server
```

검증 신호:

- 2026-03-07 기준 `go test ./...`가 통과했다.
- 테스트는 cache hit/miss, invalidation, `/metrics`, `X-Trace-ID`, migration down을 포함한다.
- 남은 선택 검증: Redis adapter와 tracing backend는 이후 확장 포인트로 남겼다.

핵심 코드: `solution/go/internal/app/app_test.go`

```go
func newService(t *testing.T) (*Service, func()) {
	t.Helper()
	db, err := OpenInMemory()
	if err != nil {
		t.Fatalf("open db: %v", err)
	}
	ctx := context.Background()
	if err := ApplyUpMigration(ctx, db); err != nil {
		t.Fatalf("up migration: %v", err)
	}
	if err := Seed(ctx, db); err != nil {
		t.Fatalf("seed: %v", err)
	}
	return NewService(db, NewTestLogger()), func() { db.Close() }
}

func TestCacheHitMiss(t *testing.T) {
	t.Parallel()
```

왜 이 코드가 중요했는가:

이 테스트나 재현 스크립트는 프로젝트의 공개 표면을 말이 아니라 입력과 결과로 고정한다. 최종 글에서 이 증거를 빼면 구현은 보여도 완료 기준은 흐려진다.

새로 배운 것:

- structured logging은 trace id, path, method 같은 필드를 일관되게 남기는 습관이다.

보조 코드: `solution/go/cmd/server/main.go`

```go
func main() {
	db, err := app.OpenInMemory()
	if err != nil {
		log.Fatal(err)
	}
	ctx := context.Background()
	if err := app.ApplyUpMigration(ctx, db); err != nil {
		log.Fatal(err)
	}
	if err := app.Seed(ctx, db); err != nil {
		log.Fatal(err)
	}

	service := app.NewService(db, nil)
	log.Println("listening on :4050")
	log.Fatal(http.ListenAndServe(":4050", service.Routes()))
}
```

왜 이 코드도 같이 봐야 하는가:

이 조각은 프로젝트의 핵심 판단이 실제 어느 함수와 자료구조에 걸려 있는지 보여 준다. 추상 요약보다 먼저 이 코드를 봐야 구현 순서가 살아난다.

CLI:

```bash
cd 01-backend-core/09-cache-migrations-observability/go
go run ./cmd/server
go test ./...
```

검증 신호:

- 2026-03-07 기준 `go test ./...`가 통과했다.
- 테스트는 cache hit/miss, invalidation, `/metrics`, `X-Trace-ID`, migration down을 포함한다.

다음:

- Redis adapter와 tracing backend는 이후 확장 포인트로 남겼다.

## 마무리

이 글을 따로 떼어 쓴 이유는 결과 요약보다 구현 순서가 먼저 보이게 하기 위해서다. `solution/go/internal/app/app_test.go` 같은 결정적인 코드와 `cd 01-backend-core/09-cache-migrations-observability/go` 같은 검증 명령이 같은 글 안에 있어야, 이 프로젝트가 어떤 경계부터 닫았는지 추적할 수 있다.
