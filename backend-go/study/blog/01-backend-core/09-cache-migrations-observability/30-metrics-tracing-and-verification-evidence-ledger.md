# 09 Cache Migrations Observability Evidence Ledger

## 30 metrics-tracing-and-verification

- 시간 표지: 11단계: /metrics 핸들러 -> 12단계: main.go 작성 -> 13단계: 테스트 작성 -> 14단계: 실행 및 검증
- 당시 목표: 검증 명령과 공개 surface를 함께 닫고 `verified` 기준을 다시 확인한다.
- 변경 단위: `solution/go/internal/app/app_test.go`, `solution/go/cmd/server/main.go`
- 처음 가설: API, migration, metrics를 한 과제에 묶어 “기능 + 운영 표면”을 동시에 읽게 했다.
- 실제 조치: 포트 4050 사용. `TestCacheHitMiss` — 첫 조회 miss, 두 번째 hit 확인 `TestInvalidationOnUpdate` — update 후 다시 조회하면 miss (cacheMisses = 2) `TestMetricsEndpoint` — /metrics 응답에 `cache_hits_total` 존재 확인 `TestTraceHeader` — X-Trace-ID 요청 헤더가 응답에 그대로 전파됨 `TestUpdateEndpoint` — PUT 후 200 응답 아이템 조회 (first = miss) 다시 조회 (cache hit)

CLI:

```bash
go test ./internal/app/...

go run ./cmd/server
```

- 검증 신호:
- 2026-03-07 기준 `go test ./...`가 통과했다.
- 테스트는 cache hit/miss, invalidation, `/metrics`, `X-Trace-ID`, migration down을 포함한다.
- 남은 선택 검증: Redis adapter와 tracing backend는 이후 확장 포인트로 남겼다.
- 핵심 코드 앵커: `solution/go/internal/app/app_test.go`
- 새로 배운 것: structured logging은 trace id, path, method 같은 필드를 일관되게 남기는 습관이다.
- 다음: Redis adapter와 tracing backend는 이후 확장 포인트로 남겼다.
