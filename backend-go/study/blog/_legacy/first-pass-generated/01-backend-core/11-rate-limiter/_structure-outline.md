# 11 Rate Limiter Structure Outline

이 문서는 chronology ledger를 바탕으로 최종 blog를 어떤 순서로 전개할지 먼저 고정한 설계 메모다. 기존 `blog/` 초안은 입력에서 제외했고, 실제 코드, README, docs, 테스트, CLI만을 근거로 삼는다.

## Planned Files

- `00-series-map.md`: 프로젝트 범위, source-of-truth, 읽는 순서를 잡는 진입 문서
- `01-evidence-ledger.md`: 파일, 함수, CLI 단위 chronology를 거칠게 복원한 근거 문서
- `10-2026-03-13-reconstructed-development-log.md`: 구현 순서와 판단 전환점을 세션 흐름으로 다시 쓴 최종 blog

## Final Blog Flow

- 도입: README 한 줄 요약과 이번 재검증 범위를 붙여 글의 위치를 먼저 밝힌다.
- 구현 순서 요약: Phase 1 -> Phase 2 -> Phase 3 순서를 미리 보여 준다.
- 세션형 chronology: 각 phase에서 당시 목표, 가설, 조치, 코드 앵커, 검증 신호를 순서대로 다시 적는다.
- CLI로 닫는 구간: 현재 저장소에서 다시 실행한 명령과 excerpt를 붙여 README 계약이 아직 살아 있는지 확인한다.
- 남은 질문: 개념 축과 다음 실험 지점을 남긴다.

## Section Plan

### 1. Phase 1 - Limiter와 refill 계산으로 token bucket 바닥을 먼저 고정한다

- 목표: Limiter와 refill 계산으로 token bucket 바닥을 먼저 고정한다
- 변경 단위: `solution/go/limiter.go`의 `Limiter.Allow`
- 핵심 가설: `Limiter.Allow`에서 refill 계산을 먼저 잠가야 middleware에서 client별 정책을 올려도 흔들리지 않는다고 봤다.
- 반드시 넣을 코드 앵커: `Limiter.Allow`
- 반드시 넣을 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `Running tests...`였다.
- 새로 배운 것 섹션 포인트: token bucket은 burst를 허용하면서 평균 처리율을 제한한다.
- 다음 섹션 연결 문장: ClientLimiter와 middleware로 요청 단위 경계를 붙인다
### 2. Phase 2 - ClientLimiter와 middleware로 요청 단위 경계를 붙인다

- 목표: ClientLimiter와 middleware로 요청 단위 경계를 붙인다
- 변경 단위: `solution/go/middleware.go`의 `RateLimitMiddleware`
- 핵심 가설: `RateLimitMiddleware`를 분리하면 전역 limiter와 per-client limiter를 같은 구조 안에서 비교하기 쉽다고 판단했다.
- 반드시 넣을 코드 앵커: `RateLimitMiddleware`
- 반드시 넣을 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `goos: darwin`였다.
- 새로 배운 것 섹션 포인트: IP 기반 식별은 쉬우나 NAT나 프록시 환경에서는 거칠 수 있다.
- 다음 섹션 연결 문장: unit test와 benchmark로 burst, refill, concurrency 계약을 잠근다
### 3. Phase 3 - unit test와 benchmark로 burst, refill, concurrency 계약을 잠근다

- 목표: unit test와 benchmark로 burst, refill, concurrency 계약을 잠근다
- 변경 단위: `solution/go/limiter_test.go`의 `TestLimiterConcurrency`
- 핵심 가설: `TestLimiterConcurrency` 같은 test, bench 조합이 있어야 token bucket 설명이 감상이 아니라 수치로 남는다고 봤다.
- 반드시 넣을 코드 앵커: `TestLimiterConcurrency`
- 반드시 넣을 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `goos: darwin`였다.
- 새로 배운 것 섹션 포인트: refill 계산을 부정확하게 하면 burst cap이 깨지거나 토큰이 과도하게 쌓인다.
- 다음 섹션 연결 문장: 마지막엔 현재 저장소에서 다시 돌린 CLI와 남은 질문으로 닫는다.

## Fixed CLI Anchor

        ```bash
(cd /Users/woopinbell/work/book-task-3/study/01-backend-core/11-rate-limiter && make -C problem test)
```

```text
Running tests...
cd ../solution/go && go test -v -race -count=1 ./...
=== RUN   TestLimiterBasic
=== RUN   TestLimiterBasic/first_token
=== RUN   TestLimiterBasic/second_token
=== RUN   TestLimiterBasic/third_token
=== RUN   TestLimiterBasic/fourth_token_(empty)
--- PASS: TestLimiterBasic (0.00s)
    --- PASS: TestLimiterBasic/first_token (0.00s)
    --- PASS: TestLimiterBasic/second_token (0.00s)
    --- PASS: TestLimiterBasic/third_token (0.00s)
    --- PASS: TestLimiterBasic/fourth_token_(empty) (0.00s)
=== RUN   TestLimiterRefill
--- PASS: TestLimiterRefill (0.25s)
=== RUN   TestLimiterBurstCap
--- PASS: TestLimiterBurstCap (0.10s)
=== RUN   TestLimiterConcurrency
--- PASS: TestLimiterConcurrency (0.00s)
=== RUN   TestClientLimiterBasic
--- PASS: TestClientLimiterBasic (0.00s)
=== RUN   TestClientLimiterCount
--- PASS: TestClientLimiterCount (0.00s)
... (20 more lines)
```

```bash
(cd /Users/woopinbell/work/book-task-3/study/01-backend-core/11-rate-limiter && cd solution/go && go test -bench=. -benchmem ./...)
```

```text
goos: darwin
goarch: arm64
pkg: github.com/woopinbell/go-backend/study/01-backend-core/11-rate-limiter
cpu: Apple M1
BenchmarkLimiterAllow-8         	 6170140	       165.1 ns/op	       0 B/op	       0 allocs/op
BenchmarkClientLimiterAllow-8   	 6150458	       203.1 ns/op	       0 B/op	       0 allocs/op
PASS
ok  	github.com/woopinbell/go-backend/study/01-backend-core/11-rate-limiter	3.284s
```
