# 09 Cache Migrations Observability Structure Outline

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

### 1. Phase 1 - ApplyUpMigration과 Service로 캐시 가능한 데이터 경계를 먼저 세운다

- 목표: ApplyUpMigration과 Service로 캐시 가능한 데이터 경계를 먼저 세운다
- 변경 단위: `solution/go/internal/app/app.go`의 `ApplyUpMigration`
- 핵심 가설: `ApplyUpMigration` 쪽에서 상태 경계를 먼저 세우면 HTTP layer는 훨씬 단순해질 것이라고 봤다.
- 반드시 넣을 코드 앵커: `ApplyUpMigration`
- 반드시 넣을 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `=== RUN   TestCacheHitMiss`였다.
- 새로 배운 것 섹션 포인트: cache-aside는 읽기 시 캐시를 먼저 보고, miss면 DB를 읽어 캐시에 채우는 패턴이다.
- 다음 섹션 연결 문장: metrics, trace, update endpoint로 관측 표면을 붙인다
### 2. Phase 2 - metrics, trace, update endpoint로 관측 표면을 붙인다

- 목표: metrics, trace, update endpoint로 관측 표면을 붙인다
- 변경 단위: `solution/go/internal/app/app.go`의 `NewService`
- 핵심 가설: `NewService`에 transport 규칙을 모아 두면 validation과 응답 shape를 한곳에서 설명할 수 있다고 판단했다.
- 반드시 넣을 코드 앵커: `NewService`
- 반드시 넣을 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `=== RUN   TestMetricsEndpoint`였다.
- 새로 배운 것 섹션 포인트: trace backend 없이 trace id만 남기면 상호 연동은 없지만 요청 상관관계는 잡을 수 있다.
- 다음 섹션 연결 문장: app_test로 cache hit/miss와 invalidation 계약을 잠근다
### 3. Phase 3 - app_test로 cache hit/miss와 invalidation 계약을 잠근다

- 목표: app_test로 cache hit/miss와 invalidation 계약을 잠근다
- 변경 단위: `solution/go/internal/app/app_test.go`의 `TestCacheHitMiss`
- 핵심 가설: `TestCacheHitMiss` 같은 테스트가 있어야 handler, auth, cache 계약이 서로 섞이지 않는다고 봤다.
- 반드시 넣을 코드 앵커: `TestCacheHitMiss`
- 반드시 넣을 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `=== RUN   TestMetricsEndpoint`였다.
- 새로 배운 것 섹션 포인트: metrics를 텍스트로 직접 쓰면 간단하지만 라벨 모델링은 제한적이다.
- 다음 섹션 연결 문장: 마지막엔 현재 저장소에서 다시 돌린 CLI와 남은 질문으로 닫는다.

## Fixed CLI Anchor

```bash
(cd /Users/woopinbell/work/book-task-3/backend-go/study/01-backend-core/09-cache-migrations-observability && cd solution/go && go test -v ./internal/app)
```

```text
=== RUN   TestCacheHitMiss
=== PAUSE TestCacheHitMiss
=== RUN   TestInvalidationOnUpdate
=== PAUSE TestInvalidationOnUpdate
=== RUN   TestMetricsEndpoint
=== PAUSE TestMetricsEndpoint
=== RUN   TestTraceHeader
=== PAUSE TestTraceHeader
=== RUN   TestUpdateEndpoint
=== PAUSE TestUpdateEndpoint
=== RUN   TestDownMigration
=== PAUSE TestDownMigration
=== CONT  TestCacheHitMiss
=== CONT  TestDownMigration
=== CONT  TestTraceHeader
=== CONT  TestMetricsEndpoint
=== CONT  TestUpdateEndpoint
=== CONT  TestInvalidationOnUpdate
--- PASS: TestDownMigration (0.00s)
--- PASS: TestMetricsEndpoint (0.00s)
--- PASS: TestCacheHitMiss (0.00s)
--- PASS: TestUpdateEndpoint (0.00s)
... (4 more lines)
```

```bash
(cd /Users/woopinbell/work/book-task-3/backend-go/study/01-backend-core/09-cache-migrations-observability && cd solution/go && go test -run TestMetricsEndpoint -v ./internal/app)
```

```text
=== RUN   TestMetricsEndpoint
=== PAUSE TestMetricsEndpoint
=== CONT  TestMetricsEndpoint
--- PASS: TestMetricsEndpoint (0.00s)
PASS
ok  	github.com/woopinbell/go-backend/study/01-backend-core/09-cache-migrations-observability/internal/app	(cached)
```
