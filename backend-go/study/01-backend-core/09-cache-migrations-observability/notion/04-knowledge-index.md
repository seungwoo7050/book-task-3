# 지식 색인 — 캐시·관측성 핵심 개념

## Cache-aside (Lazy Loading)

애플리케이션이 캐시를 직접 관리하는 패턴. 읽기: 캐시 확인 → miss면 DB 조회 → 캐시 저장. 쓰기: DB 수정 → 캐시 삭제(invalidation). DB가 원본이고 캐시는 복사본이다.

다른 캐시 전략과의 비교:
- **Write-through**: 쓰기 시 캐시와 DB를 동시에 갱신. 일관성 높지만 쓰기 느림.
- **Write-behind**: 쓰기를 캐시에만 하고 비동기로 DB 동기화. 빠르지만 데이터 유실 위험.
- **Cache-aside**: 읽기 최적화에 초점. 쓰기 시 캐시 삭제만 하므로 구현이 단순.

## Cache Invalidation

캐시의 오래된 데이터를 제거하는 행위. "컴퓨터 과학에서 어려운 두 가지: 캐시 무효화와 이름 짓기." 이 프로젝트에서는 update 시 `delete(cache, key)`로 처리. 실무에서는 TTL, 이벤트 기반 무효화, 패턴 기반 삭제 등 복잡한 전략이 필요하다.

## sync/atomic

Go의 원자적 연산 패키지. `atomic.Int64`의 `Add(1)`, `Load()`는 Mutex 없이 스레드 안전하게 카운터를 관리한다. 단일 값의 읽기/증가/저장만 필요할 때 Mutex보다 가볍다.

## Prometheus 텍스트 포맷

```
metric_name value
cache_hits_total 42
```

Prometheus 서버가 `/metrics`를 주기적으로 스크래핑해 시계열 데이터를 수집한다. 이 프로젝트에서는 공식 클라이언트 라이브러리 없이 텍스트를 직접 출력한다.

## Trace ID

분산 시스템에서 하나의 요청을 추적하기 위한 고유 식별자. 요청이 여러 서비스를 거칠 때, 같은 trace ID로 로그를 연결한다. 이 프로젝트에서는 `X-Trace-ID` 헤더로 전파한다.

## log/slog

Go 1.21에서 도입된 구조화된 로깅 패키지. 키-값 쌍으로 로그를 기록한다:

```go
slog.Info("request", "trace_id", traceID, "method", r.Method)
```

JSON 핸들러를 쓰면 `{"level":"INFO","msg":"request","trace_id":"..."}` 형태로 출력된다.

## 관측성(Observability)의 세 기둥

| 기둥 | 질문 | 이 프로젝트 |
|------|------|------------|
| **Logging** | "무슨 일이 일어났나?" | `slog.Info("request", ...)` |
| **Metrics** | "얼마나 자주/많이?" | `/metrics` (hit, miss, writes) |
| **Tracing** | "어디를 거쳤나?" | `X-Trace-ID` 전파 |

## withTrace 미들웨어 패턴

```go
func (s *Service) withTrace(next http.HandlerFunc) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        traceID := r.Header.Get("X-Trace-ID")
        if traceID == "" {
            traceID = fmt.Sprintf("trace-%d", rand.Int63())
        }
        w.Header().Set("X-Trace-ID", traceID)
        next(w, r)
    }
}
```

06의 미들웨어 패턴과 동일한 구조: 전처리 → next 호출 → (후처리).

## Seed 데이터

마이그레이션 후 초기 데이터를 삽입하는 것. 개발/테스트 환경에서는 seed 데이터가 있어야 API를 바로 검증할 수 있다. 프로덕션에서는 별도 관리하거나 생략한다.
