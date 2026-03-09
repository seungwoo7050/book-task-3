# 접근 과정 — 캐시와 관측성을 구현하기까지

## 스키마와 시드 데이터

08보다 단순한 테이블을 선택했다. `items` 테이블에 id, name, version 세 컬럼:

```sql
CREATE TABLE items (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    version INTEGER NOT NULL DEFAULT 1
);
```

seed 데이터는 `starter-sword`와 `healing-potion` 두 개. 마이그레이션 후 바로 API를 테스트할 수 있도록 초기 데이터를 함께 넣었다.

## Cache-aside 패턴 구현

`GetItem`의 흐름:

```
1. mu.Lock() → cache 맵 확인
2. 있으면(hit): Unlock, cacheHits 증가, 반환
3. 없으면(miss): Unlock, cacheMisses 증가
4. DB에서 SELECT
5. mu.Lock() → cache에 저장 → Unlock
6. 반환
```

핵심은 **캐시 확인과 DB 조회 사이에 락을 풀어두는 것**이다. DB 조회 중에 락을 잡고 있으면 다른 요청도 대기해야 하므로, 캐시의 의미가 퇴색된다.

## Cache Invalidation

`UpdateItem`에서 DB UPDATE 후 캐시를 삭제한다:

```go
s.mu.Lock()
delete(s.cache, item.ID)
s.mu.Unlock()
```

"캐시를 갱신"하지 않고 "삭제"만 한다. 다음 읽기 요청에서 DB를 조회해 캐시에 다시 넣는다. 이렇게 하면 캐시에 오래된 데이터가 남지 않는다. 이 전략을 write-invalidate라고 부른다.

## 메트릭 — atomic으로 카운터

```go
type Metrics struct {
    cacheHits   atomic.Int64
    cacheMisses atomic.Int64
    writes      atomic.Int64
}
```

`sync/atomic`을 사용한 이유: Mutex보다 경량이다. 카운터 증가는 단일 연산이므로 atomic으로 충분하다. 복합 연산(읽기 → 비교 → 쓰기)이 필요하면 Mutex를 써야 하지만, 여기서는 `Add(1)`만 하면 된다.

`/metrics` 엔드포인트는 Prometheus 텍스트 포맷을 흉내낸다:

```
cache_hits_total 42
cache_misses_total 7
writes_total 3
```

## Trace ID 전파

`withTrace` 미들웨어가 요청의 `X-Trace-ID` 헤더를 읽고, 없으면 생성한다. 같은 값을 응답 헤더에 그대로 넣는다. 로그에도 trace_id를 포함시킨다:

```go
s.logger.Info("request", "trace_id", traceID, "method", r.Method, "path", r.URL.Path)
```

이로써 하나의 요청이 로그 → 메트릭 → 응답 헤더까지 일관된 ID로 추적된다.

## 구조화된 로깅 — log/slog

Go 1.21에서 도입된 `log/slog`를 사용한다. 키-값 쌍으로 로그를 남기므로, JSON이나 텍스트 포맷으로 일관되게 출력할 수 있다. `fmt.Printf`로 로그를 찍으면 파싱이 어렵지만, `slog.Info("request", "trace_id", id)`는 구조화되어 있어 로그 검색 도구에서 필터링이 된다.

테스트에서는 `NewTestLogger`로 출력을 버린다(discardWriter). 테스트 로그가 stdout을 오염시키지 않도록.
